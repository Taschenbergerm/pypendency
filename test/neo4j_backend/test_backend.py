from typing import Any

import pytest

from pypendency.backend.neo4j.neo import Neo4jBackend, apply
from pypendency.backend.neo4j.cypher import Credentials
from pypendency.models.generics import BaseNode, Relation, Direction


@pytest.fixture(scope="module")
def creds(neo_container):
    creds = Credentials(
        uri=f"bolt://localhost:{neo_container.get_exposed_port(neo_container.bolt_port)}",
        user=neo_container.NEO4J_USER,
        password=neo_container.NEO4J_ADMIN_PASSWORD,
    )
    return creds


@pytest.mark.parametrize("node_id, want", [["g1-n1", True], ["g5-n1", False],])
def test_backend_node_exists(node_id, want, creds, graph, db):
    neo = Neo4jBackend(creds)
    got = neo.check_node_existence(node_id, db)
    assert got == want


@pytest.mark.parametrize("project_id, want", [["g1", True], ["g5", False],])
def test_backend_graph_exists(project_id, want, creds, graph, db):
    neo = Neo4jBackend(creds)
    got = neo.check_existence(project_id, db)
    assert got == want


def test_query_owned(creds, graph, db):
    neo = Neo4jBackend(credentials=creds)
    nodes, relations = neo.query_owned(graph.id, db)
    pytest.assume(len(nodes) == 3)
    pytest.assume(len(relations) == 2)


def test_neo4j_backend_apply(capsys):
    got = []

    def foo(x: Any):
        got.append(x)

    given = [1, 2, 3, 4]
    apply(foo, given)
    assert got == given


def test_neo4j_backend_query_owned(graph, db):
    neo = Neo4jBackend("")
    remote_nodes, relations = neo.query_owned(graph.id, db)

    pytest.assume(len(remote_nodes) == 3)
    pytest.assume(remote_nodes.get("g1-n1"))
    pytest.assume(remote_nodes.get("g1-n2"))
    pytest.assume(remote_nodes.get("e1-n1"))
    pytest.assume(len(relations) == 2)


def test_neo4j_backend_check_external_node(db, graph):
    neo = Neo4jBackend("")
    non_existing = neo.check_external_nodes(list(graph.nodes), db)

    pytest.assume(not non_existing)
    with graph:
        BaseNode(
            "F2",
            slug="f2",
            type="Service",
            description="a External Testnode",
            id="e2-f2",
            external=True,
        )
    non_existing = neo.check_external_nodes(list(graph.nodes), db)
    pytest.assume(non_existing)
    pytest.assume(non_existing[0].slug == "f2")
    pytest.assume(non_existing[0].id == "e2-f2")


@pytest.mark.parametrize(
    "temporary",
    [
        [True],
        [False]
    ]
)
def test_neo4j_backend_create_node(temporary, db, graph):
    neo = Neo4jBackend("")
    with graph:
        node = BaseNode(
            "N3",
            slug="n3",
            type="Service",
            description="new internal node",
        )

    neo.create_node(node, db, temporary=temporary)
    remote_node = db.run("MATCH (n {id:$id}) RETURN n", id=node.id).data()

    pytest.assume(len(remote_node) == 1 )
    pytest.assume( remote_node[0]["n"]["name"] == node.name)
    pytest.assume( remote_node[0]["n"]["id"] == node.id)


def test_neo4j_backend_update_nodes(db, graph):
    want = "Updated"
    with graph:
        node = BaseNode("E1",
                        slug="e1",
                        type="Service",
                        description=want,
                        domain="ext",
                        id="e1-n1",
                        external=True)

    neo = Neo4jBackend("")

    neo.update_nodes({node.id}, {node.id : node}, db)

    res = db.run("MATCH (n {id: $id}) RETURN n", id=node.id).data()
    got = res[0].get("n").get("description")
    assert got == want


