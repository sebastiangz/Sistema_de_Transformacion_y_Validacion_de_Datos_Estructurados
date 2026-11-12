"""Esquemas declarativos e inmutables."""
from dataclasses import dataclass

@dataclass(frozen=True)
class Field:
    kind: type
    required: bool = True
    minimum: int | None = None
    maximum: int | None = None
    email: bool = False

USER_SCHEMA = {
    'name': Field(str),
    'email': Field(str, email=True),
    'age': Field(int, minimum=18, maximum=120),
    'tags': Field(list, required=False),
}
