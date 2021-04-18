import dataclasses
from typing import List, Optional, TypeVar, Set

Statement = TypeVar("Statement")
BaseNode = TypeVar("BaseNode")
Relation = TypeVar("Relation")


@dataclasses.dataclass()
class Graph(object):
    id: str
    __old_context: List = None
    statements: List[Statement] = None
    nodes: Set[BaseNode] = None
    relations: Set[Relation] = None

    def __post_init__(self):
        self.__old_context = self.__old_context or []
        self.statements = self.statements or []
        self.nodes = self.nodes or set()
        self.relations = self.relations or set()

    def append(self, node: BaseNode):
        self.nodes.add(node)

    def attach_relations(self, relations: Set[Relation]):
        self.relations = self.relations.union(relations)

    def attach_relation(self, relation: Relation):
        self.relations.add(relation)

    def __enter__(self):
        GraphContext.push_context_managed_graph(self)
        return self

    def __exit__(self, _type, _value, _tb):
        GraphContext.pop_context_managed_graph()


class GraphContext:
    _context_managed_graph: Optional[Graph] = None
    _previous_context_managed_graphs: List[Graph] = []

    @classmethod
    def push_context_managed_graph(cls, graph: Graph):
        if cls._context_managed_graph:
            cls._previous_context_managed_graphs.append(cls._context_managed_graph)
        cls._context_managed_graph = graph

    @classmethod
    def pop_context_managed_graph(cls):
        old_graph = cls._context_managed_graph
        if cls._previous_context_managed_graphs:
            cls._context_managed_graph = cls._previous_context_managed_graphs.pop()
        else:
            cls._context_managed_graph = None
        return old_graph

    @classmethod
    def get_current_graph(cls):
        return cls._context_managed_graph
