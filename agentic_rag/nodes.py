from .guardrails import check_safety, route
from .state import AgentState
from .retrieval import retrieve

from .llm_safety import classify_safety
from .state import AgentState

_DECLINE_MESSAGES = {
    "decline_personal_medical": "I can share general health education information, but I'm not able to give a personal diagnosis or treatment advice. Please talk to your doctor.",
    "decline_emergency": "This sounds like it could be a medical emergency. Please call 911 or your local emergency number right away.",
}


def safety_check_node(state: AgentState) -> dict:
    verdict = classify_safety(state.question)

    if verdict == "allow":
        return {"safety_verdict": verdict}
    else:
        return {"safety_verdict": verdict, "answer": _DECLINE_MESSAGES[verdict]}
        
def route_node(state: AgentState) -> dict:
    routing = route(state.question)
    return routing

def retrieval_node(state: AgentState) -> dict:
    chunks = retrieve(state.question, state.audience)
    return {"retrieved_chunks": chunks}

from .generation import generate_answer

def generation_node(state: AgentState) -> dict:
    answer = generate_answer(state.question, state.retrieved_chunks)
    return {"answer": answer}