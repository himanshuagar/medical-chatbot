from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os
from src.reranker import rerank
from langchain_pinecone import PineconeVectorStore
from langchain_ollama import ChatOllama

from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

from src.helper import download_embeddings
from src.prompt import *
from langchain_core.runnables import RunnableLambda

load_dotenv()

app = Flask(__name__)

# Environment Variables
os.environ["PINECONE_API_KEY"] = os.getenv("PINECONE_API_KEY")
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY", "")

# Embedding model
embedding = download_embeddings()

# Connect to existing Pinecone index
docsearch = PineconeVectorStore.from_existing_index(
    index_name="medical-chatbot",
    embedding=embedding
)

retriever = docsearch.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 10}
)


def retrieve_and_rerank(question):

    docs = retriever.invoke(question)
    print("\nBefore Reranking")
    for d in docs:
        print(d.metadata["chunk_id"])

    docs = rerank(
        question,
        docs,
        top_k=3
    )
    print("\nAfter Reranking")
    for d in docs:
        print(d.metadata["chunk_id"])

    return "\n\n".join(
        doc.page_content
        for doc in docs
    )


llm = ChatOllama(
    model="llama3.2",
    temperature=0
)

rag_chain = (
    {
        "context": RunnableLambda(retrieve_and_rerank),
        "input": RunnablePassthrough(),
    }
    | prompt
    | llm
    | StrOutputParser()
)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():

    data = request.get_json()
    print("Incoming Request:", data)

    question = data.get("message")

    answer = rag_chain.invoke(question)
    print("LLM Response:", answer)

    return jsonify(
        {
            "answer": answer
        }
    )


if __name__ == "__main__":
    app.run(debug=True, port=5001)