import streamlit as st
import os

def load_css(file_name):
    """Loads a CSS file into the Streamlit app."""
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def setup_page(title):
    """Configures the page with a title and loads custom CSS."""
    # Use an emoji icon (Streamlit page_icon must be emoji or emoji code)
    st.set_page_config(page_title=title, page_icon="🛡️", layout="wide", initial_sidebar_state="collapsed")
    
    # Load custom CSS
    css_file = os.path.join("styles", "main.css")
    if os.path.exists(css_file):
        load_css(css_file)

def display_header(show_title=True):
    """Displays the main header of the application."""
    if show_title:
        st.markdown('<p class="title">TSRS Moulsari AI Disaster Preparedness Evaluator</p>', unsafe_allow_html=True)
    st.markdown('<hr style="height:2px;border:none;color:#333;background-color:#333;" />', unsafe_allow_html=True)


def display_welcome_message():
    """Displays the introductory message on the welcome page."""
    st.markdown(
        """
        <div style="text-align: center; font-size: 1.1rem; margin: 2rem 0;">
            This AI-powered system evaluates how prepared students and staff are to respond during emergencies 
            and disaster situations at The Shri Ram School Moulsari. The interview simulates realistic 
            scenarios such as earthquakes, fires, cybersecurity incidents, and lockdowns. Based on your 
            responses, the AI estimates your preparedness level and provides personalized feedback.
        </div>
        """,
        unsafe_allow_html=True
    )

def display_footer():
    """Renders a small footer at the bottom of the page."""
    footer_html = """
    <div class="site-footer">
        Made with care by Abhyudaya — TSRS Moulsari AI Project
        &nbsp;&middot;&nbsp;
        <a href="https://github.com/abhyudayagup" target="_blank" rel="noreferrer">GitHub</a>
    </div>
    """
    st.markdown(footer_html, unsafe_allow_html=True)
