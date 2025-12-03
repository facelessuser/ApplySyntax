# ApplySyntax

## 4.4.0

-   **NEW**: SSH config to rules.

## 4.3.2

-   **FIX**: Fix support commands.

## 4.3.1

-   **FIX**: Include `typing` dependency.

## 4.3.0

-   **NEW**: Update Zsh rules.

## 4.2.0

-   **NEW**: Add Dangerfile to Ruby patterns.

## 4.1.0

-   **NEW**: Ensure `Cartfile`s are recognized as Ruby files.
-   **NEW**: Migrate default patterns over to glob patterns from regex. If the intent of any patterns have changed in a
    negative way, please create an issue.

## 4.0.3

-   **FIX**: Recent versions of Sublime have the JSON syntax file in a new place.
-   **FIX**: Add `.babelrc` and `.stylelintrc` to JSON rule.
-   **FIX**: Reduce dependencies as they are all not required anymore.
-   **FIX**: Support dialog did not show all relevant dependencies.
-   **FIX**: New location for Ruby syntax files in later Sublime versions.

## 4.0.2

-   **FIX**: Fix `Gemfile.lock` being detected as Ruby on Rails. (#148)

## 4.0.1

-   **FIX**: "Browse Syntaxes" should show legacy `tmLanguage` files as well as the new `sublime-syntax`.

## 4.0.0

-   **NEW**: All file names are now normalized to `/`, so regex patterns should no longer use `\` to specify path
    separators for Windows. Please update your patterns personal patterns to use `/` in the settings file instead of the
    double escaped backslashes (`\\\\`). This applies to `file_path` rule patterns and `ext_trim` patterns.
-   **NEW**: Add new `globmatch` rule.
-   **NEW**: Add new `apply_syntax_browse` command in the command palette to browse all syntaxes. When one is selected,
    the syntax will be copied to the clipboard in a form compatible to be used in a syntax rule.
-   **NEW**: Add new `apply_syntax_current` command which will copy the current active view's syntax to the clipboard in
    a form compatible to be used in a syntax rule.

## 3.0.1

-   **FIX**: Avoid evaluating path if it is None.

## 3.0.0

-   **NEW**: Remove deprecations.
-   **NEW**: Add feature to allow configurable trimming of a file's extension and retry syntax detection if file path
    fails initial detection. (#132)

## 2.5.5

-   **FIX**: Fix check for unsaved buffer.

## 2.5.4

-   **FIX**: Fix extension compare and order of evaluation.

## 2.5.3

-   **FIX**: Use proper Bash syntax.
-   **FIX**: Use proper Git syntax. (!119)

## 2.5.2

-   **FIX**: Update shell scripts to use newest Bash language file.

## 2.5.1

-   **FIX**: Update `Rspec` rule with `RSpec Buddy/RSpec Buddy`.

## 2.5.0

-   **NEW**: Add document and settings command to command palette.
-   **FIX**: Handling of list syntax.

## 2.4.1

-   **FIX**: Fix usage of deprecated key name in default settings.

## 2.4.0

-   **NEW**: Added `TypoScript` rules.
-   **NEW**: Restrict phantoms to 3124+.
-   **NEW**: Support commands.

## 2.3.1

-   **FIX**: Configuration tweaks to YAML rules.

## 2.3.0

-   **NEW**: Added changelog command.
-   **NEW**: Added support command.
-   **FIX**: Fix issue where `new_file_syntax` would occasionally not work [#100](https://github.com/facelessuser/ApplySyntax/issues/100).
