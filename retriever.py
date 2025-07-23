from langchain_community.vectorstores import Chroma
from langchain.schema import Document
from langchain_openai import OpenAIEmbeddings
import os

VECTORSTORE_DIR = "vector_db"

def load_vectorstore():
    embedding_model = OpenAIEmbeddings()
    vectorstore = Chroma(persist_directory=VECTORSTORE_DIR, embedding=embedding_model)
    return vectorstore

def get_retriever(k=6):
    vectorstore = load_vectorstore()
    retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": k})
    return retriever

def retrieve_relevant_docs(query, k=6):
    retriever = get_retriever(k)
    relevant_docs = retriever.get_relevant_documents(query)
    return relevant_docs

if __name__ == "__main__":
    test_query = "Stripe Integration"
    docs = retrieve_relevant_docs(test_query)
    print(f"Retrieved {len(docs)} documents for query: {test_query}")
    print(docs[0].page_content[:500])
