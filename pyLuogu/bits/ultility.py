__all__ = [
    "make_list",
    "exist"
]

from .typing import *
from collections.abc import Iterable


def make_list(val: Any) -> list:
    if isinstance(val, list):
        return list(val)
    else:
        return [val]


def exist(_list: Iterable, _f: filter_of(Any)):
    for val in _list:
        if _f(val):
            return True
    return False
