import streamlit as st
from config.settings import load_config
from ui.sidebar import render_sidebar
from ui.file_uploader import render_file_panel
from ui.chat_interface import render_chat_panel


def main():
    # 1. Initialize environment and configuration
    load_config()

    # 2. Configure global page settings
    st.set_page_config(layout="wide", page_title="Research_Buddy")

    # 3. Define the layout grid
    left_panel, middle_panel, right_panel = st.columns([1, 3, 1])

    # 4. Render UI Components
    with left_panel:
        render_sidebar()

    with right_panel:
        render_file_panel()

    with middle_panel:
        render_chat_panel()


if __name__ == "__main__":
    main()
