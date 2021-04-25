from typing import Tuple, List, Set, Optional, Dict, Callable, Iterable

from pypendency.models.generics import Graph, BaseNode, Relation
from .cypher import CypherDialect, Credentials, graph_storage


def apply(func: Callable, iterable: Iterable, **kwargs):
    for i in iterable:
        func(i, **kwargs)


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

    def __init__(self, credentials: Credentials ):
        self.creds = credentials

    def manifest(self, graph: Graph):
        with graph_storage(self.creds) as db:
            internal, external = self.split_nodes(graph)
            exists = self.check_existence(graph.id, db)
            non_existing_externals = self.check_external_nodes(external, db)
            apply(self.create_node, non_existing_externals, db=db, temporary=True)

            if not exists:
                apply(self.create_node, internal, db=db)
            else:
                self.compare(internal, graph, db)

            apply(self.merge_relation, graph.relations, db=db)

    def compare(self,internal_node: List[BaseNode], graph: Graph, db):
        remote_nodes, relations = self.query_owned(graph.id, db)
        local_ids = {node.id: node for node in internal_node}
        remote_ids = {node.id: node for node in remote_nodes}
        new_nodes = local_ids.keys() - remote_ids.keys()
        deleted_nodes = remote_nodes.keys() - local_ids.keys()
        existing = set(local_ids.keys()).intersection(remote_ids.keys())
        self.create_nodes(new_nodes, local_ids)
        self.update_nodes(existing, local_ids)
        apply(self.deleted_node, deleted_nodes, db=db)

    def query_owned(self, id: str, db) -> Tuple[Set, Set]:
        result = self.query(CypherDialect.ALL_NODES, db, id=id)
        node_ids = self.__unwrap_nodes(result)
        result = self.query(CypherDialect.NODES_AND_RELATIONS, db, id=id)
        node_relations = {(res["n"]["id"], res["m"]["id"], res["r"][1]) for res in result }
        return node_ids, node_relations

    @staticmethod
    def __unwrap_nodes(iterable: List[Dict[str, str]]) -> Set[str]:
        nodes = {}
        for i in iterable:
            for item in i.items():
                if item:
                    nodes[item[1]["id"]] = item[1]
        return nodes

    def check_existence(self, id: str, db) -> bool:
        res = self.query(CypherDialect.GRAPH_EXIST, db, id=id)
        return any(res)

    def check_external_nodes(self, external: List[BaseNode], db) -> List[Optional[BaseNode]]:
        non_existing = []
        for node in external:
            if not self.check_node_existence(node.id, db):
                non_existing.append(node)
        return non_existing

    def check_node_existence(self, id: str, db):
        res = self.query(CypherDialect.NODE_EXIST, db, id=id)
        return any(res)

    def create_node(self, node: BaseNode, db, temporary: bool = False):
        query_kwargs = {"id": node.id, "name": node.name, "expose": node.expose, "domain": node.domain, "temporary": temporary}
        cql = CypherDialect.CREATE_NODE.substitute(type=node.type)
        self.query(cql, db, **query_kwargs)

    def create_nodes(self, new_nodes: Set[str], local_ids: Dict[str, BaseNode], db):
        for node_id in new_nodes:
            self.create_node(local_ids[node_id], db)

    def update_nodes(self, existing: Set[str], local_ids: Dict[str, BaseNode], db):
        for node_id in existing:
            self.update_node(local_ids[node_id], db)

    def update_node(self, node: BaseNode, db):
        update_kwargs = {"id": node.id, "description": node.description, "expose":node.expose}
        self.query(CypherDialect.UPDATE_NODE, db, **update_kwargs)

    def deleted_node(self, node_id, db):
        delete_kwargs = {"id": node_id}
        self.query(CypherDialect.DELETE_NODE, db, **delete_kwargs)

    def merge_relation(self, relation: Relation, db):
        merge_kwargs ={"from_id": relation.origin.id, "to_id": relation.destination.id}
        self.query(CypherDialect.MERGE_RELATION, db, **merge_kwargs)

    @staticmethod
    def query(query: str, db, **kwargs):
        res = db.run(query,**kwargs)
        return res.data()

    @staticmethod
    def split_nodes(graph) -> Tuple[List[BaseNode], List[BaseNode]]:
        internal = []
        external = []
        for node in graph.nodes:
            if node.external:
                external.append(node)
            else:
                internal.append(node)
        return internal, external

    # def query_relation(self, from_id, to_id, db):
    #     res = self.query(CypherDialect.NODES_AND_RELATIONS, db, from_id=from_id, to_id=to_id)
    #     return res

    # def query_node(self, id: str, db):
    #     query = "MATCH (n) WHERE n.id=$id and n.graph.id=$graph_id RETURN n"
    #     res = self.query(query, db, graph_id=id)
    #     return res
