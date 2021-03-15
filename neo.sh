docker run \
    -p7474:7474 -p7687:7687 \
    --env NEO4J_AUTH=neo4j/admin \
    neo4j:latest
