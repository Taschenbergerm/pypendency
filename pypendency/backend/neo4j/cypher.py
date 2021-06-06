import contextlib
import dataclasses
import string
import neo4j


class CypherTemplate(string.Template):
    delimiter = "§"


@dataclasses.dataclass(frozen=True)
class CypherDialect:
    GRAPH_EXIST = "MATCH (n) where n.project_id =$id RETURN n "
    NODE_EXIST = "MATCH (n) WHERE n.id = $id RETURN n"
    NODES_AND_RELATIONS = "MATCH (n {project_id: $id})-[r]->(m) RETURN n,r,m"
    ALL_NODES = "MATCH (n {project_id: $id}), (n)-->(m) RETURN n, m "
    OWNED_NODES = "MATCH (n {project_id: $id}) RETURN n"
    ALL_RELATIONS = "MATCH (n {project_id: $id})-[r]->(m) RETURN r"
    UPDATE_NODE = "MATCH (n) WHERE n.id = $id SET n.description = $description, n.expose = $expose"
    DELETE_NODE = "MATCH (n {id: $id}) DELETE n"
    DETACH_NODE = "MATCH (n {id: $id}) DETACH DELETE n"
    CREATE_NODE = CypherTemplate("""CREATE (n: §type
                                {id: $id, name: $name, domain: $domain, expose: $expose,
                                 temporary: $temporary, project_id: $project_id})
                                """)
    MERGE_NODE = CypherTemplate("MERGE (a: §type { id: $id })")
    MERGE_RELATION = """MATCH (n {id: $from_id}),(m {id: $to_id}) MERGE (n)-[r:DEPENDS]->(m) RETURN r """
    REALTED_NODES = """MATCH (n {id: $id}), (n)-->(m) RETURN n, m"""
    REALTED_NODES_RELATIONS = """MATCH p=(n {id: $id})-[r:DEPENDS*]->(m)  RETURN nodes(p)"""
    REALTED_PROJECTS = """MATCH p=(n)-[r:DEPENDS*]->(m) WHERE n.id = $id UNWIND nodes(p) as services
                          RETURN distinct services.project_id"""
    REALTED_RELATIONS = """MATCH (n {id: $id}), (n)-->(m) RETURN r"""
    PROJECTS = """MATCH (n:Service) RETURN DISTINCT n.project_id """


@dataclasses.dataclass
class Credentials:
    uri: str
    user: str
    password: str


@contextlib.contextmanager
def graph_storage(creds: Credentials):
    driver = neo4j.GraphDatabase.driver(creds.uri,
                                        auth=(creds.user,
                                              creds.password)
                                        )
    try:
        with driver.session() as tx:
            yield tx
    finally:
        driver.close()
