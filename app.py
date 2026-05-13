import streamlit as st
from utils.ui import setup_page, display_header, display_welcome_message

def main():
    """
    Main function for the welcome page of the application.
    """
    setup_page("TSRS Moulsari AI Disaster Preparedness Evaluator")

    display_header()
    display_welcome_message()

    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.page_link("pages/1_Interview.py", label="🎤 Start Preparedness Evaluation", icon="▶️")

    # You can add more elements to the welcome page here
    # For example, a brief overview of the process or some graphics.

if __name__ == "__main__":
    main()
