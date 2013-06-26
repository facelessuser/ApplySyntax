import sublime
import sublime_plugin
import os
import re
import imp
import sys
import warnings

DEFAULT_SETTINGS = \
'''
{
    // If you want exceptions reraised so you can see them in the console, change this to true.
    "reraise_exceptions": false,

    // If you want to have a syntax applied when new files are created, set new_file_syntax to the name of the syntax to use.
    // The format is exactly the same as "name" in the rules below. For example, if you want to have a new file use
    // JavaScript syntax, set new_file_syntax to 'JavaScript'.
    "new_file_syntax": false,

    // Put your custom syntax rules here:
    "syntaxes": [
    ]
}
'''


def sublime_format_path(pth):
    m = re.match(r"^([A-Za-z]{1}):(?:/|\\)(.*)", pth)
    if sublime.platform() == "windows" and m != None:
        pth = m.group(1) + "/" + m.group(2)
    return pth.replace("\\", "/")


def log(msg):
    print("ApplySyntax: %s" % msg)


def debug(msg):
    if bool(sublime.load_settings('ApplySyntax.sublime-settings').get("debug_enabled", False)):
        log(msg)


class ApplySyntaxCommand(sublime_plugin.EventListener):
    def __init__(self):
        self.first_line = None
        self.file_name = None
        self.entire_file = None
        self.view = None
        self.syntaxes = []
        self.plugin_name = 'ApplySyntax'
        self.plugin_dir = os.path.join(sublime.packages_path(), self.plugin_name)
        self.settings_file = self.plugin_name + '.sublime-settings'
        self.reraise_exceptions = False

    def on_new(self, view):
        self.ensure_user_settings()
        settings = sublime.load_settings(self.settings_file)
        name = settings.get("new_file_syntax")
        if name:
            self.view = view
            self.set_syntax(name)

    def on_load(self, view):
        self.detect_syntax(view)

    def on_post_save(self, view):
        self.detect_syntax(view)

    def detect_syntax(self, view):
        if view.is_scratch() or not view.file_name:  # buffer has never been saved
            return

        self.reset_cache_variables(view)
        self.load_syntaxes()

        if not self.syntaxes:
            return

        for syntax in self.syntaxes:
            # stop on the first syntax that matches
            if self.syntax_matches(syntax):
                self.set_syntax(syntax.get("name"))
                break

    def reset_cache_variables(self, view):
        self.view = view
        self.file_name = view.file_name()
        self.first_line = None # we read the first line only when needed
        self.entire_file = None # we read the contents of the entire file only when needed
        self.syntaxes = []
        self.reraise_exceptions = False

    def fetch_first_line(self):
        self.first_line = self.view.substr(self.view.line(0)) # load the first line only when needed

    def fetch_entire_file(self):
        self.entire_file = self.view.substr(sublime.Region(0, self.view.size())) # load file only when needed

    def set_syntax(self, name):
        # the default settings file uses / to separate the syntax name parts, but if the user
        # is on windows, that might not work right. And if the user happens to be on Mac/Linux but
        # is using rules that were written on windows, the same thing will happen. So let's
        # be intelligent about this and replace / and \ with os.path.sep to get to
        # a reasonable starting point

        path = os.path.dirname(name)
        name = os.path.basename(name)

        if not path:
            path = name

        file_name = name + '.tmLanguage'
        new_syntax = sublime_format_path(os.path.join("Packages", path, file_name))
        file_path = os.path.join(sublime.packages_path(), path, file_name)

        current_syntax = self.view.settings().get('syntax')

        # only set the syntax if it's different
        if new_syntax != current_syntax:
            # let's make sure it exists first!
            if os.path.exists(file_path):
                self.view.set_syntax_file(new_syntax)
                log('Syntax set to ' + name + ' using ' + new_syntax)
            else:
                log('Syntax file for ' + name + ' does not exist at ' + new_syntax)

    def load_syntaxes(self):
        self.ensure_user_settings()
        settings = sublime.load_settings(self.settings_file)
        self.reraise_exceptions = settings.get("reraise_exceptions")
        # load the default syntaxes
        default_syntaxes = settings.get("default_syntaxes")
        if default_syntaxes is None:
            default_syntaxes = []
        # load any user-defined syntaxes
        user_syntaxes = settings.get("syntaxes")
        if user_syntaxes is None:
            user_syntaxes = []

        self.syntaxes = user_syntaxes + default_syntaxes

    def syntax_matches(self, syntax):
        rules = syntax.get("rules")
        match_all = syntax.get("match") == 'all'

        for rule in rules:
            if 'function' in rule:
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

    def get_function(self, path_to_file, function_name):
        try:
            path_name = sublime_format_path(path_to_file.replace(sublime.packages_path(), ''))
            module_name = os.path.splitext(path_name)[0].replace('/', '.')
            with warnings.catch_warnings(record=True) as w:
                # Ignore warnings about plugin folder not being a python package
                warnings.simplefilter("always")
                module = imp.new_module(module_name)
                w = filter(lambda i: issubclass(i.category, UserWarning), w)
                sys.modules[module_name] = module
                with open(path_to_file, "r") as f:
                    source = f.read()
                self.execute_function(source, module_name)

            function = getattr(module, function_name)
        except:
            if self.reraise_exceptions:
                raise
            else:
                function = None

        return function

    def execute_function(self, source, module_name):
        exec(compile(source, module_name, 'exec'), sys.modules[module_name].__dict__)

    def function_matches(self, rule):
        function = rule.get("function")
        path_to_file = function.get("source")
        function_name = function.get("name")

        if not path_to_file:
            path_to_file = function_name + '.py'

        if re.match(r"^Packages(?:\\|/)", path_to_file) is None:
            path_to_file = os.path.join(self.plugin_dir, path_to_file)
        else:
            path_to_file = os.path.join(os.path.dirname(sublime.packages_path()), path_to_file)
        function = self.get_function(path_to_file, function_name)

        if function is None:
            # can't find it ... nothing more to do
            return False

        try:
            return function(self.file_name)
        except:
            if self.reraise_exceptions:
                raise
            else:
                return False

    def regexp_matches(self, rule):
        from_beginning = True # match only from the beginning or anywhere in the string

        if "first_line" in rule:
            if self.first_line is None:
                self.fetch_first_line()
            subject = self.first_line
            regexp = rule.get("first_line")
        elif "binary" in rule:
            if self.first_line is None:
                self.fetch_first_line()
            subject = self.first_line
            regexp = '^#\\!(?:.+)' + rule.get("binary")
        elif "file_name" in rule:
            subject = self.file_name
            regexp = rule.get("file_name")
        elif "contains" in rule:
            if self.entire_file is None:
                self.fetch_entire_file()
            subject = self.entire_file
            regexp = rule.get("contains")
            from_beginning = False # requires us to match anywhere in the file
        else:
            return False

        if regexp and subject:
            if from_beginning:
                result = re.match(regexp, subject)
            else:
                result = re.search(regexp, subject) # matches anywhere, not only from the beginning
            return result is not None
        else:
            return False

    def ensure_user_settings(self):
        user_settings_file = os.path.join(sublime.packages_path(), 'User', self.settings_file)
        if os.path.exists(user_settings_file):
            return

        # file doesn't exist, let's create a bare one
        with open(user_settings_file, 'w') as f:
            f.write(DEFAULT_SETTINGS)
