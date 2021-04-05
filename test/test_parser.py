import pathlib

import pytest

from pypendency.parser.yaml import Parser
from pypendency.lexer import LarkRelationLexer


def test_read_yaml():
    file = pathlib.Path(__file__).parent / "example.yml"
    p = Parser(lexer=LarkRelationLexer())
