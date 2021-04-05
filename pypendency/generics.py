import abc
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
