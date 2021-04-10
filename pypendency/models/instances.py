import dataclasses


@dataclasses.dataclass(frozen=True)
class NodeType:
    service: str = "Service"
    source: str = "Source"
    storage: str = "Storage"
    technology: str = "Technology"
    FrameWork: str = "FrameWork"
    sink: str = "Sink"
