import pytest

from errors import ValidationError
from models import BaseModel


class SampleModel(BaseModel):
    value: str


def test_value_str() -> None:
    assert SampleModel(value="").value == ""


def test_value_int() -> None:
    assert SampleModel(value=1).value == "1"


def test_value_float() -> None:
    assert SampleModel(value=1.0).value == "1.0"


def test_value_bool() -> None:
    assert SampleModel(value=True).value == "true"
    assert SampleModel(value=False).value == "false"


def test_value_bytes() -> None:
    assert SampleModel(value=b"a").value == "a"


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
