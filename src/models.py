from types import GenericAlias, UnionType
from typing import Any, Iterable, List, Optional, get_origin

from errors import ValidationError, UnexpectedTypeError, RequiredFieldError


class BaseModel:
    def __init__(self, /, **kwargs) -> None:
        for field_name, field_type in self.__annotations__.items():
            if field_name not in kwargs:
                raise RequiredFieldError(field_name, field_type, None)

            setattr(self, field_name, self.__parse_field(field_name, field_type, kwargs.get(field_name)))

    def keys(self) -> Iterable[str]:
        return self.__annotations__.keys()

    def __getitem__(self, key: str) -> Any:
        return getattr(self, key)

    @staticmethod
    def __is_instance_strict(value: Any, cls: type) -> bool:
        # https://www.python.org/dev/peps/pep-0285/
        if cls in (int, float) and type(value) is bool:
            return False

        return isinstance(value, cls)

    def __parse_field(
        self,
        field_name: int | str,
        field_type: Optional[type],
        value: Any,
        strict: bool = False,
    ) -> Any:
        if field_type is None:
            field_type = type(None)

        try:
            if get_origin(field_type) is list:
                return self.__parse_list(field_name, field_type, value)

            if get_origin(field_type) is tuple:
                return self.__parse_tuple(field_name, field_type, value)

            if isinstance(field_type, UnionType):
                return self.__parse_union(field_name, field_type, value)

            if issubclass(field_type, BaseModel):
                return field_type(**value)

            if strict and not self.__is_instance_strict(value, field_type):
                raise TypeError()

            return self.__coerce(field_type, value)
        except TypeError:
            raise UnexpectedTypeError(field_name, field_type, value)
        except ValueError:
            raise UnexpectedTypeError(field_name, field_type, value)
        except ValidationError as ex:
            raise ValidationError(ex.args[0], field_name, ex.value, ex)

    def __parse_union(self, field_name: int | str, field_type: UnionType, value: Any) -> Any:
        for field_type_option in field_type.__args__:
            try:
                return self.__parse_field(field_name, field_type_option, value, strict=True)
            except ValidationError:
                continue

        raise UnexpectedTypeError(field_name, field_type, value)

    def __parse_list(self, field_name: int | str, field_type: GenericAlias, value: Any) -> List[Any]:
        if not isinstance(value, list):
            raise UnexpectedTypeError(field_name, field_type, value)

        return [self.__parse_field(index, field_type.__args__[0], item) for index, item in enumerate(value)]

    def __parse_tuple(self, field_name: int | str, field_type: GenericAlias, value: Any) -> Any:
        if not isinstance(value, tuple):
            raise UnexpectedTypeError(field_name, field_type, value)

        return tuple(
            self.__parse_field(i, t, v) for i, t, v in zip(range(len(value)), field_type.__args__, value, strict=True)
        )

    @staticmethod
    def __coerce(field_type: type, value: Any) -> Any:
        if isinstance(value, field_type):
            if field_type is type(None):
                return value

            return field_type(value)

        if value is None and field_type is not type(None):
            raise ValueError()

        if issubclass(field_type, str):
            if isinstance(value, bool):
                return str(value).lower()

            if isinstance(value, str) or isinstance(value, int) or isinstance(value, float):
                return str(value)

            if isinstance(value, bytes):
                return value.decode()

            raise ValueError()
        elif issubclass(field_type, int):
            return int(value)
        elif issubclass(field_type, float):
            return float(value)
        elif issubclass(field_type, bool):
            if isinstance(value, str):
                value = value.lower()
                if value == "true" or value == "1" or value == "1.0":
                    return True
                elif value == "false" or value == "0" or value == "0.0":
                    return False
            elif isinstance(value, int):
                if value == 1:
                    return True
                elif value == 0:
                    return False
            elif isinstance(value, float):
                if value == 1.0:
                    return True
                elif value == 0.0:
                    return False

            raise ValueError()
        elif issubclass(field_type, type(None)):
            raise ValueError()

        return field_type(value)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({', '.join([f'{field_name}={repr(self[field_name])}' for field_name in self.keys()])})"
