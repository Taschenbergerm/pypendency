import uuid

import pytest
from pypendency.models.generics import BaseNode, Relation, Direction


def test_relation_hash():
    external_node_id_1 = str(uuid.uuid4())
    external_node_id_2 = str(uuid.uuid4())
    node1 = BaseNode("E1",
                     slug="e1",
                     type="Service",
                     description="a External Testnode",
                     id=external_node_id_1,
                     external=True)
    node2 = BaseNode("E2",
                     slug="e2",
                     type="Service",
                     description="a External Testnode",
                     id=external_node_id_2,
                     external=True)
    node1.edge_to(node2)
    node2.edge_from(node1)

    relation_set = set(node1.relations)
    relation_set.add(*node2.relations)
    set_length = len(relation_set)
    relations_equality = node1.relations[0] == node2.relations[0]

    pytest.assume(relations_equality)
    pytest.assume(set_length == 1)



@pytest.mark.parametrize(
    "direction,want",
    [
        [Direction.Bijection, 1],
        [Direction.Link, 1],
        [Direction.Injective, 2]

    ])
def test_relation_hash(direction, want):
    external_node_id_1 = str(uuid.uuid4())
    external_node_id_2 = str(uuid.uuid4())
    node1 = BaseNode("E1",
                     slug="e1",
                     type="Service",
                     description="a External Testnode",
                     id=external_node_id_1,
                     external=True)
    node2 = BaseNode("E2",
                     slug="e2",
                     type="Service",
                     description="a External Testnode",
                     id=external_node_id_2,
                     external=True)
    rel_1 = Relation(origin=node1, destination=node2, label="Depends", direction=direction)
    rel_2 = Relation(origin=node2, destination=node1, label="Depends", direction=direction)

    relation_set = {rel_1, rel_2}
    set_length = len(relation_set)
    pytest.assume(set_length == want)

