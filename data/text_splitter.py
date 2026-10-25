from langchain_text_splitters import RecursiveCharacterTextSplitter
from config.settings import settings


def chunk_documents(documents):
    """Splits full documents into smaller chunks for vectorization."""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.CHUNK_SIZE,
        chunk_overlap=settings.CHUNK_OVERLAP
    )
    return text_splitter.split_documents(documents)
