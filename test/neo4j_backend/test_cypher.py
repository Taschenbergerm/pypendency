import dataclasses
import pytest

from pypendency.backend.neo4j.neo import Neo4jBackend
from pypendency.backend.neo4j.cypher import Credentials
from pypendency.backend.neo4j.cypher import CypherDialect
from pypendency.backend.neo4j.cypher import graph_storage


@dataclasses.dataclass()
class FakeGraph:
    id = "g1"


def test_query(prepared_container):
    creds = Credentials(uri=f"bolt://localhost:{prepared_container.get_exposed_port(prepared_container.bolt_port)}",
                        user=prepared_container.NEO4J_USER,
                        password=prepared_container.NEO4J_ADMIN_PASSWORD)
    neo = Neo4jBackend(creds)
    with graph_storage(creds) as db:
        res = neo.query("MATCH (n) -[r]-> (m) RETURN n,m,r", db)
    pytest.assume(res)


@pytest.mark.parametrize(
    "project_id, want",
    [
        ["g1", True],
        ["g100", False]
    ]
                         )
def test_cypher_queries_graph_exists(project_id, want, backend_instance, db):
    res = backend_instance.query(CypherDialect.GRAPH_EXIST, db, id=project_id)
    pytest.assume(any(res) == want)


@pytest.mark.parametrize(
    "node_id, want",
    [
        ["g1-n1", True],
        ["g5-n1", False],
    ]
)
def test_cypher_queries_node_exists(node_id, want, backend_instance, db):
    res = backend_instance.query(CypherDialect.NODE_EXIST, db, id=node_id)
    pytest.assume(any(res) == want)


@pytest.mark.parametrize(
    "project_id, want",
    [
        ["g1", True],
        ["g100", False]
    ]
)
def test_cypher_queries_all_nodes_relations(project_id, want, backend_instance, db):
    res = backend_instance.query(CypherDialect.NODES_AND_RELATIONS, db, id=project_id)
    pytest.assume(any(res) == want)
    pytest.assume(len(res) == 2*want)


@pytest.mark.parametrize(
    "project_id, want",
    [
        ["g1", True],
        ["g100", False]
    ]
)
def test_cypher_queries_all_nodes(project_id, want, backend_instance, db):
    res = backend_instance.query(CypherDialect.ALL_NODES, db, id=project_id)
    pytest.assume(any(res) == want)
    pytest.assume(len(res) == 2*want)


@pytest.mark.parametrize(
    "project_id, want",
    [
        ["g1", True],
        ["g100", False]
    ]
)
def test_cypher_queries_all_relations(project_id, want, backend_instance, db):
    res = backend_instance.query(CypherDialect.ALL_RELATIONS, db, id=project_id)
    pytest.assume(any(res) == want)
    pytest.assume(len(res) == 2*want)


def test_cypher_queries_update_node(backend_instance, db):
    node_id = "g1-n1"
    want = "Updated Desc"
    backend_instance.query(CypherDialect.UPDATE_NODE, db, id=node_id, description=want, expose="true")
    res = backend_instance.query("MATCH (n {id:$id}) RETURN n ", db, id=node_id)
    new_desc = res[0]["n"]["description"]
    pytest.assume(new_desc == want)


def test_cypher_queries_delete_node(backend_instance, db):
    node_id = "g1-n1"
    want = "Updated Desc"
    backend_instance.query(CypherDialect.UPDATE_NODE, db, id=node_id, description=want, expose="true")
    res = backend_instance.query("MATCH (n {id:$id}) RETURN n ", db, id=node_id)
    new_desc = res[0]["n"]["description"]
    pytest.assume(new_desc == want)
