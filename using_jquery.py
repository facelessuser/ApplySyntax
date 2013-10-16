import mmap
import os
import re


def using_jquery(file_name):
    name, extension = os.path.splitext(file_name)

    if extension != '.js':
        return False

    jquery_patterns = re.compile(
        r"""
            (?:\$ | jQuery)(
                \(function      |
                \(document\)    |
                \(window\)      |
                \(this\)        |
                \.fn            |
                \.ajax          |
                \.noConflict
            )
        """,
        re.VERBOSE
    )

    is_using = False

    with open(file_name, 'r') as f:
        try:
            content = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
            is_using = re.search(jquery_patterns, content)
            content.close()
        except mmap.error:
            pass

    return is_using
