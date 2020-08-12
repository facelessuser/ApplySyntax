"""Apply Syntax."""
import sublime
import sublime_plugin
import os
import re
import imp
import sys
from wcmatch import glob

GLOB_FLAGS = glob.G | glob.B | glob.E | glob.N | glob.D

DEFAULT_SETTINGS = '''
{
    // If you want exceptions reraised so you can see them in the console, change this to true.
    "reraise_exceptions": false,

    // If you want to have a syntax applied when new files are created, set new_file_syntax to the name of the syntax
    // to use.  The format is exactly the same as "syntax" in the rules below. For example, if you want to have a new
    // file use JavaScript syntax, set new_file_syntax to 'JavaScript'.
    "new_file_syntax": false,

    // Auto add extensions to language settings file in User folder.
    // Do not manually remove "apply_syntax_extensions" from the settings file.
    // "extenstions" are ignored by "match": "all" setting.
    "add_exts_to_lang_settings": true,

    // Control level of logging in the console.
    // (true|false|"verbose")
    "debug": true,

    // Put your custom syntax rules here:
    "syntaxes": [
    ]
}
'''

USE_ST_SYNTAX = int(sublime.version()) >= 3084
PLUGIN_NAME = 'ApplySyntax'
PLUGIN_DIR = "Packages/%s" % PLUGIN_NAME
PLUGIN_SETTINGS = PLUGIN_NAME + '.sublime-settings'
EXT_SETTINGS = PLUGIN_NAME + ".ext-list"
ST_LANGUAGES = ('.sublime-syntax', '.tmLanguage') if USE_ST_SYNTAX else ('.tmLanguage',)
SETTINGS = {}
LANG_HASH = 0

# Call back for whether view(s) have been touched
on_touched_callback = None


def ensure_user_settings():
    """Create a default 'User' settings file for ApplySyntax if it doesn't exist."""

    user_settings_file = os.path.join(sublime.packages_path(), 'User', PLUGIN_SETTINGS)
    if os.path.exists(user_settings_file):
        return

    # file doesn't exist, let's create a bare one
    with open(user_settings_file, 'w') as f:
        f.write(DEFAULT_SETTINGS)


def get_all_syntax_files():
    """Find all `sublime-syntax` and `tmLanguage` files."""

    syntax_files = []
    if USE_ST_SYNTAX:
        syntax_files += sublime.find_resources("*.sublime-syntax")
    syntax_files += sublime.find_resources("*.tmLanguage")
    return syntax_files


def sublime_format_path(pth):
    """Format the path for the sublime API."""

    m = re.match(r"^([A-Za-z]{1}):(?:/|\\)(.*)", pth)
    if sublime.platform() == "windows" and m is not None:
        pth = m.group(1) + "/" + m.group(2)
    return pth.replace("\\", "/")


def get_lang_hash():
    """
    Return the hash of the loaded languages in Sublime.

    Return the actual language `frozenset` (hashable) as well.
    """

    def was_seen(item, item_set):
        """Check if item was seen already."""

        seen_item = True
        base = os.path.splitext(item)[0]
        if base is not item_set:
            item_set.add(base)
            seen_item = False
        return seen_item

    # Strip off `tmlanguage` so we don't have to worry about case of extension
    seen = set()
    lst = frozenset(
        [os.path.splitext(x)[0] for x in get_all_syntax_files() if not was_seen(x, seen)]
    )
    hsh = hash(lst)
    devlog("Language Hash - '%s'" % str(hsh))
    return hsh, lst


def update_language_extensions(ext_added):
    """Process the extensions for each language."""

    for lang, exts in ext_added.items():
        updated = False
        settings_file = lang + ".sublime-settings"
        lang_settings = sublime.load_settings(settings_file)
        extension_file = sublime.load_settings(EXT_SETTINGS)
        lang_ext = set(lang_settings.get("extensions", []))
        apsy_ext = set(extension_file.get(lang, []))

        for ext in list(exts):
            if ext not in lang_ext:
                # Append extension to current sublime extension list
                lang_ext.add(ext)
                # Track which extensions were specifically added by apply syntax
                apsy_ext.add(ext)
                updated = True

        if updated:
            devlog("============" + settings_file + "============")
            devlog("Updated Extensions: %s" % str(lang_ext))
            lang_settings.set("extensions", list(lang_ext))
            if len(apsy_ext):
                extension_file.set(lang, sorted(list(apsy_ext)))
            else:
                extension_file.erase(sorted(lang))
            sublime.save_settings(settings_file)
            sublime.save_settings(EXT_SETTINGS)


