import pytest

from polymathes.errors import ValidationError
from polymathes.models import BaseModel


class SampleModel(BaseModel):
    value: int


def test_value_str() -> None:
    with pytest.raises(ValidationError):
        SampleModel(value="")

    assert SampleModel(value="1").value == 1


def test_value_int() -> None:
    assert SampleModel(value=1).value == 1


def test_value_float() -> None:
    assert SampleModel(value=1.0).value == 1


def test_value_bool() -> None:
    assert SampleModel(value=True).value == 1
    assert SampleModel(value=False).value == 0


def test_value_bytes() -> None:
    with pytest.raises(ValidationError):
        SampleModel(value=b"a")

    assert SampleModel(value=b"1").value == 1


def test_value_none() -> None:
    with pytest.raises(ValidationError):
        SampleModel(value=None)


def test_value_list() -> None:
    with pytest.raises(ValidationError):
        SampleModel(value=[1, 2, 3])


def test_value_tuple() -> None:
    with pytest.raises(ValidationError):
        SampleModel(value=(1, 2, 3))


def test_value_dict() -> None:
    with pytest.raises(ValidationError):
        SampleModel(value={"a": 1, "b": 2, "c": 3})
