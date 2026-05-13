import streamlit as st

def go_to_interview():
    """Navigates to the interview page."""
    st.switch_page("1_Interview")

def go_to_results():
    """Navigates to the results page."""
    st.switch_page("2_Results")

def go_to_home():
    """Navigates to the home page."""
    st.switch_page("app")
