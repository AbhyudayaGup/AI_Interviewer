import streamlit as st
import time
from questions.question_loader import load_questions
from audio.recorder import record_audio
from audio.transcriber import transcribe_audio
from ai.evaluator import evaluate_response
from analytics.report_generator import generate_final_report

def run_interview_session():
    """
    Manages the state and flow of the AI interview.
    """
    if 'questions' not in st.session_state:
        st.session_state.questions = load_questions(num_questions=4)
    
    questions = st.session_state.questions
    q_index = st.session_state.get('question_index', 0)

    if q_index >= len(questions):
        # Interview finished, generate report and go to results
        with st.spinner("Generating your final preparedness report..."):
            st.session_state.final_report = generate_final_report(st.session_state.evaluation_results)
        st.switch_page("pages/2_Results.py")
        return

    current_question = questions[q_index]

    st.subheader(f"Question {q_index + 1} of {len(questions)}")
    st.markdown(f"**Category:** {current_question['category']}")
    st.markdown(f"**Scenario:** {current_question['scenario']}")
    st.write(current_question['question'])

    # Voice Interaction
    st.write("Click the button and speak your answer.")
    if st.button("Record Answer", key=f"record_{q_index}"):
        with st.spinner("Recording..."):
            audio_file = record_audio()
        if audio_file:
            with st.spinner("Transcribing your answer..."):
                transcript = transcribe_audio(audio_file)
            st.session_state.transcript = transcript

    # Display and allow editing of transcript
    if 'transcript' in st.session_state:
        edited_transcript = st.text_area("Your transcribed answer (edit if needed):", st.session_state.transcript, height=150)

        if st.button("Submit Answer", key=f"submit_{q_index}"):
            with st.spinner("AI is evaluating your response..."):
                evaluation = evaluate_response(current_question, edited_transcript)
                st.session_state.evaluation_results.append(evaluation)
            
            # Move to next question
            st.session_state.question_index += 1
            del st.session_state.transcript # Clear transcript for next question
            st.rerun()
