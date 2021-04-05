import pathlib
from typing import Union

import yaml
from pypendency.models.graph import Graph, BaseNode
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
        graph = Graph(ctx["id"])
        self._create_nodes_in_graph(ctx["owned"], graph, external=False)
        self._create_nodes_in_graph(ctx["external"], graph, external=True)
        relations = self.lexer.lex(ctx["relations"])


def _create_nodes_in_graph(self, raw_nodes, graph, external):
    with graph:
        for slug, node in raw_nodes.items():
            node[slug] = BaseNode(
                node["name"],
                slug=slug,
                type=node["type"],
                domain=node["domain"],
                id=node["id"],
                global_node=external,
                description=node.get("description"),
            )
