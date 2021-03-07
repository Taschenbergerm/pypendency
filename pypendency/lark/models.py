import dataclasses
from typing import List, Union

import lark


@dataclasses.dataclass
class RawRelation:
    from_node:  List[Union[str, lark.tree.Tree]]
    to_node:  List[Union[str, lark.tree.Tree]]
    edge: str
    label: str
