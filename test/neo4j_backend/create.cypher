CREATE (g:Graph {id:"g1"});
CREATE (g:Graph {id:"g2"});


MATCH (g:Graph {id:"g1"}) Merge (g) -[:DEFINES]-> (n:Service {name: "N1G1", id: "n1"}) ;

MATCH (g:Graph {id:"g1"}) Merge (g) -[:DEFINES]-> (n:Service {name: "N2G1", id: "n2"}) ;

MATCH (g:Graph {id:"g2"}) Merge (g) -[:DEFINES]-> (n:Service {name: "N1G2", id: "n1"}) ;

MATCH (g:Graph {id:"g3"}) Merge (g) -[:DEFINES]-> (n:Service {name: "N1G3", id: "n1"}) ;
MATCH (g:Graph {id:"g3"}) Merge (g) -[:DEFINES]-> (n:Service {name: "N2G3", id: "n2"}) ;


MATCH (g:Graph {id:"g1"}) --> (n {id: "n1" }), (g:Graph {id:"g1"}) --> (m {id: "n2"}) Merge (n)-[:DEPENDS]->(m);
MATCH (g:Graph {id:"g3"}) --> (n {id: "n1" }), (g:Graph {id:"g3"}) --> (m {id: "n2"}) Merge (n)-[:DEPENDS]->(m);
MATCH (g:Graph {id:"g2"}) --> (n {id: "n1" }), (h:Graph {id:"g1"}) --> (m {id: "n1"}) Merge (n)-[:DEPENDS]->(m);
