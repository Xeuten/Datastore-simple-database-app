import json
import uuid
from typing import Optional

from utils.datastore_wrapper import Datastore
from utils.operation import Operation, operation_from_json
from utils.schemas import StackType


class Stack:
    def __init__(self, stack_type: StackType):
        self._stack_type = stack_type
        self._client = Datastore(self._stack_type)

    def push(self, operation: Operation) -> None:
        current_top_key_value = Datastore.get_stack_top_key(self._stack_type)
        new_op_key = uuid.uuid4().hex
        new_op_data = {"data": operation.to_json(), "prev": current_top_key_value}
        self._client.put(new_op_key, json.dumps(new_op_data))
        Datastore.set_stack_top_key(self._stack_type, new_op_key)

    def pop(self) -> Optional[Operation]:
        current_top_key_value = Datastore.get_stack_top_key(self._stack_type)
        if current_top_key_value is None:
            return None

        top_op_str = self._client.get(current_top_key_value)
        if top_op_str is None:
            return None

        top_op_dict = json.loads(top_op_str)
        Datastore.set_stack_top_key(self._stack_type, top_op_dict["prev"])
        self._client.delete(current_top_key_value)
        return operation_from_json(top_op_dict["data"])

    def clear(self) -> None:
        Datastore.clear_stack(self._stack_type)
