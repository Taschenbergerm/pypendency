import pathlib
from typing import Union

import yaml
from pypendency.models.graph import Graph
from pypendency.models.generics import BaseNode
from pypendency.generics import LexerInterface


class Parser(object):
    def __init__(
        self,
        lexer: LexerInterface,
        folder: pathlib.Path = None,
    ):
        self.folder = folder or pathlib.Path(".")
        self.lexer = lexer

    def parse(self, file: Union[str, pathlib.Path]) -> Graph:

        yaml_file = self.folder / file
        content = yaml_file.read_text("utf-8")
        graph = self.parse_string(content)
        return graph

    def parse_string(self, content: str) -> Graph:
        ctx = yaml.load(content)
        graph = Graph(ctx["project"]["id"])
        self._create_nodes_in_graph(ctx["owned"], graph, external=False)
        self._create_nodes_in_graph(ctx["external"], graph, external=True)
        self.lexer.set_nodes(graph.nodes)
        relations = self.lexer.lex(ctx["relations"])
        graph.attach_relations(relations)
        return graph

    def _create_nodes_in_graph(self, raw_nodes, graph, external):
        with graph:
            for slug, node in raw_nodes.items():
                node[slug] = BaseNode(
                    node["name"],
                    slug=slug,
                    type=node["type"],
                    domain=node["domain"],
                    id=node["id"],
                    external=external,
                    description=node.get("description"),
                )
