import streamlit as st

def go_to_interview():
    """Navigates to the interview page."""
    st.switch_page("pages/1_Interview.py")

def go_to_results():
    """Navigates to the results page."""
    st.switch_page("pages/2_Results.py")

def go_to_home():
    """Navigates to the home page."""
    st.switch_page("app.py")
