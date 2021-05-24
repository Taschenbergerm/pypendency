import pathlib

import pytest

from pypendency.parser.yaml import Parser
from pypendency.lexer import LarkRelationLexer


def test_read_yaml_node_length():
    file = pathlib.Path(__file__).parent / "example.yml"
    lexer = LarkRelationLexer()
    p = Parser(lexer=lexer, folder=pathlib.Path(__file__).parent)
    g = p.parse("example.yml")
    length = len(g.nodes)
    pytest.assume(length == 4)

