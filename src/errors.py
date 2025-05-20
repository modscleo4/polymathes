from typing import Any, Self, Optional


class ValidationError(Exception):
    def __init__(self, message: str, field_name: str, value: Any, base_ex: Optional[Self] = None) -> None:
        super().__init__(message)
        self.field_name = field_name
        self.value = value
        self.base_ex = base_ex

    def get_full_field_name(self) -> str:
        return str(self.field_name) + ("." + self.base_ex.get_full_field_name() if self.base_ex else "")

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}: {self}"


class UnexpectedTypeError(ValidationError):
    def __init__(self, field_name: str, field_type: type, value: Any, base_ex: Optional[Self] = None) -> None:
        super().__init__(f"Expected {field_type}", field_name, value, base_ex)
        self.field_type = field_type

    def __repr__(self) -> str:
        return super().__repr__() + f"\n'{self.get_full_field_name()}': {self.value}"


class RequiredFieldError(ValidationError):
    def __init__(self, field_name: str, field_type: type, base_ex: Optional[Self] = None) -> None:
        super().__init__(f"Field '{field_name}': {field_type} is required", field_name, None, base_ex)
        self.field_type = field_type
