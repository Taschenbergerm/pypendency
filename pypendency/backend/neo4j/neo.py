from typing import Dict, Tuple, List

import neo4j
from neo4j.graph import Node
from pypendency import Graph, BaseNode, Relation

class GraphComparer:

    def compare(self,g1: Graph, g2: Graph) -> Tuple[List[BaseNode],List[BaseNode],List[BaseNode]]:
        ...

class NeoCredentails:
    user: str
    password: str
    host: str
    port: int
    driver: str

    def uri(self) -> str:
        return ""


class Neo4J(object):

    def __init__(self, credentials: NeoCredentails):
        self.driver = neo4j.GraphDatabase.driver(credentials.uri(), auth=(credentials.user, credentials.password))

    def main(self, token: str):
        """
        Neo4j Backend Class will persist the graph in the backend
        1.  Check that the token is valid
        2.  Query all nodes defined by this graph and directly related nodes
        3. Transform them into the BaseNode format
        4. Create non-existing nodes
        5. Updated nodes that already exists
        6. Delete nodes

        :return:
        """
        if not self.check_token(token):
            raise PermissionError(f"Token {token} is not registered ")

        records = self.query_graphtoken()
        graph = self.transform_records_to_graph(records)
        return graph

    def check_token(self, token):
        query = "MATCH (t:Token {id: $token}  RETURN t"
        records = self.query(query, token=token)
        return bool(len(records))

    def query_to_graph(self, token) -> Graph:
        query = "MATCH (t {token: $token}) -[r]-> (n) RETURN t, r, n "
        records = self.query(query, token=token)
        graph = Graph(token)
        with graph:
            _ = self.create_nodes(records)
        return graph

    def create_nodes(self, records: neo4j.data.Record) -> Dict[str, BaseNode]:
        node_dict: Dict[str, BaseNode] = {}
        relationships = []
        for r in records:
            if r is Node:
                node_type, = r.labels
                node_dict[r["id"]] = BaseNode(name=r["name"],
                                                slug=r["name"],
                                                type=node_type,
                                                id=r["id"],
                                                )
            else:
                relationships.append(r)

        for rel in relationships:
            start_node_id = rel.start_node["id"]
            end_node_id = rel.end_node["id"]
            node_dict[start_node_id].link_to(node_dict[end_node_id], rel.type)

        return node_dict

    def query(self, query, **kwargs) -> neo4j.data.Record:
        with self.driver.session() as session:
            res = session.run(query, **kwargs)
            records = res.single()
        return records
