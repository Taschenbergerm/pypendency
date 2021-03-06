import uuid

import pytest
import pypendency.models.graph as pmg
from pypendency.models.generics import BaseNode, Relation, Direction

from pypendency.lexer.lark.core import Lexer
import pypendency.lexer.lark.transformer as transformer


def test_tranformer():
    raw_text = " n1 -> n2"
    lex = Lexer()
    raw_relations = lex.parse(raw_text)
    g = pmg.Graph(str(uuid.uuid4()))
    with g:
        node1 = BaseNode("Node1",
                         slug="n1",
                         type="Service",
                         id=str(uuid.uuid4()),
                         description="a Testnode")

        node2 = BaseNode("Node2",
                         slug="n2",
                         type="Service",
                         id=str(uuid.uuid4()),
                         description="a Testnode")
    t = transformer.Transformer(graph=g)
    want = Relation(node1, node2, label="", direction=Direction.Injective)
    got = t.create_relations_from_raw_relations(raw_relations)
    pytest.assume(len(got) == 1)
    pytest.assume( got[0] == want)


def test_transformer_group():
    raw_text = " n1 -> [n2, n3]"
    lex = Lexer()
    raw_relations = lex.parse(raw_text)
    g = pmg.Graph(str(uuid.uuid4()))
    with g:
        node1 = BaseNode("Node1",
                         slug="n1",
                         type="Service",
                         id=str(uuid.uuid4()),
                         description="a Testnode")

        node2 = BaseNode("Node2",
                         slug="n2",
                         type="Service",
                         id=str(uuid.uuid4()),
                         description="a Testnode")
        node3 = BaseNode("Node3",
                         slug="n3",
                         type="Service",
                         id=str(uuid.uuid4()),
                         description="a Testnode")
    t = transformer.Transformer(graph=g)
    want = Relation(node1, node2, label="", direction=Direction.Injective)
    want2 = Relation(node1, node3, label="", direction=Direction.Injective)
    got = t.create_relations_from_raw_relations(raw_relations)
    pytest.assume(len(got) == 2)
    pytest.assume(got[0] == want)
    pytest.assume(got[1] == want2)
