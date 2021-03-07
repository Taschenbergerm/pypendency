from typing import List, Union

import lark
from pypendency.lark.models import RawRelation


class Lexer(object):
    graph_grammar = '''
                    start: graph
                    graph : node_candidate (edge node_candidate)*
                    ?node_candidate: node
                            | node_group
                    node_group: "[" [node ("," node)*] "]"
                    node: STRING
                    edge: "-"STRING?">"  -> to
                        | "<"STRING?"-" -> from
                    STRING: /\w/+
                    %import common.WS
                    %ignore WS
                    %import common.WS_INLINE
                    %ignore WS_INLINE
    '''

    def __init__(self):
        self.lexer = lark.Lark(self.graph_grammar)

    def _parse(self, text: str) -> List[Union[str, lark.tree.Tree]]:
        tree = self.lexer.parse(text)
        return tree.children[0].children

    def parse(self, text: str) -> List[RawRelation]:
        # FIXME: function doesnt work for  single nodes graph yet
        parsed_nodes = self._parse(text)
        relations = []
        for i, node in enumerate(parsed_nodes):
            if node.data in ("from", "to"):

                relation = RawRelation(from_node=parsed_nodes[i-1],
                                       to_node=parsed_nodes[i+1],
                                       edge=node,
                                       label=node.children[0] if node.children else ""
                                       )
                relations.append(relation)
                i += 2
        return relations