def map_extensions(ext, lst, names, ext_map, ext_added):
    """Create mappings to help with updating and pruning extensions."""

    # Always deal with language names as a series of names
    if not isinstance(names, list):
        names = [names]

    # For each language name that currently exists and is loaded,
    # append the extensions to the corresponding settings file
    # if the extension is not already there

    for n in names:
        # updated = False
        path = os.path.dirname(n)
        name = os.path.basename(n)
        syntax_file = sublime_format_path('/'.join(['Packages', path, name]))
        if syntax_file in lst:
            for e in ext:
                if e in ext_map:
                    ext_map[e].append(name)
                else:
                    ext_map[e] = [name]

        for ext, languages in ext_map.items():
            lang = languages[-1]
            ext_map[ext] = [lang]
            ext_added[lang].add(ext)


def prune_language_extensions(ext_map, ext_added):
    """
    Prune dead extensions that were added by ApplySyntax (AS), but are no longer defined in AS.

    `exts`        - Sublime's extension list for the given language
    `old_ext`     - The current saved list of AS added extension
    `new_ext`     - The current tracked list of extensions found defined by AS
    `bad_ext`     - (`old_ext` - `new_ext`) Extensions that were added by AS but are no longer defined
    `updated_ext` - (`ext` - `bad_ext`) Sublime's adjusted extension list minus the obsolete ones
    """

    devlog("Pruning Extensions")
    for name, new_ext in ext_added.items():
        updated = False
        settings_file = name + '.sublime-settings'
        lang_settings = sublime.load_settings(settings_file)
        extension_file = sublime.load_settings(EXT_SETTINGS)
        exts = set(lang_settings.get("extensions", []))
        old_ext = set(extension_file.get(name, []))

        # Calculate the correct extension list
        bad_ext = old_ext.difference(new_ext)
        updated_ext = exts.difference(bad_ext)

        # Remove extension from file it ApplySyntax added
        # it to a different file
        for ext in list(updated_ext):
            try:
                if ext_map[ext][-1] != name:
                    updated_ext.remove(ext)
            except Exception:
                pass

        # Update settings file if necessary
        if len(updated_ext) != len(exts):
            # Update pruned list
            lang_settings.set("extensions", sorted(list(updated_ext)))
            if len(new_ext) == 0:
                # No currently added extensions by AS
                extension_file.erase(name)
            else:
                # Updated with relevant AS extensions
                extension_file.set(name, sorted(list(new_ext)))
            updated = True

        if updated:
            devlog("============" + settings_file + "============")
            devlog("Pruned Extensions: %s" % str(bad_ext))
            sublime.save_settings(settings_file)
            sublime.save_settings(EXT_SETTINGS)


def update_extenstions(lst):
    """Walk through all syntax rules updating the extensions in the corresponding language settings."""

    devlog("Updating Extensions")

    # Prepare a list to track extensions defined by ApplySyntax
    ext_added = dict([(os.path.splitext(os.path.basename(l))[0], set()) for l in lst])
    ext_map = {}

    # Walk the entries
    for entry in SETTINGS.get("syntaxes", []) + SETTINGS.get("default_syntaxes", []):
        # Grab the extensions from each relevant rule
        ext = []
        if "extensions" in entry:
            ext += entry.get("extensions", [])

        # Add the extensions to the relevant language settings file
        if len(ext):
            syntax = entry.get("syntax", entry.get("name"))
            if isinstance(syntax, list):
                for s in syntax:
                    name = os.path.splitext(s)[0]
                    devlog("Found Extensions: %s - %s" % (name, str(ext)))
                    map_extensions(ext, lst, name, ext_map, ext_added)
            else:
                name = os.path.splitext(syntax)[0]
                devlog("Found Extensions: %s - %s" % (name, str(ext)))
                map_extensions(ext, lst, name, ext_map, ext_added)

    update_language_extensions(ext_added)

    prune_language_extensions(ext_map, ext_added)


