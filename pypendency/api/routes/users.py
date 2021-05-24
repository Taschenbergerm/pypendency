import enum

import fastapi
import pydantic
from fastapi import Query, Header


router = fastapi.APIRouter(
    prefix="/user",
    tags=["/user"],
    include_in_schema=False
)


class State(enum.Enum):
    active: 1
    deactivate: 0
    suspended: -1


class User(pydantic.BaseModel):
    name: str
    password: str
    role: str
    status: State


@router.get("/")
def query_user_statistics():
    return "We currently have X users"

@router.get("/")
def query_all_users():
    return "Here take them all "


@router.get("/{user-id}")
def query_user(user_id: str):
    return f"Queried for user {user_id}"


@router.post("/")
def add_user(user: User, admin_token: str = Header(...)):
    return f"Try to create user {user.name}"


@router.put("/{user-id}")
def update_user(user_id: str, status: State = Query(...), admin_token: str = Header(...)):
    return f"User {user_id} was updated "

@router.delete("/{user-id}")
def delete_user(user_id: str,admin_token: str = Header(...)):
    return f"Delete user {user_id}"
