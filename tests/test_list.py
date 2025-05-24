import pytest

from polymathes.errors import ValidationError
from polymathes.models import BaseModel


class SampleModel(BaseModel):
    value: list[str]


def test_value_str() -> None:
    with pytest.raises(ValidationError):
        SampleModel(value="")


def test_value_int() -> None:
    with pytest.raises(ValidationError):
        SampleModel(value=1)


def test_value_float() -> None:
    with pytest.raises(ValidationError):
        SampleModel(value=1.0)


def test_value_bool() -> None:
    with pytest.raises(ValidationError):
        SampleModel(value=True)


def test_value_bytes() -> None:
    with pytest.raises(ValidationError):
        SampleModel(value=b"a")


def test_value_none() -> None:
    with pytest.raises(ValidationError):
        SampleModel(value=None)


def test_value_list() -> None:
    assert SampleModel(value=[1, 2, 3]).value == ["1", "2", "3"]


def test_value_tuple() -> None:
    with pytest.raises(ValidationError):
        SampleModel(value=(1, 2, 3))


def test_value_dict() -> None:
    with pytest.raises(ValidationError):
        SampleModel(value={"a": 1, "b": 2, "c": 3})
