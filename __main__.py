
from neo4j import GraphDatabase




if __name__ == "__main__":
    uri,user, password  = ("bolt://localhost:7687", "neo4j", "admin")
    driver = GraphDatabase.driver(uri, auth=(user, password))
    query = """Match (n)-[r]->(m) Return n,r,m"""
    with driver.session() as session:
        res = session.run(query, name="marvin")
        print("")


q = """MATCH (a:Person {name:"Doug"}) , (b:Person {name: "Marvin"}) CREATE (a) -[:'LOVES']-> (b)"""
