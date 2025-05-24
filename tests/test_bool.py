import pytest

from polymathes.errors import ValidationError
from polymathes.models import BaseModel


class SampleModel(BaseModel):
    value: bool


def test_value_str() -> None:
    with pytest.raises(ValidationError):
        SampleModel(value="")

    assert SampleModel(value="1").value is True
    assert SampleModel(value="true").value is True


def test_value_int() -> None:
    assert SampleModel(value=1).value is True
    assert SampleModel(value=0).value is False


def test_value_float() -> None:
    assert SampleModel(value=1.0).value is True
    assert SampleModel(value=0.0).value is False


def test_value_bool() -> None:
    assert SampleModel(value=True).value is True
    assert SampleModel(value=False).value is False


def test_value_bytes() -> None:
    with pytest.raises(ValidationError):
        SampleModel(value=b"a")

    assert SampleModel(value=b"1").value is True
    assert SampleModel(value=b"0").value is False


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
