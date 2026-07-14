from langchain_pinecone import PineconeVectorStore

from src.helper import load_pdf_files, filter_to_minimal_docs, text_splitter, download_embeddings

from pinecone import ServerlessSpec
from pinecone import Pinecone
from dotenv import load_dotenv
import os 
load_dotenv()

extracted_data = load_pdf_files("data")

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY

pinecone_api_key = PINECONE_API_KEY
pc = Pinecone(api_key=pinecone_api_key)
pc

index_name = "medical-chatbot"

# if pc.has_index(index_name):
#     pc.delete_index(index_name)
#     print("Old index deleted.")

if not pc.has_index(index_name):
    pc.create_index(
        name=index_name,
        dimension=384,  # Dimension of the embeddings
        metric="cosine",  # Similarity metric
        spec=ServerlessSpec(cloud="aws", region="us-east-1")
    )

index = pc.Index(index_name)

# text_chunks = text_splitter(filter_to_minimal_docs())

minimal_docs = filter_to_minimal_docs(extracted_data)
text_chunks = text_splitter(minimal_docs)

print(text_chunks[0].metadata)
print(text_chunks[1].metadata)
print(text_chunks[2].metadata)

embedding = download_embeddings()
docsearch = PineconeVectorStore.from_documents(
    documents=text_chunks, embedding=embedding, index_name=index_name
    )