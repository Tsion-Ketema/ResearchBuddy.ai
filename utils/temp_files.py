import os
import tempfile
from contextlib import contextmanager


@contextmanager
def save_uploaded_file_temp(uploaded_file):
    """Context manager to temporarily save a Streamlit UploadedFile to disk and auto-clean it."""
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_path = tmp_file.name
        yield tmp_path
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
