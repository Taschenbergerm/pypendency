import fastapi
from fastapi import File, UploadFile, Request


router = fastapi.APIRouter(
    prefix="/project",
    tags=["project"]
)


@router.get("/")
def query_all_projects(request: Request):
    query = request.app.state.dialect.PROJECTS
    session = request.app.state.pool.session()
    result = session.run(query)
    records = [record for record in result]
    session.close()
    return records


@router.put("/")
def put_project(request: Request, content: bytes = File(...)):
    return "You want to create a new project"


@router.post("/")
def post_project(request: Request, content: UploadFile = File(...)):
    return "You want to post a new project"


@router.get("/reltated/{project-id}")
def query_related_projects(project_id: str, request: Request):

    return f"You queried for the Project with the id {project_id}"


@router.get("/direct-dependencies/{project-id}")
def query_direct_dependecies(project_id: str, request: Request):

    return f"You want all direct depencies of {project_id}"


@router.get("/dependencies/{project-id}")
def query_direct_dependecies(project_id: str, request: Request):
    return f"You want all depencies of {project_id}"


@router.get("/dependent/{project-id}")
def query_direct_dependecies(project_id: str, request: Request):
    return f"You want all dependent Projects of  {project_id}"


@router.get("/direct-dependent/{project-id}")
def query_direct_dependecies(project_id: str, request: Request):
    return f"You want all direct dependent Projects of {project_id}"