def log(msg):
    """Print the ApplySyntax log message in console."""

    print("ApplySyntax: %s" % msg)


def debug(msg):
    """Print the debug ApplySyntax log message in console (debug mode only)."""

    if SETTINGS.get("debug", True) in (True, 'verbose'):
        log(msg)


def devlog(msg):
    """Print the developer mode ApplySyntax log message in console (developer mode only)."""

    if SETTINGS.get("debug", True) == 'verbose':
        log(msg)


class ApplySyntaxCommand(sublime_plugin.EventListener):
    """ApplySyntax command."""

    def __init__(self):
        """Initialization."""

        global on_touched_callback
        self.first_line = None
        self.file_name = None
        self.entire_file = None
        self.view = None
        self.syntaxes = []
        self.reraise_exceptions = False
        self.seen_deprecation_warnings = set()

        on_touched_callback = self.on_touched

    def print_deprecation_warning(self, keyword, rule=None):
        """Print the deprecation warnings."""

        if rule is not None:
            warn_key = "%s,%s" % (keyword, rule)
        else:
            warn_key = keyword

        if warn_key not in self.seen_deprecation_warnings:
            self.seen_deprecation_warnings.add(warn_key)
            if rule is None:
                log(
                    "Warning: '%s' keyword is deprecated and will be removed in the future."
                    % keyword
                )
            else:
                log(
                    "Warning: '%s' keyword in '%s' rule is deprecated and will be removed in the future."
                    % (keyword, rule)
                )

    def touch(self, view):
        """Touch the view."""

        view.settings().set("apply_syntax_touched", True)

    def update_extenstions(self):
        """Only update extensions if desired."""

        if not SETTINGS.get("add_exts_to_lang_settings", False):
            devlog("Skipping Extension Update")
            return

        global LANG_HASH
        hsh, lst = get_lang_hash()
        if LANG_HASH != hsh:
            LANG_HASH = hsh
            update_extenstions(lst)

    def get_setting(self, name, default=None):
        """Get the settings."""

        active_settings = self.view.settings() if self.view else {}
        key_exist = name in active_settings if isinstance(active_settings, dict) else active_settings.has(name)
        return active_settings.get(name) if key_exist else SETTINGS.get(name, default)

    def on_new(self, view):
        """Apply syntax on new file."""
        self.touch(view)
        self.update_extenstions()
        name = self.get_setting("new_file_syntax")
        if name:
            self.view = view
            self.set_syntax(name)

    def on_load(self, view):
        """Apply syntax on file load."""

        self.touch(view)
        self.update_extenstions()
        self.detect_syntax(view)

    def on_post_save(self, view):
        """Apply syntax on save."""

        self.touch(view)
        self.update_extenstions()
        self.detect_syntax(view)

    def on_touched(self, view):
        """Apply syntax to untouched views."""

        self.touch(view)
        self.update_extenstions()
        self.detect_syntax(view)

    def detect_syntax(self, view):
        """Detect the syntax."""

        self.plugins = {}
        if view.is_scratch() or not view.file_name():  # buffer has never been saved
            return

        self.reset_cache_variables(view)
        self.load_syntaxes()

        if not self.syntaxes:
            return

        found = False
        for syntax in self.syntaxes:
            # stop on the first syntax that matches
            if self.syntax_matches(syntax):
                found = True
                self.set_syntax(syntax.get("syntax"))
                break

        # If pattern matches extension trim pattern, try again after trimming the extension
        if not found:
            for ext_trim in self.ext_trim:
                try:
                    match = False
                    pattern = ext_trim.get('file_path')
                    if pattern:
                        match = re.match(pattern, self.file_name) is not None
                    if not match:
                        pattern = ext_trim.get('globmatch')
                        case = glob.C if ext_trim.get('case', False) else glob.I
                        match = glob.globmatch(self.file_name, pattern, flags=GLOB_FLAGS | case)
                except Exception:
                    if self.reraise_exceptions:
                        raise
                    else:
                        match = False

                if match:
                    parts = os.path.splitext(self.orig_file_name)
                    # If there is no extension, then there is nothing to do
                    if parts[1]:
                        self.file_name = parts[0]
                        for syntax in self.syntaxes:
                            if self.syntax_matches(syntax):
                                self.set_syntax(syntax.get("syntax", syntax.get("name")))
                                break
                    break

        self.plugins = {}

    def reset_cache_variables(self, view):
        """Reset variables."""

        self.view = view
        self.file_name = view.file_name()
        self.orig_file_name = self.file_name
        self.first_line = None  # We read the first line only when needed
        self.entire_file = None  # We read the contents of the entire file only when needed
        self.syntaxes = []
        self.reraise_exceptions = False

    def fetch_first_line(self):
        """Get the first line."""

        self.first_line = self.view.substr(self.view.line(0))  # load the first line only when needed

    def fetch_entire_file(self):
        """Get the entire file content."""

        self.entire_file = self.view.substr(sublime.Region(0, self.view.size()))  # load file only when needed

    def set_syntax(self, name):
        """
        Set the syntax.

        The default settings file uses / to separate the syntax name parts, but if the user
        is on windows, that might not work right. And if the user happens to be on Mac/Linux but
        is using rules that were written on windows, the same thing will happen. So let's
        be intelligent about this and replace forward slashes and back slashes with `os.path.sep` to get
        a reasonable starting point.
        """

        if not isinstance(name, list):
            names = [name]
        else:
            names = name

        for n in names:
            if not n:
                continue

            path = os.path.dirname(n)
            if not path:
                continue

            for ext in ST_LANGUAGES:
                lang_ext = os.path.splitext(n)[1]
                if lang_ext and lang_ext in ST_LANGUAGES:
                    if lang_ext != ext:
                        continue

                name = os.path.splitext(os.path.basename(n))[0]
                file_name = name + ext
                new_syntax = sublime_format_path('/'.join(['Packages', path, file_name]))

                current_syntax = self.view.settings().get('syntax')

                # only set the syntax if it's different
                if new_syntax != current_syntax:
                    # let's make sure it exists first!
                    try:
                        sublime.load_resource(new_syntax)
                        self.view.set_syntax_file(new_syntax)
                        debug('Syntax set to ' + name + ' using ' + new_syntax)
                        return
                    except Exception:
                        debug('Syntax file for ' + name + ' does not exist at ' + new_syntax)
                else:
                    debug('Syntax already set to ' + new_syntax)
                    return

    def create_extension_rule(self, syntaxes):
        """Create a rules for the defined extensions."""

        for syntax in syntaxes:
            if 'extensions' in syntax:
                if 'rules' not in syntax:
                    syntax['rules'] = []
                syntax['rules'].insert(0, {'extensions': syntax['extensions']})
        return syntaxes

    def load_syntaxes(self):
        """Load syntax rules."""

        self.reraise_exceptions = SETTINGS.get("reraise_exceptions")
        # load the default syntaxes
        default_syntaxes = self.create_extension_rule(
            self.get_setting("default_syntaxes", [])
        )
        # load any user-defined syntaxes
        user_syntaxes = self.create_extension_rule(
            self.get_setting("syntaxes", [])
        )
        # load any project-defined syntaxes
        project_syntaxes = self.create_extension_rule(
            self.get_setting("project_syntaxes", [])
        )

        self.syntaxes = project_syntaxes + user_syntaxes + default_syntaxes

        default_ext_trim = self.get_setting("default_ext_trim", [])
        user_ext_trim = self.get_setting("ext_trim", [])
        project_ext_trim = self.get_setting("project_ext_trim", [])

        self.ext_trim = default_ext_trim + user_ext_trim + project_ext_trim

    def syntax_matches(self, syntax):
        """Match syntax rules."""

        rules = syntax.get("rules", [])
        match_all = syntax.get("match") == 'all'

        for rule in rules:
            if 'extensions' in rule:
                # Do not let 'extensions' contribute to 'match_all'
                result = self.extension_matches(rule)
                if result:
                    return True
                else:
                    continue

            if 'globmatch' in rule:
                result = self.glob_matches(rule)
            elif 'function' in rule:
                result = self.function_matches(rule)
            else:
                result = self.regexp_matches(rule)

            if match_all:
                # can return on the first failure since they all
                # have to match
                if not result:
                    return False
            elif result:
                # return on first match. don't return if it doesn't
                # match or else the remaining rules won't be applied
                return True

        if match_all:
            # if we need to match all and we got here, then all of the
            # rules matched
            return True
        else:
            # if we needed to match just one and got here, none of the
            # rules matched
            return False

    def get_function(self, path_to_file):
        """Get the match function."""
        try:
            path_name = sublime_format_path(os.path.join("Packages", path_to_file))
            module_name = os.path.splitext(path_name)[0].replace('Packages/', '', 1).replace('/', '.')
            module = imp.new_module(module_name)
            sys.modules[module_name] = module
            exec(compile(sublime.load_resource(path_name), module_name, 'exec'), sys.modules[module_name].__dict__)
            function = getattr(module, "syntax_test")
        except Exception:
            if self.reraise_exceptions:
                raise
            else:
                function = None

        return function

    def extension_matches(self, rule):
        """Match extension."""

        match = False
        extensions = rule.get('extensions', [])
        file_name = os.path.basename(self.file_name).lower()
        for extension in extensions:
            ext = extension.lower()
            dot_file_match = ext.startswith('.') and ext == file_name
            if dot_file_match or file_name.endswith('.' + ext):
                match = True
                break
        return match

    def function_matches(self, rule):
        """Perform function match."""

        function_rule = rule.get("function")
        source = function_rule.get("source")
        args = function_rule.get("args", None)
        if source in self.plugins:
            function = self.plugins[source]
        else:
            if not source or source.lower().endswith(".py"):
                # Bad format
                return False

            path_to_file = source.replace('.', '/') + '.py'
            function = self.get_function(path_to_file)

            if function is None:
                # can't find it ... nothing more to do
                return False
            else:
                self.plugins[source] = function

        try:
            return function(self.file_name, **args) if args is not None else function(self.file_name)
        except Exception:
            if self.reraise_exceptions:
                raise
            else:
                return False

    def glob_matches(self, rule):
        """Perform glob matches."""

        result = False
        pattern = rule.get('globmatch')
        if pattern:
            case = glob.C if rule.get('case', False) else glob.I
            result = glob.globmatch(self.file_name, pattern, flags=GLOB_FLAGS | case)
        return result

    def regexp_matches(self, rule):
        """Perform regex matches."""

        from_beginning = True  # match only from the beginning or anywhere in the string

        if "first_line" in rule:
            if self.first_line is None:
                self.fetch_first_line()
            subject = self.first_line
            regexp = rule.get("first_line")
        elif "interpreter" in rule:
            if self.first_line is None:
                self.fetch_first_line()
            subject = self.first_line
            regexp = '^#\\!(?:.+)' + rule.get("interpreter")
        elif "file_path" in rule:
            subject = self.file_name
            regexp = rule.get("file_path")
        elif "contains" in rule:
            if self.entire_file is None:
                self.fetch_entire_file()
            subject = self.entire_file
            regexp = rule.get("contains")
            from_beginning = False  # requires us to match anywhere in the file
        else:
            return False

        if regexp and subject:
            if from_beginning:
                result = re.match(regexp, subject)
            else:
                result = re.search(regexp, subject)  # matches anywhere, not only from the beginning
            return result is not None
        else:
            return False


def touch_untouched():
    """Touch the untouched views."""

    for window in sublime.windows():
        for view in window.views():
            if not view.settings().get("apply_syntax_touched", False):
                if on_touched_callback is not None:
                    on_touched_callback(view)
                else:
                    devlog("EventListener not loaded yet")


def on_reload():
    """
    Only update extensions if desired.

    Remove extensions added by ApplySyntax if disabled.
    """

    if not SETTINGS.get("add_exts_to_lang_settings", False):
        ext_added = dict(
            [(os.path.splitext(os.path.basename(l))[0], set()) for l in get_lang_hash()[1]]
        )
        ext_map = {}
        devlog("Skipping Extension Update")
        prune_language_extensions(ext_map, ext_added)
    else:
        global LANG_HASH
        LANG_HASH, lang_list = get_lang_hash()
        update_extenstions(lang_list)


def plugin_loaded():
    """Setup plugin."""

    global SETTINGS
    ensure_user_settings()
    SETTINGS = sublime.load_settings(PLUGIN_SETTINGS)
    SETTINGS.clear_on_change('reload')
    SETTINGS.add_on_change('reload', on_reload)
    on_reload()
    touch_untouched()
