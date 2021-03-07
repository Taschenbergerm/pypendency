import contextlib
import dataclasses
import string

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
        yield driver
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
    CREATE_NODE = """ MERGE ( a $type$ { id:'@id@', defined: '@graph_id@'}) """

    def __init__(self, graph: Graph, credentials: Credentials ):
        self.graph = graph
        self.creds = credentials
        # environment = jinja2.Environment(loader=loader, trim_blocks=True,block_start_string='@@',block_end_string='@@',variable_start_string='@=', variable_end_string='=@')

    def generate_node_cypher(self):
        pass

    def generate_relation_cypher(self):
        pass

    def query_nodes(self):
        query = f"""MATCH (n) WHERE graph_id=$graph_id """
        res = self.query(query, graph_id=self.graph.id)
        return res

    def query(self, query: str, **kwargs):
        with graph_storage(self.creds) as db:
            with db.seesion() as tx:
                result = tx.run(query, **kwargs)
                ret = result.all()
        return ret
