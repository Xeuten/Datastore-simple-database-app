from typing import Optional

from google.cloud import datastore

from utils.schemas import StackType

client = datastore.Client()


class Datastore:
    def __init__(self, kind: str):
        self._kind = kind

    def get(self, name: str) -> Optional[str]:
        key = client.key(self._kind, name)
        entity = client.get(key) or {}
        return entity.get("value")

    def put(self, name: str, value: str) -> None:
        key = client.key(self._kind, name)
        entity = datastore.Entity(key=key)
        entity["value"] = value
        client.put(entity)

    def delete(self, name: str) -> None:
        key = client.key(self._kind, name)
        client.delete(key)

    @classmethod
    def get_stack_top_key(cls, stack_type: StackType) -> Optional[str]:
        key = client.key(f"{stack_type}_top")
        entity = client.get(key) or {}
        return entity.get("value")

    @classmethod
    def set_stack_top_key(cls, stack_type: StackType, value: str) -> None:
        key = client.key(f"{stack_type}_top")
        entity = datastore.Entity(key=key)
        entity["value"] = value
        client.put(entity)

    @classmethod
    def clear_stack(cls, stack_type: StackType) -> None:
        query = client.query(kind=stack_type)
        keys_to_delete = (entity.key for entity in query.fetch())
        client.delete_multi(keys_to_delete)

    @classmethod
    def clear_all(cls) -> None:
        query = client.query(kind="__kind__")
        keys_to_delete = (entity.key for entity in query.fetch())
        client.delete_multi(keys_to_delete)
