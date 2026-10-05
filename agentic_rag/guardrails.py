import re

_EMERGENCY_PATTERNS = [
    r"\bblood sugar\b.{0,20}\b(\d{3,4})\b",
    r"\bchest pain\b",
    r"\bcan'?t breathe\b|\bdifficulty breathing\b",
    r"\bpassing out\b|\bfaint(ed|ing)?\b",
    r"\bketones?\b",
]

_PERSONAL_MEDICAL_PATTERNS = [
    r"\bdo i have\b.{0,20}\bdiabetes\b",
    r"\bshould i take\b.{0,10}\b(insulin|metformin|medication)\b",
    r"\bmy (doctor|a1c|glucose|blood sugar) (level )?(is|was)\b",
]


def check_safety(question: str) -> str:
    q = question.lower()

    for pattern in _EMERGENCY_PATTERNS:
        if re.search(pattern, q):
            return "decline_emergency"

    for pattern in _PERSONAL_MEDICAL_PATTERNS:
        if re.search(pattern, q):
            return "decline_personal_medical"

    return "allow"

_YOUTH_WORDS = ["child", "kid", "teen", "teenager", "daughter", "son", "my daughter", "my son"]
_MANAGEMENT_WORDS = ["manage", "managing", "medication", "insulin", "monitor", "my blood sugar", "track"]

def route(question: str) -> dict:
    q = question.lower()

    has_youth_word = any(word in q for word in _YOUTH_WORDS)
    has_management_word = any(word in q for word in _MANAGEMENT_WORDS)

    audience = "youth" if has_youth_word else "adult"
    topic_mode = "active_management" if has_management_word else "general_education"

    return {"audience": audience, "topic_mode": topic_mode}