import os
import tempfile
import streamlit as st
import time
from questions.question_loader import load_questions
from audio.recorder import record_audio_non_blocking
import audio.recorder as recorder
from audio.transcriber import transcribe_audio
from ai.evaluator import evaluate_response
from analytics.report_generator import generate_final_report

def run_interview_session():
    """
    Manages the state and flow of the AI interview.
    """
    # normal interview flow
    if 'questions' not in st.session_state:
        st.session_state.questions = load_questions(num_questions=4)
    
    questions = st.session_state.questions
    q_index = st.session_state.get('question_index', 0)

    if q_index >= len(questions):
        # Interview finished, generate report and go to results
        with st.spinner("Generating your final preparedness report..."):
            st.session_state.final_report = generate_final_report(st.session_state.evaluation_results)
        # Use explicit relative file path for switch_page to avoid "Could not find page" errors
        st.switch_page("pages/2_Results.py")
        return

    current_question = questions[q_index]

    st.subheader(f"Question {q_index + 1} of {len(questions)}")
    st.markdown(f"**Category:** {current_question['category']}")
    st.markdown(f"**Scenario:** {current_question['scenario']}")
    st.write(current_question['question'])

    # Voice Interaction
    recording_key = f"q_{q_index}"
    rec_state = {"status": "idle"}
    audio_supported = recorder.can_use_microphone()

    if audio_supported:
        st.write("Click the button and speak your answer.")
        
        # Initialize recording state dict for this session
        if 'recording_state' not in st.session_state:
            st.session_state.recording_state = {}

        rec_state = st.session_state.recording_state.get(recording_key, {"status": "idle", "start_time": None, "audio_path": None})

        # Start recording
        if rec_state["status"] == "idle":
            if st.button("🎤 Record Answer", key=f"record_{q_index}"):
                # Kick off non-blocking recording
                recorded = recorder.record_audio_non_blocking(max_duration=15)
                if not recorded:
                    st.error("Microphone recording is unavailable on this platform.")
                    return
                rec_state["status"] = "recording"
                rec_state["start_time"] = time.time()
                st.session_state.recording_state[recording_key] = rec_state
                st.rerun()
    else:
        st.warning(
            "Microphone recording is unavailable on deployed Streamlit. "
            "Please type your answer below or upload a recorded audio file."
        )
        uploaded_file = st.file_uploader(
            "Upload your recorded answer (optional)",
            type=["wav", "mp3", "m4a"],
            key=f"upload_{q_index}"
        )
        if uploaded_file is not None:
            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as temp_audio:
                temp_audio.write(uploaded_file.read())
                temp_audio_path = temp_audio.name
            transcript = transcribe_audio(temp_audio_path)
            if transcript and not transcript.startswith("Error"):
                st.session_state.transcript = transcript
                st.success("Uploaded audio transcribed successfully.")
            else:
                st.error("Transcription failed. Please try another file or type your answer manually.")

        manual_answer = st.text_area(
            "Type your answer here:",
            value=st.session_state.get(f"manual_{q_index}", ""),
            key=f"manual_{q_index}",
            height=200
        )
        if manual_answer and manual_answer.strip():
            st.session_state.transcript = manual_answer

    # Recording UI and stop control
    if rec_state["status"] == "recording":
        elapsed = time.time() - (rec_state.get("start_time") or time.time())
        max_duration = 15
        # Show recording message
        st.info(f"🔴 Recording... {int(max_duration - elapsed)}s remaining. Click 'Stop Recording' to finish early.")

        if st.button("⏹️ Stop Recording", key=f"stop_{q_index}"):
            try:
                recorder.set_stop_flag()
            except Exception:
                # Best-effort: set a fallback session flag
                st.session_state.stop_recording = True

            rec_state["status"] = "stopping"
            st.session_state.recording_state[recording_key] = rec_state
            st.rerun()

        # Auto-timeout handling: if recorder reports stopped or elapsed > max, move on
        if elapsed > max_duration or (not recorder.is_recording() and rec_state["status"] == "recording"):
            rec_state["status"] = "stopping"
            st.session_state.recording_state[recording_key] = rec_state
            st.rerun()

    # Finalize recording: save file and transcribe
    if rec_state["status"] == "stopping":
        with st.spinner("Finalizing recording and transcribing..."):
            audio_path = recorder.save_recording()
            if not audio_path:
                st.error("Failed to save recording. Please try again.")
                rec_state["status"] = "idle"
                st.session_state.recording_state[recording_key] = rec_state
                st.rerun()
                return

            # Transcribe
            transcript = transcribe_audio(audio_path)
            if transcript and not transcript.startswith("Error"):
                st.session_state.transcript = transcript
                rec_state["status"] = "done"
                rec_state["audio_path"] = audio_path
                st.session_state.recording_state[recording_key] = rec_state
                st.rerun()
                return
            else:
                st.error("No speech detected or transcription failed. Please try again.")
                rec_state["status"] = "idle"
                st.session_state.recording_state[recording_key] = rec_state
                st.rerun()
                return

    # Display and allow editing of transcript
    if 'transcript' in st.session_state:
        st.success("✓ Recording transcribed successfully")
        edited_transcript = st.text_area("Your transcribed answer (edit if needed):", st.session_state.transcript, height=150, key=f"textarea_{q_index}")

        if st.button("Submit Answer", key=f"submit_{q_index}"):
            if not edited_transcript or len(edited_transcript.strip()) == 0:
                st.error("Please provide an answer before submitting.")
            else:
                with st.spinner("AI is evaluating your response..."):
                    evaluation = evaluate_response(current_question, edited_transcript)
                    st.session_state.evaluation_results.append(evaluation)
                
                # Clear state for this question and move to next
                if 'transcript' in st.session_state:
                    del st.session_state.transcript
                if recording_key in st.session_state.recording_state:
                    del st.session_state.recording_state[recording_key]
                
                st.session_state.question_index += 1
                st.rerun()
