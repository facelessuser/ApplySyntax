"""Test if rails file."""
import os
import re
import platform


def syntax_test(file_path):
    """Check file location and name to determine if a rails file."""

    windows = platform.system() == "Windows"

    is_unc = windows and file_path.startswith("\\\\")

    if is_unc:
        unc_drive, path = os.path.splitunc(file_path)
    else:
        path = os.path.dirname(file_path)

    file_name = os.path.basename(file_path).lower()
    name, extension = os.path.splitext(file_name)

    result = False

    # I doubt this is the most elegant way of identifying a Rails directory structure,
    # but it does work. The idea here is to work up the tree, checking at each level for
    # the existence of config/routes.rb. If it's found, the assumption is made that it's
    # a Rails app.
    while path != '':
        if is_unc:
            if os.path.exists(os.path.join(unc_drive, path, 'config', 'routes.rb')):
                result = True
                break
            elif path == '\\':
                path = ''
            else:
                path = os.path.dirname(path)
        else:
            if os.path.exists(os.path.join(path, 'config', 'routes.rb')):
                result = True
                break
            elif windows and re.match(r"^([A-Za-z]{1}:)\\$", path) is not None:
                path = ''
            elif not windows and path == '/':
                path = ''
            else:
                path = os.path.dirname(path)

    return extension in ['.rb', '.rake'] and result
