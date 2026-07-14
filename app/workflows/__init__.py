from app.workflows.edges import Edge, NormalEdge, ConditionalEdge

EDGE_TYPES: dict[str, Edge] = {
    "normal": NormalEdge,
    "conditional": ConditionalEdge,
}
