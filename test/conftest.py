import dataclasses
import pathlib

import pytest
from testcontainers.neo4j import Neo4jContainer

import pypendency.models.graph as pmg
from pypendency.models.generics import BaseNode
from pypendency.backend.neo4j.neo import Neo4jBackend
from pypendency.backend.neo4j.cypher import Credentials
from pypendency.backend.neo4j.cypher import graph_storage


@pytest.fixture(scope="session")
def neo_container():
    with Neo4jContainer() as container:
        yield container


@pytest.fixture(scope="function")
def prepared_container(neo_container):

    cypher = pathlib.Path(__file__).parent / "create.cypher"
    cql = cypher.read_text()
    with neo_container.get_driver() as driver:
        with driver.session() as session:
            for query in cql.split(";")[:-1]:
                session.run(query)

    yield neo_container
    with neo_container.get_driver() as driver:
        with driver.session() as session:
            cql = "MATCH (n) DETACH DELETE n"
            session.run(cql)


@pytest.fixture()
def backend_instance(prepared_container):
    creds = Credentials(uri=f"bolt://localhost:{prepared_container.get_exposed_port(prepared_container.bolt_port)}",
                        user=prepared_container.NEO4J_USER,
                        password=prepared_container.NEO4J_ADMIN_PASSWORD)
    neo = Neo4jBackend(creds)
    return neo


@pytest.fixture()
def db(prepared_container):
    creds = Credentials(uri=f"bolt://localhost:{prepared_container.get_exposed_port(prepared_container.bolt_port)}",
                        user=prepared_container.NEO4J_USER,
                        password=prepared_container.NEO4J_ADMIN_PASSWORD)
    with graph_storage(creds) as db:
        yield db

