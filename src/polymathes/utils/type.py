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

from typing import Any


def is_instance_strict(value: Any, cls: type) -> bool:
    # https://www.python.org/dev/peps/pep-0285/
    if cls in (int, float) and type(value) is bool:
        return False

    return isinstance(value, cls)


def coerce_to_str(value: Any) -> str:
    if isinstance(value, bool):
        return str(value).lower()

    if isinstance(value, str | int | float):
        return str(value)

    if isinstance(value, bytes):
        return value.decode()

    raise ValueError()


def coerce_to_bool(value: Any) -> bool:
    if isinstance(value, str):
        value = value.lower()
        if value == "true" or value == "1" or value == "1.0":
            return True
        elif value == "false" or value == "0" or value == "0.0":
            return False
    elif isinstance(value, bytes):
        if value == b"1":
            return True
        elif value == b"0":
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


def coerce(field_type: type, value: Any) -> Any:
    if isinstance(value, field_type):
        if field_type is type(None):
            return value

        return field_type(value)

    if value is None and field_type is not type(None):
        raise ValueError()

    if issubclass(field_type, str):
        return coerce_to_str(value)
    elif issubclass(field_type, bool):
        return coerce_to_bool(value)
    elif issubclass(field_type, int):
        return int(value)
    elif issubclass(field_type, float):
        return float(value)
    elif issubclass(field_type, type(None)):
        raise ValueError()

    return field_type(value)
