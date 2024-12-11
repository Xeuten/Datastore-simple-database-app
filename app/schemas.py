from dataclasses import dataclass
from enum import StrEnum, auto
from typing import Optional


@dataclass
class Variable:
    name: str
    value: Optional[str] = None

    def __str__(self):
        return f"{self.name} = {self.value}"


class StackType(StrEnum):
    UNDO = auto()
    REDO = auto()
