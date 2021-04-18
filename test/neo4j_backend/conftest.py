import dataclasses
import pathlib

import pytest
from testcontainers.neo4j import Neo4jContainer

import pypendency.models.graph as pmg
from pypendency.models.generics import BaseNode
from pypendency.backend.neo4j.neo import Neo4jBackend
from pypendency.backend.neo4j.cypher import Credentials
from pypendency.backend.neo4j.cypher import graph_storage


@dataclasses.dataclass()
class FakeGraph:
    id = "g1"


@pytest.fixture(scope="module")
def neo_container():
    with Neo4jContainer() as container:
        yield container


@pytest.fixture()
def prepared_container(neo_container):

    cypher = pathlib.Path(__file__).parent / "create.cypher"
    cql = cypher.read_text()
    with neo_container.get_driver() as driver:
        with driver.session() as session:
            for query in cql.split(";")[:-1]:
                session.run(query)

    return neo_container


@pytest.fixture()
def graph():
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
                         slug="e1",
                         type="Service",
                         description="a External Testnode",
                         id="e1-n1",
                         external=True)
        node4 = BaseNode("F1",
                         slug="e2",
                         type="Service",
                         description="a External Testnode",
                         id="e2-n1",
                         external=True)
    node1 << node2 << node4
    node2 >> node3
    return g


@pytest.fixture()
def backend_instance(prepared_container):
    creds = Credentials(uri=f"bolt://localhost:{prepared_container.get_exposed_port(prepared_container.bolt_port)}",
                        user=prepared_container.NEO4J_USER,
                        password=prepared_container.NEO4J_ADMIN_PASSWORD)
    neo = Neo4jBackend(FakeGraph, creds)
    return neo


@pytest.fixture()
def db(prepared_container):
    creds = Credentials(uri=f"bolt://localhost:{prepared_container.get_exposed_port(prepared_container.bolt_port)}",
                        user=prepared_container.NEO4J_USER,
                        password=prepared_container.NEO4J_ADMIN_PASSWORD)
    with graph_storage(creds) as db:
        yield db

