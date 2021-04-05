from typing import List, Optional

import lark

import pypendency.models.graph
from pypendency.models import generics

from .models import RawRelation


class TransformerError(Exception):
    pass


class Transformer(object):
    def __init__(self, graph: Optional[pypendency.Graph] = None):
        self.graph = graph or None
        self.slug_map = {node.slug: node for node in graph.nodes} if graph else None

    def set_graph(self, graph: pypendency.Graph):
        self.graph = graph
        self.slug_map = {node.slug: node for node in graph.nodes}

    def attache_relations(self, raw_relations: List[RawRelation]):
        relations = self.create_relations_from_raw_relations(raw_relations)
        self.graph.attach_relations(relations)

    def create_relations_from_raw_relations(
        self, raw_relations: List[RawRelation]
    ) -> List[generics.Relation]:
        res = []
        for raw_relation in raw_relations:
            relations = self.create_relations_from_raw_relation(raw_relation)
            res.extend(relations)
        return res

    def create_relations_from_raw_relation(
        self, raw_relation: RawRelation
    ) -> List[generics.Relation]:
        from_node = raw_relation.from_node
        to_node = raw_relation.to_node
        edge = raw_relation.edge.data
        if edge == "to":
            direction = generics.Direction.Injective
        elif edge == "from":
            direction = generics.Direction.Injective
            from_node, to_node = to_node, from_node
        elif edge == "link":
            direction = generics.Direction.Link
        elif edge == "bijection":
            direction = generics.Direction.Bijection
        else:
            raise TransformerError(f"Direction  {edge} is unknown to transformer")

        relations = self.__create_relation(
            from_node, to_node, raw_relation.label, direction
        )
        return relations

    @staticmethod
    def _extract_tokens(tree: lark.tree.Tree):
        if tree.data == "node_group":
            res = [t.children[0] for t in tree.children]
        else:
            res = tree.children
        return res

    def __create_relation(
        self, from_nodes, to_nodes, label, direction
    ) -> List[generics.Relation]:
        relations = []
        for n1 in self._extract_tokens(from_nodes):
            for n2 in self._extract_tokens(to_nodes):

                relation = generics.Relation(
                    self.slug_map[n1], self.slug_map[n2], label, direction
                )
                relations.append(relation)

        return relations
