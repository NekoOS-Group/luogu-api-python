"""
  # Definition
  #
  #     Expression                       Meaning
  #     --------------------------------------------------------------------------------------
  #     T                                type T
  #     [T]                              array of T
  #     [T1,T2,...,Tn]                   type T1 or T2 or ... or Tn
  #     (T1,T2,...,Tn)                   tuples that ith type is Ti
  #     {V1:T1,...Vn:Tn}                 dicts that type of data for key Vi is Ti
  #
  # Example
  #
  #     [[int]]                          array of int array, such as [[1,2],[3,4]]
  #     [[int, str]]                     array of Union[int, str], such as [1,'qwq',0,'qaq']
  #     (int, str, bool)                 tuples like (1, 'qwq', True)
  #     {'id': int, 'name': 'str'}       dicts like {'id': 19260817, 'name': 'haha'}
  #
"""

from typing import Any, Type, Callable, Union, Optional, Literal, List, NoReturn, TypeVar, ParamSpec, TypeAlias


def single_or_list_of(_type: type) -> TypeAlias:
    return Union[type, list[type]]


def filter_of(_type: type) -> TypeAlias:
    return Callable[[type], bool]


def handler_of(_type: type) -> TypeAlias:
    return Callable[[type], NoReturn]


T = TypeVar('T')
P = ParamSpec('P')


def isType(_type) -> bool:
    if type(_type) == type:
        return True
    flag = True

    if type(_type) == dict:
        if len(_type) == 0:
            flag = False
        for k, v in _type.items():
            if type(k) != str:
                flag = False
            flag &= isType(v)

    if type(_type) in [list, tuple]:
        if len(_type) == 0:
            flag = False
        for v in _type:
            flag &= isType(v)

    return flag


def isTypeof(val: Any, _type) -> bool:
    if not isType(_type):
        raise Exception("Invalid type")

    pass


def typeOf(val: Any):
    pass


def translate(val: Any, _type):
    if not isTypeof(val, _type):
        raise Exception("Type mismatch")

    pass
