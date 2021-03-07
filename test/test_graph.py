"""Tests for `pypendency` package."""
import uuid

import pypendency.models.graph as pmg
from pypendency.models.generics import BaseNode, Relation, Direction


def test_graph_context():
    g = pmg.Graph(str(uuid.uuid4()))
    with g:
        node = BaseNode("TestNode",
                        slug="t1",
                        type="Service",
                        id=str(uuid.uuid4()),
                        description="a Testnode")
        assert node.graph is not None
    assert node == g.nodes.pop()


def test_relation():
    g = pmg.Graph(str(uuid.uuid4()))
    with g:
        node1 = BaseNode("TestNode1",
                         slug="t1",
                         type="Service",
                         id=str(uuid.uuid4()),
                         description="a Testnode")

        node2 = BaseNode("TestNode2",
                         slug="t2",
                         type="Service",
                         id=str(uuid.uuid4()),
                         description="a Testnode")
        node1.link_to(node2, "link")
    expect = Relation(node1, node2, "link", direction=Direction.Link)
    actual = node1.relations.pop()
    assert expect == actual
