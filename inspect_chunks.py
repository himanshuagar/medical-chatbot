from langchain_pinecone import PineconeVectorStore
from src.helper import download_embeddings
from dotenv import load_dotenv
import os

load_dotenv()

embedding = download_embeddings()

docsearch = PineconeVectorStore.from_existing_index(
    index_name="medical-chatbot",
    embedding=embedding
)

retriever = docsearch.as_retriever(
    search_kwargs={"k":5}
)

while True:

    question = input("\nAsk Question: ")

    docs = retriever.invoke(question)

    for i, doc in enumerate(docs):

        print("="*70)
        print(f"Rank : {i+1}")
        print(f"Chunk ID : {doc.metadata.get('chunk_id')}")
        print(f"Page : {doc.metadata.get('page')}")
        print(f"Source : {doc.metadata.get('source')}")
        print()
        print(doc.page_content[:500])