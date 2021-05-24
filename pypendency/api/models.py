import datetime
from typing import Optional, List

import pydantic


class Node(pydantic.BaseModel):
    name: str
    slug: str
    type: str
    description: str
    id: str = ""
    domain: Optional[str] = ""
    external: bool = False
    expose: bool = False


class StatusObject(pydantic.BaseModel):
    timestamp: datetime.datetime
    jobId: str
    status: str
    resultCode: int
    errorMessage: str
    elapsed: int


class NodeResponse(pydantic.BaseModel):
    data: List[Optional[Node]]
    status: StatusObject

