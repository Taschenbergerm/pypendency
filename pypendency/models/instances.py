import dataclasses
from .generics import BaseNode
from .generics import BaseInstance

_CONTEXT_MANAGER_GRAPH = None


class Service(BaseInstance):
    ...


class Source(BaseInstance):
    ...


class Storage(BaseInstance):
    ...


class Technology(BaseNode):
    ...


class FrameWork(BaseNode):
    ...


class Sink(BaseNode):
    ...