def test_neo4j_backend_update_node(db, graph):
    want = "Updated"
    with graph:
        node = BaseNode("E1",
                        slug="e1",
                        type="Service",
                        description=want,
                        domain="ext",
                        id="e1-n1",
                        external=True)

    neo = Neo4jBackend("")
    neo.update_node(
        node,
        db
    )

    res = db.run("MATCH (n {id: $id}) RETURN n", id=node.id).data()
    got = res[0].get("n").get("description")
    assert got == want


def test_neo4j_backend_delete_node(db, graph):
    node_id = "xx"
    neo = Neo4jBackend("")
    before = db.run("MATCH (n {id: $id }) RETURN n ", id=node_id).data()
    neo.deleted_node(node_id, db)
    after = db.run("MATCH (n {id: $id }) RETURN n ", id=node_id).data()
    assert len(before) == 1
    assert len(after) == 0


def test_neo4j_backend_query(db):
    res = Neo4jBackend.query("MATCH (n) RETURN n", db)
    pytest.assume(res)
    pytest.assume(len(res))
    res = Neo4jBackend.query("MATCH (n {id: $id}) RETURN n", db, id="g1-n1")
    pytest.assume(res)
    pytest.assume(len(res))


def test_neo4j_backend_split_nodes(creds, graph):
    neo = Neo4jBackend(creds)
    internal, external = neo.split_nodes(graph)
    internal_slugs = {node.slug for node in internal}
    external_slugs = {node.slug for node in external}

    pytest.assume(len(internal) == 2)
    pytest.assume("n1" in internal_slugs)
    pytest.assume("n2" in internal_slugs)

    pytest.assume(len(external) == 2)
    pytest.assume("e1" in external_slugs)
    pytest.assume("e2" in external_slugs)


def test_neo4j_backend_merge_relation_new_relation(graph, db):
    externals = [node for node in graph.nodes if node.external]
    externals.sort()
    rel = Relation(
        externals[0],
        externals[1],
        label="DEPENDS",
        direction=Direction.Injective
                   )
    neo = Neo4jBackend("")
    neo.merge_relation(rel, db)
    res = db.run("MATCH (n {id: $id1}) -[r]-> (m {id: $id2}) RETURN n, m, r",
                 id1=externals[0].id,
                 id2=externals[1].id).data()
    pytest.assume(len(res) == 1)
    pytest.assume(res[0]["n"]["id"] == rel.origin.id)
    pytest.assume(res[0]["m"]["id"] == rel.destination.id)
    pytest.assume(res[0]["r"][0]["id"] == rel.origin.id)
    pytest.assume(res[0]["r"][2]["id"] == rel.destination.id)
    pytest.assume(res[0]["r"][1] == rel.label)

def test_neo4j_backend_merge_relation_existing_relation(graph, db):
    internals = [node for node in graph.nodes if not node.external]
    internals.sort()
    rel = Relation(
        internals[1],
        internals[0],
        label="DEPENDS",
        direction=Direction.Injective
                   )
    neo = Neo4jBackend("")
    neo.merge_relation(rel, db)
    res = db.run("MATCH (n {id: $id1}) -[r]-> (m {id: $id2}) RETURN n, m, r",
                 id1=internals[1].id,
                 id2=internals[0].id).data()
    pytest.assume(len(res) == 1)
    pytest.assume(res[0]["n"]["id"] == rel.origin.id)
    pytest.assume(res[0]["m"]["id"] == rel.destination.id)
    pytest.assume(res[0]["r"][0]["id"] == rel.origin.id)
    pytest.assume(res[0]["r"][2]["id"] == rel.destination.id)
    pytest.assume(res[0]["r"][1] == rel.label)


def test_neo4j_backend_compare(creds, graph):
    neo = Neo4jBackend("")
    neo.com

def test_neo4j_backend_manifest(creds, graph):
    neo = Neo4jBackend(creds)
    neo.manifest(graph)
