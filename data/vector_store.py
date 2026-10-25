from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from data.document_loader import load_documents_from_uploads
from data.text_splitter import chunk_documents


def process_and_create_vectorstore(uploaded_files):
    """End-to-end pipeline: Loads, chunks, and embeds documents into a vector database."""
    # 1. Extract text
    raw_documents = load_documents_from_uploads(uploaded_files)

    # 2. Chunk text
    chunks = chunk_documents(raw_documents)

    # 3. Create embeddings and store in Chroma
    embeddings = OpenAIEmbeddings()
    vectorstore = Chroma.from_documents(documents=chunks, embedding=embeddings)

    return vectorstore
