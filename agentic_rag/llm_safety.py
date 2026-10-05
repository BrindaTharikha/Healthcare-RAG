from dotenv import load_dotenv
load_dotenv()

from langchain_anthropic import ChatAnthropic

_llm = ChatAnthropic(model="claude-sonnet-4-6")

_CLASSIFY_SYSTEM = (
    "You classify health questions into exactly one category:\n"
    "- allow: a general health education question\n"
    "- decline_personal_medical: asks for a personal diagnosis, treatment decision, "
    "or references the person's own specific lab value/reading (e.g., their own A1C, "
    "glucose, HbA1c) in the context of asking what it means for them\n"
    "- decline_emergency: describes acute/emergency symptoms (chest pain, can't breathe, "
    "passing out, a dangerously abnormal reading with acute symptoms)\n\n"
    "Respond with ONLY the category label, nothing else."
)


def classify_safety(question: str) -> str:
    response = _llm.invoke([
        ("system", _CLASSIFY_SYSTEM),
        ("human", question),
    ])
    label = response.content.strip().lower()
    if label not in {"allow", "decline_personal_medical", "decline_emergency"}:
        return "decline_personal_medical"  # fail safe, not fail open
    return label