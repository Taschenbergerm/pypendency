import dataclasses
from typing import TypeVar, Optional, Generic, List, Union
import enum
from .graph import Graph

T = TypeVar('T')


class Direction(enum.Enum):
    Bijection = enum.auto()
    Injective = enum.auto()
    Link = enum.auto()


@dataclasses.dataclass()
class BaseNode(Generic[T]):
    name: str
    slug: str
    type: str
    id: str
    description: str
    graph: Optional[Graph] = None
    compound: bool = False
    global_node: bool = False
    relations: List['Relation'] = None

    def __post_init__(self):
        from .graph import GraphContext
        if not self.graph:
            self.graph = GraphContext.get_current_graph()
        self.graph.append(self)

        if not self.relations:
            self.relations = []

        if not self.nodes:
            self.nodes = []

    def edge_from(self, other: 'BaseNode[T]', label: str):
        relation = Relation(origin=other, destination=self, label=label, direction=Direction.Injective)
        self.relations.append(relation)

    def edge_to(self, other: 'BaseNode[T]', label: str):
        relation = Relation(origin=self, destination=other, label=label, direction=Direction.Injective)
        self.relations.append(relation)

    def link_to(self, other: 'BaseNode[T]', label: str):
        relation = Relation(origin=self, destination=other, label=label, direction=Direction.Link)
        self.relations.append(relation)

    def __hash__(self):
        return self.id

    def __eq__(self, other):
        return self.id == other.id

    def __repr__(self):
        return f"Node<{self.id}>"


@dataclasses.dataclass()
class Relation(object):

    origin: BaseNode
    destination: BaseNode
    label: str
    direction: Direction

    def __repr__(self):
        return f"{self.origin} -{self.label}:{self.direction}- {self.destination}"

    def __hash__(self):
        return hash(self.__repr__)


@dataclasses.dataclass()
class BaseInstance(BaseNode):
    domain: str = ""
