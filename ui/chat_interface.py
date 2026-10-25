import streamlit as st
from core.rag_orchestrator import ask_question


def render_chat_panel():
    """Renders the central chat interface and handles user interactions."""
    st.header("Research Guide Q&A")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant",
                "content": "Upload your reports on the right, then ask me anything!"}
        ]

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Handle new input
    if prompt := st.chat_input("Ask a question about your reports..."):
        _handle_user_input(prompt)


def _handle_user_input(prompt: str):
    """Internal helper to process a submitted chat message."""
    # 1. Render and save user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Guard clause: Ensure vectorstore exists
    if "vectorstore" not in st.session_state:
        _render_assistant_message("Please upload and process a report first.")
        st.warning(
            "Please upload and process a report on the right before asking questions.")
        return

    # 3. Generate response via Core layer
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            answer = ask_question(st.session_state.vectorstore, prompt)
            st.markdown(answer)
            st.session_state.messages.append(
                {"role": "assistant", "content": answer})


def _render_assistant_message(content: str):
    """Internal helper to render and save an assistant message directly."""
    st.session_state.messages.append({"role": "assistant", "content": content})
    with st.chat_message("assistant"):
        st.markdown(content)
