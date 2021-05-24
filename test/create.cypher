CREATE (n:Service {name: "N1", slug: "n1", id:"g1-n1", project_id:"g1"}) ;
CREATE (n:Service {name: "N2", slug: "n2", id:"g1-n2", project_id:"g1"}) ;
CREATE (n:Service {name: "E1", slug: "n1", id:"e1-n1", project_id:"e1"}) ;
CREATE (n:Service {name: "F1", slug: "n1", id:"e2-n1", project_id:"e2"}) ;
CREATE (n:Service {name: "X1", slug: "x1", id:"xx", project_id:"x"}) ;
MATCH (n {id: "g1-n1" }), (m {id: "g1-n2"}) Merge (m)-[:DEPENDS]->(n);
MATCH (n {id: "e1-n1" }), (m {id: "g1-n2"}) Merge (m)-[:DEPENDS]->(n);
MATCH (n {id: "e2-n1" }), (m {id: "g1-n2"}) Merge (n)-[:DEPENDS]->(m);
