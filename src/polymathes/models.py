# Copyright 2025 Dhiego Cassiano Fogaça Barbosa
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from collections.abc import Iterable
from enum import Enum
from types import GenericAlias, UnionType
from typing import Any, get_origin

from polymathes.errors import RequiredFieldError, UnexpectedTypeError, ValidationError
from polymathes.utils.type import coerce, is_instance_strict


class BaseModel:
    """
    The base class for all models.

    All values are coerced to the specified type when possible.
    """

    def __init__(self, /, **kwargs) -> None:
        for field_name, field_type in self.__annotations__.items():
            if field_name not in kwargs and not hasattr(self, field_name):
                raise RequiredFieldError(field_name, field_type, None)

            setattr(self, field_name, self.__parse_field(field_name, field_type, kwargs.get(field_name)))

    def dump(self) -> dict:
        return {key: value for key, value in self.__dict__.items() if not key.startswith("_")}

    def keys(self) -> Iterable[str]:
        return self.__annotations__.keys()

    def __getitem__(self, key: str) -> Any:
        return getattr(self, key)

    def __parse_field(
        self,
        field_name: int | str,
        field_type: type | None,
        value: Any,
        strict: bool = False,
    ) -> Any:
        """
        Parses a field to the specified type.

        :param field_name: The name of the field.
        :param field_type: The required type of the field.
        :param value: The value of the field.
        :param strict: If the value should be coerced to the specified type or not.
        :return: The parsed value.
        """
        if field_type is None:
            field_type = type(None)

        try:
            if get_origin(field_type) is list:
                return self.__parse_list(field_name, field_type, value)

            if get_origin(field_type) is tuple:
                return self.__parse_tuple(field_name, field_type, value)

            if get_origin(field_type) is dict:
                return self.__parse_dict(field_name, field_type, value)

            if isinstance(field_type, UnionType):
                return self.__parse_union(field_name, field_type, value)

            if issubclass(field_type, Enum):
                return self.__parse_enum(field_name, field_type, value)

            if issubclass(field_type, BaseModel):
                return field_type(**value)

            if strict and not is_instance_strict(value, field_type):
                raise TypeError()

            return coerce(field_type, value)
        except TypeError:
            raise UnexpectedTypeError(field_name, field_type, value) from None
        except ValueError:
            raise UnexpectedTypeError(field_name, field_type, value) from None
        except ValidationError as ex:
            raise ValidationError(ex.args[0], field_name, ex.value, ex) from None

    def __parse_union(self, field_name: int | str, field_type: UnionType, value: Any) -> Any:
        for field_type_option in field_type.__args__:
            try:
                return self.__parse_field(field_name, field_type_option, value, strict=True)
            except ValidationError:
                continue

        raise UnexpectedTypeError(field_name, field_type, value)

    def __parse_list(self, field_name: int | str, field_type: GenericAlias, value: Any) -> list[Any]:
        if not isinstance(value, list):
            raise UnexpectedTypeError(field_name, field_type, value)

        return [self.__parse_field(index, field_type.__args__[0], item) for index, item in enumerate(value)]

    def __parse_tuple(self, field_name: int | str, field_type: GenericAlias, value: Any) -> Any:
        if not isinstance(value, tuple):
            raise UnexpectedTypeError(field_name, field_type, value)

        values_types = field_type.__args__
        if len(values_types) == 2 and values_types[1] is ...:
            values_types = (values_types[0],) * len(value)

        if len(value) != len(values_types):
            raise UnexpectedTypeError(field_name, field_type, value)

        return tuple(
            self.__parse_field(i, t, v) for i, t, v in zip(range(len(value)), values_types, value, strict=True)
        )

    def __parse_dict(self, field_name: int | str, field_type: GenericAlias, value: Any) -> Any:
        if not isinstance(value, dict):
            raise UnexpectedTypeError(field_name, field_type, value)

        key_type = field_type.__args__[0]
        value_type = field_type.__args__[1]

        return {
            self.__parse_field(key, key_type, key): self.__parse_field(value, value_type, value)
            for key, value in value.items()
        }

    def __parse_enum(self, field_name: int | str, field_type: type[Enum], value: Any) -> Any:
        if not isinstance(value, field_type):
            if hasattr(field_type, value):
                return field_type[value]

            raise UnexpectedTypeError(field_name, field_type, value)

        return value

    def __repr__(self) -> str:
        values = [f"{field_name}={repr(self[field_name])}" for field_name in self.keys()]

        return f"{self.__class__.__name__}({', '.join(values)})"
