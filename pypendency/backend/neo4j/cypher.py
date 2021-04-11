import contextlib
import dataclasses
from typing import Tuple, List, Set, Optional, Dict

import neo4j

from pypendency.models.generics import Graph, BaseNode, Relation


@dataclasses.dataclass(frozen=True)
class CypherDialect:
    GRAPH_EXIST = "MATCH (n:Graph) where n.id =$id"
    NODE_EXIST = "MATCH (n) WHERE n.id = $id RETURN n"
    NODES_AND_RELATIONS = "MATCH (g: Graph {id: $id}) -->(n)-[r]->(m) RETURN n,r,m"
    ALL_NODES = "MATCH (g: Graph {id: $id}) -->(n)-[r]->(m) RETURN n"
    ALL_RELATIONS = "MATCH (g: Graph {id: $id}) -->(n)-[r]->(m) RETURN r"
    UPDATE_NODE = "MATCH (n) WHERE n.id = $id SET n.description = $description, n.expose = $expose"
    DELETE_NODE = "MATCH (n) WHERE n.id = $id DELETE n"
    DETACH_NODE = "MATCH (n) WHERE n.id = $id DETACH DELETE n"
    CREATE_NODE = "CREATE (n:$type {id: $id, name: $name, domain: $domain, expose: $expose, temporary: $temporary})"
    MERGE_NODE = " MERGE ( a: $type { id: $id }) "
    MERGE_RELATION = "MATCH (n {id: $from_id}),(m {id: $to_id}) MERGE (n)-[r:Depends]->(m)"


@dataclasses.dataclass
class Credentials:
    uri: str
    user: str
    password: str


@contextlib.contextmanager
def graph_storage(creds: Credentials):
    driver = neo4j.GraphDatabase.driver(creds.uri,
                                        auth=(creds.user,creds.password))
    try:

        with driver.session() as tx:
            yield tx
    finally:
        driver.close()
