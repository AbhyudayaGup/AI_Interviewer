import streamlit as st
from utils.ui import setup_page, display_header, display_footer


def main():
        """
        Main function for the welcome page of the application.
        Renders a modern hero with a primary CTA to begin the evaluation.
        """
        setup_page("TSRS Moulsari AI Disaster Preparedness Evaluator")

        # Minimal header (title is handled by CSS)
        display_header(show_title=False)

        # Hero section built with HTML for a modern look
        hero_html = '''
        <div class="hero">
            <div class="hero-content">
                <h1 class="hero-title">TSRS Moulsari — Disaster Preparedness Evaluator</h1>
                <p class="hero-sub">Realistic scenario interviews that assess readiness and provide actionable feedback.</p>
                <div class="hero-cta">
                    <!-- Placeholder for button - will use st.page_link below -->
                </div>
                <p class="hero-note">Voice-based interview • Secure • School-specific guidance</p>
            </div>
        </div>
        '''

        st.markdown(hero_html, unsafe_allow_html=True)
        
        # Use st.page_link for same-page navigation within Streamlit
        st.page_link("pages/1_Interview.py", label="🚀 Start Preparedness Evaluation", icon="▶️")

        # Footer
        display_footer()


if __name__ == "__main__":
        main()
