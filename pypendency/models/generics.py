import dataclasses
import enum
from typing import TypeVar, Optional, Generic, List, Union, Set

from loguru import logger

from .graph import Graph

T = TypeVar("T")


class Direction(enum.Enum):
    Bijection = enum.auto()
    Injective = enum.auto()
    Link = enum.auto()


class NodeError(Exception):
    pass


@dataclasses.dataclass()
class BaseNode(Generic[T]):
    name: str
    slug: str
    type: str
    description: str
    id: str = ""
    domain: Optional[str] = ""
    graph: Optional[Graph] = None
    external: bool = False
    expose: bool = False
    relations: Set["Relation"] = None

    def __post_init__(self):
        from .graph import GraphContext

        self.relations = self.relations or set()
        self.graph = self.graph or GraphContext.get_current_graph()

        if self.graph:
            self.graph.append(self)

        if not self.id and not self.external:
            self.id = f"{self.graph.id}-{self.slug}"

        elif not id and self.external:
            raise NodeError(f"External node {self.name} defined without ID")
        else:
            logger.debug(f"Node {self.__repr__}created as internal and with existing ID")

    def edge_from(self, other: "BaseNode[T]", label: str = "Depends"):
        relation = Relation(
            origin=other, destination=self, label=label, direction=Direction.Injective
        )
        self._add_relation(relation)

    def edge_to(self, other: "BaseNode[T]", label: str = "Depends"):
        relation = Relation(
            origin=self, destination=other, label=label, direction=Direction.Injective
        )
        self._add_relation(relation)

    def link_to(self, other: "BaseNode[T]", label: str = "Link"):
        relation = Relation(
            origin=self, destination=other, label=label, direction=Direction.Link
        )
        self._add_relation(relation)

    def _add_relation(self, relation):
        self.relations.add(relation)
        if self.graph:
            self.graph.attach_relation(relation)

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other.id

    def __le__(self, other):
        return self.id <= other.id

    def __lt__(self, other):
        return self.id < other.id

    def __ge__(self, other):
        return self.id >= other.id

    def __gt__(self, other):
            return  self.id > other.id

    def __repr__(self):
        return f"Node<{self.id}>"

    def __str__(self):
        return self.id

    def __lshift__(self, other):
        self.edge_from(other, label="Depends")
        return other

    def __rshift__(self, other):
        self.edge_to(other, label="Depends")
        return other


@dataclasses.dataclass()
class Relation(object):

    origin: BaseNode
    destination: BaseNode
    label: str
    direction: Direction

    def __post_init__(self):

        if self.direction != Direction.Injective:
            nodes = [self.origin, self.destination]
            nodes.sort()
            self.origin, self.destination = nodes

    def __repr__(self):
        if self.direction == Direction.Injective:
            relation = f"-{self.label}->"
        elif self.direction == Direction.Bijection:
            relation = f"<-{self.label}->"
        else:
            relation = f"-{self.label}-"

        return f"({self.origin}){relation}({self.destination})"

    def __hash__(self):
        return hash(self.__repr__())


@dataclasses.dataclass()
class BaseInstance(BaseNode):
    domain: str = ""
