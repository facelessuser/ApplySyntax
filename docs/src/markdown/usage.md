# User Guide

## Overview

ApplySyntax is based on the idea of creating rules for applying certain syntaxes to specific files. You define the rules, the plugin checks them. The first one to pass wins.

ApplySyntax allows you to create your own custom rules. The easiest way to get started is to create a settings file called `ApplySyntax.sublime-settings` in your `Packages/User` folder.  You can override the default settings in `Packages/ApplySyntax/ApplySyntax.sublime-settings` by setting them in your `Packages/User/ApplySyntax.sublime-settings` file. You can override any setting to meet your needs.  To prepend rules to the default rule set, you can create a key called `syntaxes` (modifying `default_syntaxes` will wipe out all the default rules and is not recommended as you won't get the latest updates).

## Creating Rules

Each rule is a dictionary within the syntax array.  Let's take a look at the top level parameters.

### Syntax

The `syntax` attribute is the syntax file that will be applied to a view which meets the criteria defined in the rule.

For syntax files you must specify the path to the syntax file. The plugin is capable of supporting multiple levels of folder nesting if you need it to. For example, if you had all of your tmLanguage files for Rails organized in a folder like this: `Packages/Rails/Language/*.tmLanguage`, and you were looking to use the `Ruby Haml.tmLanguage` file, the path to name translation would simply be: `Packages/Rails/Language/Ruby Haml.tmLanguage` --> `Rails/Language/Ruby Haml`.

```js
"syntax": "Rails/Language/Ruby Haml"
```

Notice that the paths are relative to the `Packages` folder.  Also, notice that we don't specify the extension.  Sublime Text in build 3084 added a new language syntax with the extension `sublime-syntax`.  In Sublime builds >= 3084, ApplySyntax will first default to `sublime-syntax` and fall back to `tmLanguage` if it cannot find the the other format.  If you want to force the syntax, just specify the extension; the extension must be either `sublime-syntax` or `tmLanguage`.

```js
"syntax": "Rails/Language/Ruby Haml.tmLanguage"
```

If it is desirable for the syntax rule to reference multiple tmLanguage files because it is not known which package will be on a machine, you can set the syntax as an array of syntaxes as shown in the following example.  The first one found will be used.

```js
"syntax": ["RSpec/RSpec", "RSpec (snippets and syntax)/Syntaxes/RSpec"]
```

Notice that each syntax file has a different path since they come from completely different plugins.

Lastly, if using Package Control, it is likely that most, if not all, of your packages will be zipped with the extension `.sublime-package` in the `Installed Packages` folder instead of `Packages`.  These will be handled exactly like plugins installed under `Packages`.  The one difference is that you treat the zip bundle as a folder without the `.sublime-package` extension.  So if we had a syntax file located in a zipped bundle: `Installed Packages/Rails.sublime-package/Language/Ruby Haml.tmLanguage` --> `Rails/Language/Ruby Haml`.

```js
"syntax": "Rails/Language/Ruby Haml"
```

### Extensions

The `extensions` attribute is used to define extensions to apply a syntax to.  `extensions` is an array of strings where each string is an extension.  No `.` is needed when defining extensions, unless it is desired to target a dot file like `.gitignore`, then you would include the `.`.

```js
    {
        "syntax": "YAML/YAML",
        "extensions": [".gemrc", "yml", "yml.dist"]
    },
```

`extensions` is evaluated before all other rules, and it never takes part in "[match all](#match)" rule sets as it is run separate from the normal rule sets; if an extension is matched here, all other rules will be skipped.

An added benefit of `extensions`, if you are using ST3 and set [`add_exts_to_lang_settings`](#add-extensions-to-language-settings) to `true`, is that ApplySyntax will add the extensions to the specified syntax language's settings file in your `User` folder.  By doing this, Sublime Text will be able to show the associated icon for the file type in the sidebar.  Apply syntax will also create a file `ApplySyntax.ext-list` in your `User` folder and track which extension it added so that if you remove a rule, ApplySyntax will only remove the extensions it added to the language file in question. If you do not like this functionality, you can simply disable `add_exts_to_lang_settings` by setting it to `false`.

!!! note "Note"
    `add_exts_to_lang_settings` will not be applied to `extensions` found in a [project specific rule](#project-specific-rules), as project specific rules are not global, but the effects of `add_exts_to_lang_settings` are global.

### Match

`match` is a setting that you either include or omit.  When included, you set it to `all`.  When set, all rules defined must be met for a match to be considered successful.  `match` ignores the [`extensions`](#extensions) key as `extensions` never take part in "match all" rule sets.  If you want to include an extension rule in a "match all" rule set, then a [`file_path`](#file-path-rule) rule should be used.

```js
    "match": "all"
```

So in this case, all the rules must match for the syntax to be applied:

```js
     "syntax": "Handlebars/Handlebars",
     "match": "all",
     "rules": [
         {"file_path": ".*\\.html$"},
         {"contains": "<script [^>]*type=\"text\\/x-handlebars\"[^>]*>"}
     ]
```

In this case, there is no `match` key, so only one rule needs to match:

```js
    {
        "syntax": "Ruby/Ruby",
        "rules": [
            {"file_path": ".*(\\\\|/)Gemfile$"},
            {"file_path": ".*(\\\\|/)Capfile$"},
            {"file_path": ".*(\\\\|/)Guardfile$"},
            {"file_path": ".*(\\\\|/)[Rr]akefile$"},
            {"file_path": ".*(\\\\|/)Berksfile$"},
            {"file_path": ".*(\\\\|/)[Cc]heffile$"},
            {"file_path": ".*(\\\\|/)Thorfile$"},
            {"file_path": ".*(\\\\|/)Podfile$"},
            {"file_path": ".*(\\\\|/)config.ru$"},
            {"file_path": ".*\\\\Vagrantfile(\\\\..*)?$"},
            {"file_path": ".*/Vagrantfile(/..*)?$"},
            {"file_path": ".*\\.thor$"},
            {"file_path": ".*\\.rake$"},
            {"file_path": ".*\\.simplecov$"},
            {"file_path": ".*\\.jbuilder$"},
            {"file_path": ".*\\.rb$"},
            {"file_path": ".*\\.podspec$"},
            {"file_path": ".*\\.rabl$"},
            {"interpreter": "ruby"}
        ]
    },
```

### Rules

`rules` is an array of rules that can be used to target specific files with your defined syntax file.  The rules are
processed until the first rule matches, so order your rules in a way that makes sense to you.

#### Globmatch Rule

A `globmatch` rule defines a glob pattern to match a file path against. Regex is more powerful, but often, a glob
pattern can be far less cumbersome and easier to specify patterns that work cross platform.

ApplySyntax uses the [`wcmatch`](https://github.com/facelessuser/wcmatch) library with the following flags enabled:

- `GLOBSTAR`: Allows you to match 0 or more directories with `**`.
- `BRACE`: Allows you to use Bash style brace expansions for patterns (`a{b,c}` --> `ab ac`).
- `EXTGLOB`: Allows you to use extended glob patterns such as `@(file1|file2)`, etc.
- `NEGATE`: Allows you to use exclusion patterns that filter inclusion patterns (`#!py3 ['**/*.py', '!**/bad.py']`).
- `DOTGLOB`: Allows `*` and other such patterns to match file names that start with `.`.

`globmatch` rule takes either a string pattern or list of strings patterns. You do not have to specify Windows paths
with `\\`, just use `/`.

```js
{"globmatch": "**/*.py"}
````

When providing a list, all patterns are evaluated together. This allows you to apply excludes:

```js
{"globmatch": ["**/*.py", "!**/bad.py"]}
````

If necessary, you can specify case sensitivity:

```js
{"globmatch": "**/*.py", "case": true}
````

#### File Path Rule

A `file_path` rule defines a regex to match against the complete file path. The pattern is always anchored to the beginning of the path, as if there were an implicit `^` — so the pattern `/a/b/c` will match the file `/a/b/c/foo.py`, but not the file `/x/y/z/a/b/c/foo.py`. (You may include an explicit `^` at the beginning of the pattern, as some of the default rules do — but the result is the same either way.)

For backwards compatibility with older versions of ApplySyntax, the rule name `file_name` is also accepted, and functions exactly like `file_path`.

```js
{"file_path": ".*\\.xml(\\.dist)?$"},
```

#### First Line Rule

A `first_line` rule allows you to check whether the first line of the file's content matches a given regex. As with `file_path` [rules](#file-path-rule), the pattern is always anchored to the beginning of the line.

```js
{"first_line": "^<\\?xml"},
```

#### Interpreter (Shebang)

An `interpreter` rule does the same thing as a `first_line` rule that uses a regex to match an interpreter directive (shebang).  The difference being that ApplySyntax will construct the regex for you.

So a `first_line` rule:

```js
{"first_line": "^#\\!(?:.+)ruby"}
```

Can be simplified as:

```js
{"interpreter": "ruby"}
```

For backwards compatibility with older versions of ApplySyntax, the rule name `binary` is also accepted, and functions exactly like `interpreter`.

#### Function Rule

This is an example of using a custom function to decide whether or not to apply a syntax. This is done via ApplySyntax plugins.  The plugin file should be under a plugin folder.

The function rule takes two parameters.  The first is `source` and is the plugin source file.  It is defined as if you were importing a python plugin.  If you had a plugin in `Packages/ApplySyntax/as_plugins/is_rails_file.py`, it would be defined under `source` as `ApplySyntax.as_plugins.is_rails_file`.  Function rules still support the legacy way: `ApplySyntax/as_plugins/is_rails_file`, but it is recommended to use the dot notation as it makes more sense from a Python import perspective.

The second parameter is `args` and is optional. `args` is a dictionary of the keyword arguments the function rule plugin accepts.

The plugin must have a function defined as `syntax_test`. `syntax_test` will be the function called within the plugin file and accepts an argument `file_path` (which is the full path to the file being evaluated), and any custom keyword arguments desired by the user.  The plugin must return either `True` or `False`.


```js
{"function": {"source": "User.plugins.myplugin", "args": {'foo': "bar"}}}
```

Example:

```py3
def syntax_test(file_path, foo):
    # Some test logic
    return False # True or False
```

!!! tip "Tip"
    When placing a function rule module in a package, it is advised to put it in a sub-folder.  The sub-folder does not need an `__init__.py`, it just needs your module(s).

#### Content Rule

Sometimes a file name or first line search is just not enough and maybe a function rule is overkill.  In this case, maybe searching the content of a file can be enough.  You can search a file's content with regex for a specific token via the `contains` rule.

```js
{"contains": "<script [^>]*type=\"text\\/x-handlebars\"[^>]*>"}
```

!!! tip "Tip"
    It is recommended to pair `contains` rules with other rules via the `#!js "match": "all"` option to ensure you don't search every file (which can significantly slow down the editor); this will also help ensure get more reliable matches. If pairing with other rules as dependencies, it is advised to pair the `contains` rule after the other required rule(s) to ensure you search the content of as few files as possible.

    Also, try to use very specific regex to ensure you don't get false positives.

### Extension Trimming

Sometimes a file may have a trailing extension that prevents it from matching a rule, but if it was trimmed off, it would match. By creating an extension trimming rule, you target files that do not initial match and send them back through the pipe without it's last extension.

Currently, an extension trimming rule only contains a `file_path` pattern.

```js
"ext_trim": [{"file_path": ".*\\.py3\\.temp"}]
```

So, if we had a file named `test.py3.temp`, it normally wouldn't match one of default rules. With the above rule, the file would be retried as `test.py3` and would match the Python syntax rule.

### Project Specific Rules

To define project specific syntaxes, just create a `settings` key in your project file (if it doesn't already exist) and then and an additional key under `settings` called `project_syntaxes` or `project_ext_trim`.

`project_syntaxes` is an array; just add your syntax rules to `project_syntaxes` just like you would add them to `syntaxes` in your user settings file, and ApplySyntax will prepend the rules to the beginning of your defined rules.  The order of rules is as follows: project --> user --> default.

`project_ext_trim` is also an array, and you can trim rules just as you would to `ext_trim` in your user settings file.

There is one difference between project specific rules and global rules.  In project rules, the [extensions](#extensions) key will not be applied to the associated syntax language settings file as project specific rules are not global, but language settings files are global.

```js
    "settings": {
        "project_syntaxes": [
            {
                "syntax": "XML/XML",
                "rules": [
                    {"file_path": ".*\\.xml(\\.dist)?$"},
                    {"first_line": "^<\\?xml"}
                ]
            }
        ],
        "project_ext_trim": [
            {"file_path": ".*\\.file.temp"}
        ]
    }
```

### Settings Options

There are a couple of general settings found in `ApplySyntax.sublime-settings`.

#### Re-Raise Exceptions

If an exception occurs when processing a function, this will re-raised the captured exception in Sublime's console so the user get feedback. This is really only useful to those writing functions. The average user shouldn't need this.  By default, the setting will be set to `false`.

```js
    "reraise_exceptions": false,
```

#### New File Syntax

If you want to have a syntax applied when new files are created, set `new_file_syntax` to the name of the syntax to use. The format is exactly the same as the [syntax](#syntax) parameter in the syntax rules mentioned earlier. For example, if you want to have a new file use JavaScript syntax, set `new_file_syntax` to `JavaScript/JavaScript`.  The default is `false`.

```js
    "new_file_syntax": "JavaScript/JavaScript",
```

#### Add Extensions to Language Settings

To enable adding defined extensions to language settings, just set `add_exts_to_lang_settings` to `true`.  See [Extensions](#extensions) for more info.

```js
    "add_exts_to_lang_settings": true,
```

#### Troubleshooting and Debugging

By default, the `debug` setting is turned on so that users have some form of visual feedback in the console that ApplySyntax is working.  This can be turned off by setting `debug` to `false`.  If developing, you can set `debug` to `verbose` to get even more info in the console.

```js
    // Control level of logging in the console.
    // (true|false|"verbose")
    "debug": true,
```

--8<-- "refs.md"
