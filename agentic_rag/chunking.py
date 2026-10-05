from langchain_text_splitters import MarkdownHeaderTextSplitter

_HEADERS_TO_SPLIT_ON = [("##", "Header 2")]


def chunk_documents(docs):
    splitter = MarkdownHeaderTextSplitter(headers_to_split_on=_HEADERS_TO_SPLIT_ON)
    all_chunks = []

    for doc in docs:
        chunks = splitter.split_text(doc.page_content)

        for chunk in chunks:
            combined_metadata = {**doc.metadata, **chunk.metadata}
            chunk.metadata = combined_metadata
            all_chunks.append(chunk)

    return all_chunks