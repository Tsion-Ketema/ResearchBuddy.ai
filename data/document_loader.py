from langchain_community.document_loaders import PyPDFLoader
from utils.temp_files import save_uploaded_file_temp


def load_documents_from_uploads(uploaded_files):
    """Extracts raw text documents from a list of Streamlit uploaded files."""
    documents = []
    for file in uploaded_files:
        with save_uploaded_file_temp(file) as tmp_path:
            loader = PyPDFLoader(tmp_path)
            documents.extend(loader.load())
    return documents
