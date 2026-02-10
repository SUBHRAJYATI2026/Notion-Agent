from langgraph.graph import END, StateGraph, START
from langgraph.graph.state import CompiledStateGraph
from src.nodes.response import node
from src.state import State


def ai_graph() -> CompiledStateGraph:
    graph = StateGraph(State)
    graph.add_node("response_node", node)
    graph.add_edge(START, "response_node")
    graph.add_edge("response_node", END)
    return graph.compile()

