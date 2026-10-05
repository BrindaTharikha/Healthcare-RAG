# 🩺 Healthcare RAG — Diabetes & Prediabetes Info Assistant

An agentic RAG system that answers general health education questions about
diabetes and prediabetes, grounded in real CDC content, with a safety
guardrail that declines personal diagnosis, treatment, and emergency
questions.

## What it does

- Answers general questions using only retrieved CDC content.
- Declines personal-medical questions (e.g., "Do I have diabetes?") with a
  message pointing to a doctor.
- Declines emergency-pattern questions (chest pain, abnormal glucose reading,
  difficulty breathing) with a message pointing to emergency services.
- Routes questions toward adult or youth framing and filters retrieval
  accordingly.
- Shows retrieved source chunks alongside every answer.

## Architecture

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
      ├─ safety_check   — regex guardrail (allow / decline_personal_medical /
      │                   decline_emergency); on decline, sets the answer and
      │                   skips straight to END via a conditional edge
      ├─ route          — tags audience + topic_mode
      ├─ retrieval      — embeds question, searches Chroma, filtered by audience
      └─ generation     — answers via Claude, grounded only in retrieved context
```

State is a Pydantic `BaseModel`, validated at creation.

## Design notes

- Routing is one node with a filter parameter, not duplicated adult/youth nodes.
- Business logic (`guardrails.py`, `retrieval.py`, `generation.py`) is
  separated from LangGraph wiring (`nodes.py`) — independently testable.
- The decline path still returns a real, user-facing answer.

## Future Work

- Add an LLM-based classifier as a second-tier safety check, to catch
  phrasings the regex guardrail misses (e.g., "HbA1c" vs. "A1C").
- Add defenses against prompt injection, including via retrieved content.
- Build an automated evaluation harness (guardrail accuracy + retrieval
  precision) with a hand-labeled test set.
  
## Tech stack

LangGraph · Claude (`claude-sonnet-4-6`) · `sentence-transformers`
(`all-mpnet-base-v2`) · ChromaDB · Pydantic · `python-frontmatter` · Streamlit

## Running it

```bash
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

## Disclaimer

Learning/portfolio project, not a medical product. Not a substitute for
professional medical advice.
