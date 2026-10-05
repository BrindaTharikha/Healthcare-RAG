from langgraph.graph import StateGraph, END

from .state import AgentState
from .nodes import safety_check_node, route_node, retrieval_node, generation_node


def decide_after_safety_check(state: AgentState) -> str:
    if state.safety_verdict == "allow":
        return "continue"
    else:
        return "decline"


graph_builder = StateGraph(AgentState)

graph_builder.add_node("safety_check", safety_check_node)
graph_builder.add_node("route", route_node)
graph_builder.add_node("retrieval", retrieval_node)
graph_builder.add_node("generation", generation_node)

graph_builder.set_entry_point("safety_check")

graph_builder.add_conditional_edges(
    "safety_check",
    decide_after_safety_check,
    {
        "continue": "route",
        "decline": END,
    },
)

graph_builder.add_edge("route", "retrieval")
graph_builder.add_edge("retrieval", "generation")
graph_builder.set_finish_point("generation")

graph = graph_builder.compile()