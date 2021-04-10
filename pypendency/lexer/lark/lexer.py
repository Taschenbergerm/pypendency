from typing import List

from pypendency.models.generics import Relation
from pypendency.models.generics import BaseNode
from .core import Lexer
from .transformer import Transformer


class RelationLexer(object):
    def __init__(
        self, lexer: Lexer = Lexer(), transformer: Transformer = Transformer()
    ):
        self.lexer = lexer
        self.transformer = transformer

    def set_nodes(self, nodes: List[BaseNode]):
            self.transformer.set_nodes(nodes)

    def lex(self, raw_relations: List[str]) -> List[Relation]:
        relations = []
        for raw_relation in raw_relations:
            tokenized_relation = self.lexer.parse(raw_relation)
            for token in tokenized_relation:
                relation = self.transformer.create_relations_from_raw_relation(token)
                relations.extend(relation)
        return relations
