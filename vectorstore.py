from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv
import os

load_dotenv() 

def create_vectorstore(chunks, persist_directory="vector_db"):
    # Inicializa el modelo de embeddings
    embedding_model = OpenAIEmbeddings()

    # Crea vectorstore persistente desde documentos
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        persist_directory=persist_directory
    )

    return vectorstore

def get_retriever(vectorstore, k=6):
    # Crea un retriever para buscar los k documentos más relevantes
    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": k}
    )
    return retriever

if __name__ == "__main__":
    from splitter import split_documents
    from data_loader import load_all_docs_from_data

    docs = load_all_docs_from_data("data")
    chunks = split_documents(docs)

    vectorstore = create_vectorstore(chunks)
    retriever = get_retriever(vectorstore)

    # Test retriever con query de ejemplo
    query = "Stripe Integration"
    results = retriever.get_relevant_documents(query)

    print(f"Top {len(results)} chunks para query '{query}':")
    for i, doc in enumerate(results):
        print(f"--- Chunk {i+1} ---")
        print(doc.page_content[:300])
