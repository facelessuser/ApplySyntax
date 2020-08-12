# ApplySyntax 4.0.0

Changelog and support info command is now available in `Preferences->Package Settings->ApplySyntax`.

A restart after update may be required.

## New

- Rules can now use glob patterns instead of regular expression. See documentation for more information.

- Commands have been added to either browse existing syntax files so you can copy a properly formatted
  syntax path for rules to the clipboard, or grab the the syntax from the currently active view.

  In the past, users often thought that the name in the status bar was the proper name to use, but it
  is the syntax file name that must be used in syntax rules. Now we provide commands that make getting
  a properly formatted file path name easy.

## Breaking Changes

This is a major upgrade of ApplySyntax. While it includes new features, it also includes a breaking
change. While this may be a minor inconvenience in the short run, in the long run, it makes creating
patterns cross platform much easier:

- All file names are now normalized to `/` for regex matching, so regex patterns should no longer use
  `\` to specify path separators for Windows. Please update your patterns personal patterns to use `/`
  in the settings file instead of the double escaped backslashes (`\\\\`).
