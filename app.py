import streamlit as st
import os
import tempfile
import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv


@st.cache_resource
def process_and_store_documents(uploaded_files):
    documents = []
    # 1. Temporarily save and load each uploaded file
    for file in uploaded_files:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(file.getvalue())
            tmp_path = tmp_file.name

        loader = PyPDFLoader(tmp_path)
        documents.extend(loader.load()) == []
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
load_dotenv()

# Configure the page to use the full width of the screen
st.set_page_config(layout="wide", page_title="Research Guide")

# Create 3 vertical columns: Left (Chats - 20%), Middle (Q&A - 60%), Right (Files - 20%)
left_panel, middle_panel, right_panel = st.columns([1, 3, 1])

with left_panel:
    st.header("Chat History")
    st.button("New Chat +", use_container_width=True)
    st.write("---")
    st.write("Chat 1: Report Analysis")
    st.write("Chat 2: Financials Q3")

# 2. RIGHT PANEL (Files)
with right_panel:
    st.header("Files")
    uploaded_files = st.file_uploader(
        "Upload Research Papers", accept_multiple_files=True, type=["pdf"])
    st.write("---")

    if uploaded_files:
        # The missing button logic is added here
        if st.button("Process Documents"):
            with st.spinner("Processing files and building database..."):
                # Run the ingestion function
                vectorstore = process_and_store_documents(uploaded_files)
                # Save the database to session state so the chat can use it later
                st.session_state.vectorstore = vectorstore
                st.success("Documents processed successfully!")

        for file in uploaded_files:
            st.write(f"📄 {file.name}")

with middle_panel:
    st.header("Research Guide Q&A")

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
        # 1. Display user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # 2. Generate and display the AI response
        with st.chat_message("assistant"):
            # Check if the user has processed documents yet
            if "vectorstore" not in st.session_state:
                st.warning(
                    "Please upload and process a report on the right before asking questions.")
                st.session_state.messages.append(
                    {"role": "assistant", "content": "Please upload and process a report first."})
            else:
                with st.spinner("Thinking..."):
                    # Initialize the LLM
                    llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)

                    # Define how the AI should answer
                    system_prompt = (
                        "You are an expert research assistant helping a user analyze multiple documents. "
                        "Use the provided context to answer the user's questions thoroughly and accurately. "
                        "Synthesize information across different parts of the context if necessary. "
                        "If the answer is not contained within the provided context, state clearly that you cannot find the answer in the current documents. "
                        "Do not hallucinate or guess.\n\n"
                        "Context:\n{context}"

                        # """You are a helpful research assistant.
                        # First, try to answer the user's question using the provided context.
                        # If the context does not contain the answer, you may use your general knowledge to answer,
                        # but you must clearly state that you are answering from general knowledge and not from the uploaded reports."""
                    )

                    prompt_template = ChatPromptTemplate.from_messages([
                        ("system", system_prompt),
                        ("human", "{input}"),
                    ])

                    # Create the chains
                    question_answer_chain = create_stuff_documents_chain(
                        llm, prompt_template)
                    rag_chain = create_retrieval_chain(
                        st.session_state.vectorstore.as_retriever(), question_answer_chain)

                    # Run the query
                    response = rag_chain.invoke({"input": prompt})
                    answer = response["answer"]

                    # Display and save the answer
                    st.markdown(answer)
                    st.session_state.messages.append(
                        {"role": "assistant", "content": answer})
