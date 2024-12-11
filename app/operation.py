import json
from abc import ABC, abstractmethod
from dataclasses import asdict
from typing import Optional

from app.datastore_wrapper import Datastore
from app.schemas import Variable

client = Datastore("Variable")


class Operation(ABC):
    @abstractmethod
    def execute(self) -> Variable:
        pass

    @abstractmethod
    def undo(self) -> Variable:
        pass

    @abstractmethod
    def to_json(self) -> str:
        pass


class Set(Operation):
    def __init__(self, variable: Variable, prev_variable: Optional[Variable] = None):
        self._variable = variable
        self._prev_variable = prev_variable

    def execute(self) -> Variable:
        self._prev_variable = Variable(
            name=self._variable.name, value=client.get(self._variable.name)
        )
        client.put(self._variable.name, self._variable.value)
        return self._variable

    def undo(self) -> Variable:
        client.put(self._prev_variable.name, self._prev_variable.value)
        return self._prev_variable

    def to_json(self) -> str:
        return json.dumps(
            {
                "variable": asdict(self._variable),
                "prev_variable": asdict(self._prev_variable),
            }
        )


class Unset(Operation):
    def __init__(self, variable_name: str, prev_variable: Optional[Variable] = None):
        self._variable_name = variable_name
        self._prev_variable = prev_variable

    def execute(self) -> Variable:
        self._prev_variable = Variable(
            name=self._variable_name, value=client.get(self._variable_name)
        )
        client.delete(self._variable_name)
        return Variable(name=self._variable_name)

    def undo(self) -> Variable:
        client.put(self._prev_variable.name, self._prev_variable.value)
        return self._prev_variable

    def to_json(self) -> str:
        return json.dumps(
            {
                "variable_name": self._variable_name,
                "prev_variable": asdict(self._prev_variable),
            }
        )


def operation_from_json(json_str: str) -> Operation:
    data = json.loads(json_str)
    if "variable" in data:
       operation = Set(
           variable=Variable(
               name=data["variable"]["name"],
               value=data["variable"]["value"]
           ),
           prev_variable=Variable(
               name=data["prev_variable"]["name"],
               value=data["prev_variable"]["value"]
           ),
       )
    else:
        operation = Unset(
            variable_name=data["variable_name"],
            prev_variable=Variable(
                name=data["prev_variable"]["name"],
                value=data["prev_variable"]["value"]
            ),
        )
    return operation
