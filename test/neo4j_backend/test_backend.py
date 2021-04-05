import dataclasses

from pypendency.backend.neo4j.cypher import Neo4jBackend
from pypendency.backend.neo4j.cypher import Credentials
from pypendency.backend.neo4j.cypher import graph_storage


@dataclasses.dataclass()
class FakeGraph:
    id = "g1"


def test_query():
    creds = Credentials(uri="bolt://localhost:7687", user="neo4j", password="admin")
    neo = Neo4jBackend(FakeGraph, creds)
    with graph_storage(creds) as db:
        res = neo.query("MATCH (n)-[r]->(m) RETURN n,m,r", db)
    assert res
