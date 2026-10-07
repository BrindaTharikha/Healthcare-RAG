🩺 Healthcare RAG — Diabetes & Prediabetes Info Assistant
An agentic RAG system that answers general health education questions about diabetes and prediabetes, grounded in real CDC content, with an LLM-based safety guardrail that declines personal diagnosis, treatment, and emergency questions.

What it does

* Answers general questions using only retrieved CDC content.
* Declines personal-medical questions (e.g., "Do I have diabetes?", "what does my A1C of X mean?") with a message pointing to a doctor.
* Declines emergency-pattern questions (chest pain, difficulty breathing, passing out, a dangerously abnormal reading with acute symptoms) with a message pointing to emergency services.
* Routes questions toward adult or youth framing and filters retrieval accordingly.
* Shows retrieved source chunks alongside every answer.

Architecture

```
data/raw/*.md (7 CDC pages)
      │
ingest.py        — parses frontmatter + body into LangChain Documents
      │
chunking.py      — MarkdownHeaderTextSplitter, splits on ## headers
      │
HuggingFaceEmbeddings (all-mpnet-base-v2) + Chroma vector store
      │
graph.py (LangGraph StateGraph)
      ├─ safety_check   — LLM-based guardrail (classify_safety, via Claude):
      │                   classifies each question as allow /
      │                   decline_personal_medical / decline_emergency using
      │                   a dedicated classification prompt; fails safe to
      │                   decline_personal_medical on any unexpected model
      │                   output. On decline, sets the answer and skips
      │                   straight to END via a conditional edge.
      ├─ route          — tags audience + topic_mode
      ├─ retrieval      — embeds question, searches Chroma, filtered by audience
      └─ generation     — answers via Claude, grounded only in retrieved context

```

State is a Pydantic `BaseModel`, validated at creation.

Design notes

* The safety check was originally a regex-based guardrail; it's now an LLM classifier (`classify_safety`, using a dedicated Claude call with a strict system prompt) to catch phrasings regex missed, such as "HbA1c" vs. "A1C" or more oblique references to a personal reading.
* The classifier fails safe: any output outside the three expected labels defaults to `decline_personal_medical` rather than silently allowing the question through.
* Routing is one node with a filter parameter, not duplicated adult/youth nodes.
* Business logic (`guardrails.py`, `retrieval.py`, `generation.py`) is separated from LangGraph wiring (`nodes.py`) — independently testable.
* The decline path still returns a real, user-facing answer.

Future Work

* Add defenses against prompt injection, including via retrieved content.
* Build an automated evaluation harness (guardrail accuracy + retrieval precision) with a hand-labeled test set.
* Consider a lightweight regex pre-filter ahead of the LLM classifier for obvious emergency phrasing, to cut latency/cost on clear-cut cases before invoking the model.

Tech stack
LangGraph · Claude (`claude-sonnet-4-6`) · `sentence-transformers` (`all-mpnet-base-v2`) · ChromaDB · Pydantic · `python-frontmatter` · Streamlit

Running it

```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
echo "ANTHROPIC_API_KEY=your_key_here" > .env

python3 -c "
from agentic_rag.ingest import load_documents
from agentic_rag.chunking import chunk_documents
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from agentic_rag import config

docs = load_documents()
chunks = chunk_documents(docs)
embedding_model = HuggingFaceEmbeddings(model_name=config.EMBEDDING_MODEL_NAME)
Chroma.from_documents(documents=chunks, embedding=embedding_model, persist_directory=str(config.index_dir))
"

streamlit run streamlit_app.py
```
