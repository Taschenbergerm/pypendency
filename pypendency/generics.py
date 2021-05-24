import abc
import dataclasses
from typing import List

from pypendency import Relation


class LexerInterface(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'lex') and
                callable(subclass.lex))

    def lex(self, raw_relations: List[str]) -> List[Relation]:
        raise NotImplementedError


class BackendInterface(metaclass=abc.ABCMeta):

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'compare') and
                callable(subclass.compare))


class TransformerInterface(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'attache_relations') and
                callable(subclass.attache_relations))


@dataclasses.dataclass(frozen=True)
class DialectInterface(metaclass=abc.ABCMeta):
    GRAPH_EXIST: str
    NODE_EXIST: str
    NODES_AND_RELATIONS: str
    ALL_NODES: str
    OWNED_NODES: str
    ALL_RELATIONS: str
    UPDATE_NODE: str
    DELETE_NODE: str
    DETACH_NODE: str
    CREATE_NODE: str
    MERGE_NODE: str
    MERGE_RELATION: str
