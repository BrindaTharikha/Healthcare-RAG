from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

from . import config

_embedding_model = HuggingFaceEmbeddings(model_name=config.EMBEDDING_MODEL_NAME)

_vectorstore = Chroma(
    persist_directory=str(config.index_dir),
    embedding_function=_embedding_model,
)


def retrieve(question: str, audience: str, k: int = None) -> list:
    k = k or config.TOPK
    results = _vectorstore.similarity_search(
        question,
        k=k,
        filter={"audience": audience},
    )
    return results