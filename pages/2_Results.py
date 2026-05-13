import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from utils.ui import setup_page, display_header
from analytics.report_generator import generate_final_report

def results_page():
    """
    Renders the results and analytics dashboard page.
    """
    setup_page("Your Preparedness Report")
    display_header(show_title=False)

    st.title("Your Preparedness Report")

    if 'final_report' not in st.session_state:
        st.warning("No report found. Please complete the interview first.")
        if st.button("Back to Home"):
            st.switch_page("app.py")
        return

    report = st.session_state.final_report

    # Display Overall Score
    st.metric(label="Overall Preparedness Score", value=f"{report['overall_score']}%")

    # Create two columns for the radar chart and category scores
    col1, col2 = st.columns([2, 1])

    with col1:
        # Radar Chart
        st.subheader("Preparedness Profile")
        categories = list(report['category_scores'].keys())
        scores = list(report['category_scores'].values())
        
        fig = go.Figure()

        fig.add_trace(go.Scatterpolar(
            r=scores,
            theta=categories,
            fill='toself',
            name='Your Score'
        ))

        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )),
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Category Scores
        st.subheader("Category Scores")
        for category, score in report['category_scores'].items():
            st.metric(label=category, value=f"{score}%")

    # Strengths and Weaknesses
    st.subheader("AI-Generated Feedback")
    st.success(f"**Strengths:** {report['strengths']}")
    st.warning(f"**Areas for Improvement:** {report['weaknesses']}")

    # Recommendations
    st.subheader("Personalized Recommendations")
    st.info(report['recommendations'])
    
    # Misconceptions
    if report['misconceptions_detected']:
        st.subheader("Critical Misconceptions Detected")
        for mc in report['misconceptions_detected']:
            st.error(mc)

    if st.button("Restart Interview"):
        # Clear session state to allow for a new interview
        for key in st.session_state.keys():
            del st.session_state[key]
        st.switch_page("app.py")


if __name__ == "__main__":
    # Mock data for testing the results page directly
    if 'final_report' not in st.session_state:
        st.session_state.final_report = {
            'overall_score': 85,
            'category_scores': {
                'Safety Awareness': 90,
                'Procedural Correctness': 80,
                'Calmness': 95,
                'Communication': 75,
                'Cybersecurity': 85,
                'Evacuation': 90,
            },
            'strengths': "Excellent awareness of immediate safety protocols and maintaining a calm demeanor.",
            'weaknesses': "Could improve on specific communication protocols and remembering exact evacuation routes.",
            'recommendations': "Review the school's communication tree for emergencies. Take a walk along the primary and secondary evacuation routes from your most frequent locations.",
            'misconceptions_detected': ["Mentioned using an elevator during a fire alarm, which is extremely dangerous."]
        }
    results_page()
