from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader
from typing import List
from langchain_core.documents import Document

def load_pdf_files(data):
    loader = DirectoryLoader(data, glob="*.pdf",loader_cls=PyPDFLoader)

    documents = loader.load()
    return documents



def filter_to_minimal_docs(docs: List[Document]) -> List[Document]:
    """
    Given a list of Document objects, return a new list of Document objects
    containing only 'source' in metadata and the original page_content.
    """
    minimal_docs: List[Document] = []
    for doc in docs:
        src = doc.metadata.get("source")
        minimal_docs.append(
            Document(
                page_content=doc.page_content,
                metadata={
                    "source": doc.metadata.get("source"),
                    "page": doc.metadata.get("page")
                }
            )
        )
    return minimal_docs


def text_splitter(documents, chunk_size=500, chunk_overlap=20):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )

    chunks = splitter.split_documents(documents)

    for i, chunk in enumerate(chunks):
        chunk.metadata["chunk_id"] = i

    return chunks

from langchain_community.embeddings import HuggingFaceBgeEmbeddings
def download_embeddings():
    model_name = "BAAI/bge-small-en-v1.5"
    embeddings = HuggingFaceBgeEmbeddings(model_name=model_name)
    return embeddings
