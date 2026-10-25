import streamlit as st
from data.vector_store import process_and_create_vectorstore


def render_file_panel():
    """Renders the right panel for document upload and triggers ingestion."""
    st.header("Files")
    uploaded_files = st.file_uploader(
        "Upload Research Papers",
        accept_multiple_files=True,
        type=["pdf"]
    )
    st.write("---")

    if uploaded_files:
        if st.button("Process Documents"):
            with st.spinner("Processing files and building database..."):
                # Call the pure data layer function
                vectorstore = process_and_create_vectorstore(uploaded_files)

                # Update UI state
                st.session_state.vectorstore = vectorstore
                st.success("Documents processed successfully!")

        for file in uploaded_files:
            st.write(f"📄 {file.name}")
