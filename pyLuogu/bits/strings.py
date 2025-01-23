__all__ = [
    'decorating',
    'transfer',
    'str_type',
    'str_type_of',
    'str_val',
    'refresh_decorator'
]

import re
from typing import get_args, get_origin


def decorating(x: str, command: int | str = 30, default: int | str = '0;37') -> str:
    """Make string colorful

    Args:
        x: the string to be decorated
        command: CSI command at the beginning
        default: CSI command at the end

    Returns:
         decorated string
    """
    return f"\033[{str(command)}m{x}\033[{str(default)}m"


def refresh_decorator(x: str) -> str:
    """Remove ANSI escape sequences from a string"""
    return re.sub(r'\033\[[0-9;]*m', "", x)


def transfer(x: str) -> str:
    """Replace special characters with escape sequences

    Args:
        x: the input string

    Returns:
        translated string

    Examples:
        >>> print('1\\n1')
        1
        1
        >>> transfer('1\\n1')
        1\\n1
    """
    replacements = {
        '\n': '\\n',
        '\r': '\\r',
        '\t': '\\t'
    }
    for key, value in replacements.items():
        x = x.replace(key, decorating(value, 31, 33))
    return x


def str_type_of(x, origin: bool = False) -> str:
    """Detect the type of x and return a printable string

    Args:
        x: input data
        origin: not colored

    Returns:
        string of type of x
    """
    type_str = str(type(x)).split("'")[1]
    if x is None:
        return decorating("Unknown", 31)
    elif isinstance(x, list):
        return decorating(f"list[{len(x)}]", 34)
    elif isinstance(x, tuple):
        return decorating("(", 34) + ", ".join([str_type_of(v) for v in x]) + decorating(")", 34)
    elif isinstance(x, dict):
        k, v = list(x.items())[0]
        return decorating("map: ", 34) + str_type(type(k)) + " -> " + str_type(type(v))
    elif isinstance(x, (int, float, bool)):
        return decorating(type_str, 36)
    elif isinstance(x, str):
        return decorating(type_str, 33)
    elif isinstance(x, BaseException):
        return type_str
    else:
        type_str = type_str.split('.')[-1]
        if not origin:
            type_str = decorating(f"{type_str}<at {hex(id(x))}>", '30;47')
    return type_str


def str_type(t, origin: bool = False) -> str:
    """Return a string representation of the type t

    Args:
        t: input type
        origin: not colored

    Returns:
        string of type t
    """
    origin_type = type(t)
    
    if origin_type is list:
        return decorating(f"list<{str_type(t[0])}", 34) + decorating(f">", 34)
    elif origin_type is tuple:
        return decorating("tuple<", 34) + ", ".join([str_type(nt) for nt in t]) + decorating(">", 34)
    elif origin_type is dict:
        k, v = list(t.items())[0]
        return decorating("dict<", 34) + str_type(k) + " -> " + str_type(v) + decorating(">", 34)
    elif t in [int, float, bool]:
        return decorating(str(t).split("'")[1], 36)
    elif t is str:
        return decorating(str(t).split("'")[1], 33)
    else:
        type_str = str(t).split("'")[1].split('.')[-1]
    return type_str


def str_val(x, origin: bool = False) -> str:
    """Return a string representation of the value x

    Args:
        x: input object
        origin: not colored

    Returns:
        string format of x
    """
    if origin:
        return repr(x)
    s = str(x)
    if len(s) > 50:
        s = s[:50] + "..."
    if isinstance(x, str):
        s = decorating("'" + transfer(s) + "'", 33)
    return s
