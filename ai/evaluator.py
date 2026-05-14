from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os
from dotenv import load_dotenv

load_dotenv()

def get_llm():
    """Initializes and returns the LLM instance."""
    # Using Groq for fast inference. Ensure GROQ_API_KEY is in .env
    # Previous models (llama3-8b-8192, mixtral-8x7b-32768) were decommissioned
    # Using the latest available model: llama-3.1-8b-instant
    return ChatGroq(temperature=0, model_name="llama-3.1-8b-instant")

def evaluate_response(question_data, user_response):
    """
    Evaluates a user's response against the question's rubric using an LLM.
    
    Args:
        question_data (dict): The dictionary containing the question, rubric, etc.
        user_response (str): The user's transcribed answer.
        
    Returns:
        dict: A structured evaluation of the response.
    """
    llm = get_llm()
    
    prompt_template = ChatPromptTemplate.from_template(
        """
        You are an expert AI evaluator for a school's disaster preparedness program.
        Your task is to evaluate a user's response to a scenario-based question.
        Be strict, fair, and focus on safety.

        **Scenario:** {scenario}
        **Question:** {question}

        **Evaluation Rubric:**
        - **Ideal Concepts:** {ideal_concepts}
        - **Dangerous Misconceptions:** {dangerous_misconceptions}

        **User's Answer:**
        "{user_response}"

        **Your Task:**
        1.  **Score each category** from 0 to 100 based on how well the user's answer aligns with the ideal concepts and avoids dangerous misconceptions.
        2.  **Identify Strengths:** Briefly list what the user answered correctly.
        3.  **Identify Weaknesses:** Briefly list what the user missed or got wrong.
        4.  **Detect Misconceptions:** List any dangerous misconceptions the user mentioned.
        5.  **Provide a score for the overall response** from 0 to 100.

        **Output Format (Strictly JSON):**
        {{
            "category_scores": {{
                "Safety Awareness": <score_0_100>,
                "Procedural Correctness": <score_0_100>,
                "Calmness": <score_0_100_based_on_clarity_and_confidence>,
                "Communication Understanding": <score_0_100>
            }},
            "strengths": "<strengths_summary>",
            "weaknesses": "<weaknesses_summary>",
            "misconceptions_detected": ["<misconception_1>", "<misconception_2>"],
            "overall_score": <score_0_100>,
            "follow_up_guidance": "<follow_up_guidance>"
        }}
        """
    )
    
    chain = prompt_template | llm | StrOutputParser()
    
    response_str = chain.invoke({
        "scenario": question_data['scenario'],
        "question": question_data['question'],
        "ideal_concepts": question_data['evaluation_rubric']['ideal_concepts'],
        "dangerous_misconceptions": question_data['evaluation_rubric']['dangerous_misconceptions'],
        "user_response": user_response,
        "follow_up_guidance": question_data.get('follow_up_guidance', '')
    })
    
    try:
        import json
        # The output from LLM might have extra text, so we find the JSON part.
        json_start = response_str.find('{')
        json_end = response_str.rfind('}') + 1
        clean_json_str = response_str[json_start:json_end]
        evaluation = json.loads(clean_json_str)
        evaluation['category'] = question_data['category'] # Add category for final report
        # Also include any follow-up guidance from the question metadata
        evaluation['follow_up_guidance'] = question_data.get('follow_up_guidance', '')

        # Sanitize any undesired phrases (e.g., "communication tree") from text outputs
        import re
        banned_phrases = [r"communication tree"]
        def sanitize_text(text: str) -> str:
            if not isinstance(text, str):
                return text
            out = text
            for p in banned_phrases:
                out = re.sub(p, 'school emergency contact list', out, flags=re.I)
            return out

        # Apply sanitization to textual fields
        if 'strengths' in evaluation:
            evaluation['strengths'] = sanitize_text(evaluation['strengths'])
        if 'weaknesses' in evaluation:
            evaluation['weaknesses'] = sanitize_text(evaluation['weaknesses'])
        if 'misconceptions_detected' in evaluation:
            evaluation['misconceptions_detected'] = [sanitize_text(m) for m in evaluation['misconceptions_detected']]
        # preserve follow_up_guidance from question metadata if present but sanitize
        evaluation['follow_up_guidance'] = sanitize_text(question_data.get('follow_up_guidance', ''))

        return evaluation
    except (json.JSONDecodeError, IndexError) as e:
        print(f"Failed to parse LLM response into JSON: {e}")
        print(f"Raw response: {response_str}")
        # Return a default error structure
        return {
            "category_scores": {"Safety Awareness": 0, "Procedural Correctness": 0, "Calmness": 0, "Communication Understanding": 0},
            "strengths": "Evaluation failed.",
            "weaknesses": "Could not parse the AI's response. This might be a temporary issue.",
            "misconceptions_detected": [],
            "overall_score": 0,
            "category": question_data['category']
        }
