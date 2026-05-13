import streamlit as st
from utils.ui import setup_page, display_header, display_welcome_message
from utils.navigation import go_to_interview

def main():
    """
    Main function for the welcome page of the application.
    """
    setup_page("TSRS Moulsari AI Disaster Preparedness Evaluator")

    display_header()
    display_welcome_message()

    if st.button("Start Preparedness Evaluation", key="start_interview_button"):
        go_to_interview()

    # You can add more elements to the welcome page here
    # For example, a brief overview of the process or some graphics.

if __name__ == "__main__":
    main()
