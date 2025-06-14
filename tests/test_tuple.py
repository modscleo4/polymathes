import pytest

from polymathes.errors import ValidationError
from polymathes.models import BaseModel


class SampleModel(BaseModel):
    value: tuple[int, float, str]


class SampleEllipsisModel(BaseModel):
    value: tuple[int, ...]


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
    with pytest.raises(ValidationError):
        SampleModel(value=[1, 2, 3])


def test_value_tuple() -> None:
    assert SampleModel(value=(1, 2, 3)).value == (1, 2.0, "3")


def test_value_tuple_wrong() -> None:
    with pytest.raises(ValidationError):
        SampleModel(value=(1, 2, 3, 4))


def test_value_tuple_ellipsis() -> None:
    assert SampleEllipsisModel(value=(1,)).value == (1,)
    assert SampleEllipsisModel(value=(1, 2)).value == (1, 2)
    assert SampleEllipsisModel(value=(1, 2, 3)).value == (1, 2, 3)


def test_value_tuple_ellipsis_wrong() -> None:
    with pytest.raises(ValidationError):
        SampleEllipsisModel(value=("a",))


def test_value_dict() -> None:
    with pytest.raises(ValidationError):
        SampleModel(value={"a": 1, "b": 2, "c": 3})
