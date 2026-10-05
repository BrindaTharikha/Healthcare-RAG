import frontmatter
from langchain_core.documents import Document

from . import config



def load_documents(raw_dir=None) -> list[Document]:
    raw_dir = raw_dir or config.raw_data_dir
    docs = []

    for path in sorted(raw_dir.glob("*.md")):
        post = frontmatter.load(path)
        combined_metadata = {**post.metadata, "doc_id": path.stem, "last_updated": str(post.metadata["last_updated"])}
        doc = Document(page_content=post.content, metadata=combined_metadata)
        docs.append(doc)

    return docs