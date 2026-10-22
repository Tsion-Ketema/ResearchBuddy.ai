import streamlit as st
import os
import tempfile
import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings


@st.cache_resource
def process_and_store_documents(uploaded_files):
    documents = []
    # 1. Temporarily save and load each uploaded file
    for file in uploaded_files:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(file.getvalue())
            tmp_path = tmp_file.name

        loader = PyPDFLoader(tmp_path)
        documents.extend(loader.load())
        os.remove(tmp_path)  # Clean up the temp file

    # 2. Split the text into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    chunks = text_splitter.split_documents(documents)

    # 3. Embed the chunks and load them into ChromaDB
    embeddings = OpenAIEmbeddings()
    vectorstore = Chroma.from_documents(documents=chunks, embedding=embeddings)

    return vectorstore


# Set your API key here (in production, use a .env file or Streamlit secrets!)
os.environ["OPENAI_API_KEY"] = "sk-your-openai-api-key-here"

# Configure the page to use the full width of the screen
st.set_page_config(layout="wide", page_title="RAG App")

# Create 3 vertical columns: Left (Chats - 20%), Middle (Q&A - 60%), Right (Files - 20%)
left_panel, middle_panel, right_panel = st.columns([1, 3, 1])

with left_panel:
    st.header("Chat History")
    st.button("New Chat +", use_container_width=True)
    st.write("---")
    st.write("Chat 1: Report Analysis")
    st.write("Chat 2: Financials Q3")

with right_panel:
    st.header("Files")
    uploaded_files = st.file_uploader(
        "Upload Reports", accept_multiple_files=True, type=["pdf", "txt", "csv"])
    st.write("---")
    if uploaded_files:
        for file in uploaded_files:
            st.write(f"📄 {file.name}")
            # Later, this is where we will trigger the RAG ingestion pipeline

with middle_panel:
    st.header("Q&A Interface")

    # Initialize chat history in session state
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Upload your reports on the right, then ask me anything!"}]

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("Ask a question about your reports..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Placeholder for RAG response
        with st.chat_message("assistant"):
            st.markdown(
                "This is where the LLM response will appear once we connect the RAG backend.")
        st.session_state.messages.append(
            {"role": "assistant", "content": "This is where the LLM response will appear once we connect the RAG backend."})
