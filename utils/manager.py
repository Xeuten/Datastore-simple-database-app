from typing import Optional

from utils.operation import Operation
from utils.schemas import StackType, Variable
from utils.stack import Stack


class DatastoreManager:
    def __init__(self):
        self._undo_stack = Stack(StackType.UNDO)
        self._redo_stack = Stack(StackType.REDO)

    def execute(self, operation: Operation) -> Variable:
        variable = operation.execute()
        self._undo_stack.push(operation)
        self._redo_stack.clear()
        return variable

    def undo(self) -> Optional[Variable]:
        operation = self._undo_stack.pop()
        if operation is None:
            return None

        variable = operation.undo()
        self._redo_stack.push(operation)
        return variable

    def redo(self) -> Optional[Variable]:
        operation = self._redo_stack.pop()
        if operation is None:
            return None

        variable = operation.execute()
        self._undo_stack.push(operation)
        return variable
