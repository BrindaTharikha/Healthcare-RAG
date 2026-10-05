from pydantic import BaseModel


class AgentState(BaseModel):
    question: str
    safety_verdict: str = ""
    audience: str = ""
    topic_mode: str = ""
    retrieved_chunks: list = []
    answer: str = ""