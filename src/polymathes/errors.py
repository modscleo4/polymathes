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

from typing import Any, Self


class ValidationError(Exception):
    """
    Represents a validation error.
    """

    def __init__(
        self,
        message: str,
        field_name: str,
        value: Any,
        base_ex: Self | None = None,
    ) -> None:
        """

        :param message: The error message.
        :param field_name: The name of the field.
        :param value: The value of the field.
        :param base_ex: The base exception.
        """
        super().__init__(message)
        self.field_name = field_name
        self.value = value
        self.base_ex = base_ex

    def get_full_field_name(self) -> str:
        return str(self.field_name) + ("." + self.base_ex.get_full_field_name() if self.base_ex else "")

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}: {self}"


class UnexpectedTypeError(ValidationError):
    """
    Raised when a field has an unexpected type.
    """

    def __init__(
        self,
        field_name: str,
        field_type: type,
        value: Any,
        base_ex: Self | None = None,
    ) -> None:
        super().__init__(f"Expected {field_type}, got {type(value)}", field_name, value, base_ex)
        self.field_type = field_type

    def __repr__(self) -> str:
        return super().__repr__() + f"\n'{self.get_full_field_name()}': {self.value}"


class RequiredFieldError(ValidationError):
    """
    Raised when a required field is missing.
    """

    def __init__(
        self,
        field_name: str,
        field_type: type,
        base_ex: Self | None = None,
    ) -> None:
        super().__init__(f"Field '{field_name}': {field_type} is required", field_name, None, base_ex)
        self.field_type = field_type
