__all__ = [
    "make_list",
    "JsonSerializable",
    "Printable"
]

import json

from .strings import str_type_of, str_val, decorating, str_type


def make_list(val) -> list:
    if isinstance(val, list):
        return list(val)
    else:
        return [val]


class JsonSerializable:
    __type_dict__ = {}  # 子类应定义属性名与类型的映射

    def __init__(self, json=None):
        if json is None:
            json = {}
        self.parse(json)

    def parse(self, json):
        """
        初始化对象，将 JSON 数据映射到对象属性
        """

        def handle_nested_type(_key, _value, _expected_type):
            """
            处理嵌套类型的转换
            """
            if _value is None:
                return None

            if isinstance(_expected_type, list):
                if len(_expected_type) != 1:
                    raise TypeError(f"List type must have exactly one element type: {_expected_type}")
                inner_type = _expected_type[0]
                if not isinstance(_value, list):
                    raise TypeError(f"Expected a list of {inner_type}, got {type(_value)}")
                return [handle_nested_type(None, v, inner_type) for v in _value]

            elif isinstance(_expected_type, tuple):
                if not isinstance(_value, (list, tuple)) or len(_value) != len(_expected_type):
                    raise TypeError(f"Expected a tuple of {_expected_type}, got {type(_value)} with value {_value}")
                return tuple(handle_nested_type(None, v, t) for v, t in zip(_value, _expected_type))

            elif isinstance(_expected_type, dict):
                if not isinstance(_value, dict):
                    raise TypeError(f"Expected a dict of {_expected_type}, got {type(_value)}")

            elif issubclass(_expected_type, JsonSerializable):
                return _expected_type(json=_value)

            elif not isinstance(_value, _expected_type):
                raise TypeError(f"{_key} Expected {_expected_type}, got {type(_value)}")

            return _value

        if not isinstance(json, dict):
            raise TypeError(f"Expected a dictionary, got {type(json)}")

        for key, value in json.items():
            expected_type = self.__type_dict__.get(key)

            if expected_type is None:
                continue

            if value is not None:
                value = handle_nested_type(key, value, expected_type)

            setattr(self, key, value)

        for key, expected_type in self.__type_dict__.items():
            if not hasattr(self, key):
                setattr(self, key, None)  # 默认值为 None

    def to_json(self):
        """
        转换对象为 JSON 格式（字典）
        """

        def serialize(_value):
            if isinstance(_value, JsonSerializable):
                return _value.to_json()  # 递归处理嵌套对象
            elif isinstance(_value, list):
                return [serialize(v) for v in _value]  # 递归处理列表
            elif isinstance(_value, tuple):
                return [serialize(v) for v in _value]  # 元组转换为列表
            elif isinstance(_value, dict):
                return {k: serialize(v) for k, v in _value.items()}  # 递归处理字典
            else:
                return _value

        json_data = {}
        for key, value in self.__type_dict__.items():
            attr_value = getattr(self, key, None)
            if attr_value is None:
                continue
            json_data[key] = serialize(attr_value)

        return json_data

    @classmethod
    def from_file(cls, path: str):
        with open(path, 'r') as json_file:
            data = json.load(json_file)

        return cls(json=data)

    def store(self, path: str):
        with open(path, 'w') as json_file:
            json_file.write(json.dumps(self.to_json()))


class Printable:
    __type_dict__ = {}

    def __tree__(self, offset=""):
        s = ""
        for x, y in self.__dict__.items():
            tail = "├─ " if x != list(self.__dict__.keys())[-1] else "└─ "
            addi = "│  " if x != list(self.__dict__.keys())[-1] else "   "
            if y is None:
                s += offset + tail + f"{str_type(self.__type_dict__[x])} {x}: {decorating("None", 31)}\n"
            elif isinstance(y, list):
                s += offset + tail + f"{str_type_of(y)} {x}:\n"
                new_offset = offset + addi
                for p in range(len(y)):
                    tail = "├─ " if p != len(y) - 1 else "└─ "
                    addi = "│  " if p != len(y) - 1 else "   "
                    if isinstance(y[p], Printable):
                        s += new_offset + tail + f"{x}[{p}] -> {str_type_of(y[p])} :\n" + y[p].__tree__(
                            new_offset + addi)
                    else:
                        s += new_offset + tail + f"{x}[{p}] -> {str_type_of(y[p])} : {str_val(y[p])}\n"
            elif isinstance(y, Printable):
                s += offset + tail + f"{str_type_of(y)} {x} :\n" + y.__tree__(offset + addi)
            else:
                s += offset + tail + f"{str_type_of(y)} {x} : {str_val(y)}\n"
        return s

    def __str__(self):
        return decorating(str_type_of(self) + "\n" + self.__tree__(), 37, 0)