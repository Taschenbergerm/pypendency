import fastapi

router = fastapi.APIRouter(
    prefix="/nodes",
    tags=["nodes"]
)


@router.get("/")
def query_nodes(request: fastapi.Request):
    query = request.app.state.dialect.ALL_NODES
    session = request.app.state.pool.session()
    result = session.run(query)
    records = [record for record in result]
    session.close()
    return records


@router.get("/{node-id}")
def query_node(node_id: str, request: fastapi.Request):
    query = request.app.state.dialect.NODE_EXISTS
    session = request.app.state.pool.session()
    result = session.run(query, id=node_id)
    records = [record for record in result]
    session.close()
    return records


@router.post("/")
def query_node(node_id: str, request: fastapi.Request):
    query = request.app.state.dialect.NODE_EXISTS
    session = request.app.state.pool.session()
    result = session.run(query, id=node_id)
    records = [record for record in result]
    session.close()
    return records


@router.get("/related/{node-id}")
def query_related_nodes(node_id, request: fastapi.Request):
    query = request.app.state.dialect.REALTED_NODES_RELATIONS
    session = request.app.state.pool.session()
    result = session.run(query, id=node_id)
    records = [record for record in result]
    session.close()
    return records

