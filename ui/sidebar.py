import streamlit as st


def render_sidebar():
    """Renders the left navigation panel."""
    st.header("Chat History")
    st.button("New Chat +", use_container_width=True)
    st.write("---")

    # Placeholders for future database/history integration
    st.write("Chat 1: Report Analysis")
    st.write("Chat 2: Financials Q3")
