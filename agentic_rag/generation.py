from dotenv import load_dotenv
load_dotenv()

from langchain_anthropic import ChatAnthropic

_llm = ChatAnthropic(model="claude-sonnet-4-6")

_SYSTEM_MESSAGE = (
    "You are a public health information assistant. Answer ONLY using the "
    "provided context. If the context doesn't contain the answer, say so "
    "plainly rather than guessing."
)


def generate_answer(question: str, retrieved_chunks: list) -> str:
    texts = [chunk.page_content for chunk in retrieved_chunks]
    combined_context = "\n\n---\n\n".join(texts)

    user_message = f"QUESTION: {question}\n\nCONTEXT:\n{combined_context}"

    response = _llm.invoke([
        ("system", _SYSTEM_MESSAGE),
        ("human", user_message),
    ])

    return response.content