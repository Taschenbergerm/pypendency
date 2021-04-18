"""Tests for nodes"""
import uuid


import pytest

import pypendency.models.graph as pmg
from pypendency.models.generics import BaseNode, Relation, Direction


def test_bitshift_left():
    external_node_id = str(uuid.uuid4())
    g = pmg.Graph("g1")
    with g:
        node1 = BaseNode("N1",
                         slug="n1",
                         type="Service",
                         description="a Testnode")
        node2 = BaseNode("N2",
                         slug="n2",
                         type="Service",
                         description="a Testnode")
        node3 = BaseNode("E1",
                         slug="e2",
                         type="Service",
                         description="a External Testnode",
                         id=external_node_id,
                         external=True)
    node1 << node2 << node3

    expected_rel_1 = Relation(origin=node2, destination=node1, label="Depends", direction=Direction.Injective)
    expected_rel_2 = Relation(origin=node3, destination=node2, label="Depends", direction=Direction.Injective)

    pytest.assume(len(node1.relations) == 1)
    pytest.assume(len(node2.relations) == 1)
    pytest.assume(node1.relations.pop() == expected_rel_1)
    pytest.assume(node2.relations.pop() == expected_rel_2)


def test_bitshift_right():
    external_node_id = str(uuid.uuid4())
    g = pmg.Graph("g1")
    with g:
        node1 = BaseNode("N1",
                         slug="n1",
                         type="Service",
                         description="a Testnode")
        node2 = BaseNode("N2",
                         slug="n2",
                         type="Service",
                         description="a Testnode")
        node3 = BaseNode("E1",
                         slug="e2",
                         type="Service",
                         description="a External Testnode",
                         id=external_node_id,
                         external=True)
    node3 >> node2 >> node1

    expected_rel_1 = Relation(origin=node2, destination=node1, label="Depends", direction=Direction.Injective)
    expected_rel_2 = Relation(origin=node3, destination=node2, label="Depends", direction=Direction.Injective)

    pytest.assume(len(node1.relations) == 0)
    pytest.assume(len(node2.relations) == 1)
    pytest.assume(len(node3.relations) == 1)
    pytest.assume(node2.relations.pop() == expected_rel_1)
    pytest.assume(node3.relations.pop() == expected_rel_2)


def test_bitshift_mixed():
    external_node_id = str(uuid.uuid4())
    g = pmg.Graph("g1")
    with g:
        node1 = BaseNode("N1",
                         slug="n1",
                         type="Service",
                         description="a Testnode")
        node2 = BaseNode("N2",
                         slug="n2",
                         type="Service",
                         description="a Testnode")
        node3 = BaseNode("E1",
                         slug="e2",
                         type="Service",
                         description="a External Testnode",
                         id=external_node_id,
                         external=True)
    node1 >> node2 << node3

    expected_rel_1 = Relation(origin=node1, destination=node2, label="Depends", direction=Direction.Injective)
    expected_rel_2 = Relation(origin=node3, destination=node2, label="Depends", direction=Direction.Injective)

    pytest.assume(len(node1.relations) == 1)
    pytest.assume(len(node2.relations) == 1)
    pytest.assume(len(node3.relations) == 0)
    pytest.assume(node1.relations.pop() == expected_rel_1)
    pytest.assume(node2.relations.pop() == expected_rel_2)
