import mmap
import os


def using_jquery(file_name):
    name, extension = os.path.splitext(file_name)

    if extension != '.js':
        return False

    jquery_idioms = [
        '$(function',
        '$(document)',
        '$(window)',
        '$(this)'
        '$.fn',
        '$.ajax',
        '$.noConflict',
        'jQuery.noConflict'
    ]

    is_using = False

    with open(file_name, 'r') as f:
        try:
            content = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
            is_using = any(content.find(idiom) >= 0 for idiom in jquery_idioms)
            content.close()
        except mmap.error:
            pass

    return is_using