import dataclasses
import pytest

from pypendency.backend.neo4j.neo import Neo4jBackend
from pypendency.backend.neo4j.cypher import Credentials


@pytest.fixture(scope="module")
def creds(neo_container):
    creds = Credentials(uri=f"bolt://localhost:{neo_container.get_exposed_port(neo_container.bolt_port)}",
                user=neo_container.NEO4J_USER,
                password=neo_container.NEO4J_ADMIN_PASSWORD)
    return creds

@pytest.mark.parametrize(
    "node_id, want",
    [
        ["g1-n1", True],
        ["g5-n1", False],
    ]
)
def test_backend_node_exists(node_id, want, creds, graph, db):
    neo = Neo4jBackend(graph, creds)
    got = neo.check_node_existence(node_id, db)
    assert got == want


@pytest.mark.parametrize(
    "project_id, want",
    [
        ["g1", True],
        ["g5", False],
    ]
)
def test_backend_graph_exists(project_id, want, creds, graph, db):
    neo = Neo4jBackend(graph, creds)
    got = neo.check_existence(project_id, db)
    assert got == want

def test_query_owned( creds, graph, db):
    neo = Neo4jBackend(graph, credentials=creds)
    nodes, relations = neo.query_owned(graph.id, db)
    pytest.assume(len(nodes) == 3)
    pytest.assume(len(relations) == 2)
