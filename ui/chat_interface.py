import streamlit as st
from core.rag_orchestrator import ask_question


def render_chat_interface():
    st.header("Research Guide Q&A")

    # Initialize session state if it doesn't exist
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant",
                "content": "Upload your reports on the right, then ask me anything!"}
        ]

    # 1. Create a dedicated container for ALL messages
    chat_container = st.container()

    # 2. Draw historical messages INSIDE the container
    with chat_container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # 3. The input box sits independently BELOW the container
    if prompt := st.chat_input("Ask a question about your reports..."):

        # 4. Force new messages to render INSIDE the container (above the input box)
        with chat_container:

            # Add and show user message
            st.session_state.messages.append(
                {"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            # Add and show AI response
            with st.chat_message("assistant"):

                # GUARD CLAUSE: Ensure vectorstore exists before calling the AI
                if "vectorstore" not in st.session_state:
                    error_msg = "Please upload and process a report on the right before asking questions."
                    st.warning(error_msg)
                    st.markdown(error_msg)
                    st.session_state.messages.append(
                        {"role": "assistant", "content": error_msg})

                # REAL AI LOGIC
                else:
                    with st.spinner("Analyzing documents..."):
                        # Call your actual backend function
                        answer = ask_question(
                            st.session_state.vectorstore, prompt)

                        # Display and save the real answer
                        st.markdown(answer)
                        st.session_state.messages.append(
                            {"role": "assistant", "content": answer})
