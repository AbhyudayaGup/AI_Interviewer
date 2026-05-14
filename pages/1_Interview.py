import streamlit as st
from utils.ui import setup_page, display_header, display_footer
from components.interview_session import run_interview_session

def interview_page():
    """
    Renders the main interview page.
    """
    setup_page("Interview Session")
    display_header(show_title=False) # Header is shown, but maybe a smaller version

    # Initialize session state for the interview
    if 'interview_started' not in st.session_state:
        st.session_state.interview_started = True
        st.session_state.messages = []
        st.session_state.question_index = 0
        st.session_state.user_responses = []
        st.session_state.evaluation_results = []
        # More initializations can go here
    # Ensure recording_state exists to avoid widget mutation errors
    if 'recording_state' not in st.session_state or not isinstance(st.session_state.recording_state, dict):
        st.session_state.recording_state = {}

    run_interview_session()
    
    # Display footer
    display_footer()
if __name__ == "__main__":
    interview_page()
