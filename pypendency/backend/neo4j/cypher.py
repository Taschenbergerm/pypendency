import contextlib
import dataclasses
import string
from typing import Tuple, List, Set

import jinja2
import neo4j

from pypendency.models.generics import Graph

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

class Neo4jBackend(object):
    """
    Neo4jBackend is responsible for transforming a Graph with all its nodes and
    relations to be transformed to cypher

    1. Pull all nodes and relations defined in this
    2. Check which nodes and relations do exists
    3. Check for removed nodes and whether they are used
    4. Merge Create all nodes
    5. Update all nodes and overwrite attributes
    6. CREATE nonexistent relationships
    7. Update old relationships
    """
    CREATE_NODE = """ MERGE ( a $type$ { id:'@id@', owner: '@graph_id@'}) """

    def __init__(self, graph: Graph, credentials: Credentials ):
        self.graph = graph
        self.creds = credentials
        # environment = jinja2.Environment(loader=loader, trim_blocks=True,block_start_string='@@',block_end_string='@@',variable_start_string='@=', variable_end_string='=@')


    def compare(self, graph: Graph):
        try:
            self.connect()
            self.manifest(graph )
        finally:
            self.disconnect()

    def manifest(self, graph: Graph):
        with graph_storage(self.creds) as db:
            exists = self.check_existence(graph.id, db)
            if exists:
                nodes, relations = self.query_owned_nodes(graph.id, db)
            else:
                self.create_owned_nodes_and_relartions(graph, db)

            self.check_external_nodes(db)

            self.check_deleted_nodes(db)
            self.check_relations(db)
            self.manifest_cypher(db)

    def query_owned_nodes(self, id: str, db) -> Tuple[Set, Set]:
        neo_result = self.query("MATCH (g: Graph {id: $id}) -->(n)-[r]->(m) RETURN n,r,m", id=id)
        node_ids = {res["n"]["id"] for res in neo_result}
        node_relations = {(res["n"]["id"], res["n"]["id"], res["r"][1]) for res in neo_result }
        return node_ids, node_relations

    def check_existence(self, id: str, db) -> bool:
        cql = "MATCH (n:Graph) where n.id =$id"
        res = self.query(cql, db, id=id)
        return any(res)


    def check_owned_nodes_and_relations(self, graph: Graph, db):
        self.check_nodes(graph.nodes, graph.id,  db)
        self.check_relations(graph.relations, graph.id, db)

    def check_nodes(self, nodes, db):
        cql = "MATCH (g:Graph {id: $graph_id}) --> (n {id: $id}) RETURN n"
        for node in nodes:
            res = self.query()


    def create_owned_nodes_and_relartions(self, graph: Graph, db):
        self.create_nodes(graph.nodes, db)
        self.create_relations(graph.relations, db)


    def query_node(self, id: str, db):
        query = "MATCH (n) WHERE n.id=$id and n.graph.id=$graph_id RETURN n"
        res = self.query(query, db, graph_id=self.graph.id)
        return res

    def query_relation(self, from_id, to_id, db):
        query ="MATCH n-[r]->m WHERE n.id=$from_id and m.id=$to_id RETURN r"
        res = self.query(query, db, from_id=from_id, to_id=to_id)
        return res


    def query(self, query: str, db, **kwargs):
        res = db.run(query,
                     **kwargs)
        return res.data()

