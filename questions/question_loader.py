import os
import glob
import random
import json
import yaml

def parse_markdown_question(file_path):
    """
    Parses a markdown file with YAML front matter into a structured question dictionary.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split by --- to separate YAML front matter from content
    parts = content.split('---')
    if len(parts) < 3:
        return get_default_question()
    
    # Parse YAML front matter
    try:
        metadata = yaml.safe_load(parts[1])
    except:
        metadata = {}
    
    # Parse markdown content
    md_content = parts[2]
    lines = md_content.split('\n')
    
    scenario = ""
    question_text = ""
    ideal_concepts = ""
    dangerous_misconceptions = ""
    
    # State machine to parse sections
    current_section = None
    section_content = []
    
    for line in lines:
        if line.startswith('### Scenario'):
            if current_section and section_content:
                if current_section == 'scenario':
                    scenario = ' '.join(section_content).strip()
                elif current_section == 'question':
                    question_text = ' '.join(section_content).strip()
            current_section = 'scenario'
            section_content = []
        elif line.startswith('### Question'):
            if current_section == 'scenario':
                scenario = ' '.join(section_content).strip()
            current_section = 'question'
            section_content = []
        elif line.startswith('#### Ideal Concepts'):
            if current_section == 'question':
                question_text = ' '.join(section_content).strip()
            current_section = 'ideal'
            section_content = []
        elif line.startswith('#### Dangerous Misconceptions'):
            current_section = 'dangerous'
            section_content = []
        elif current_section and line.strip() and not line.startswith('#'):
            section_content.append(line.strip())
    
    # Get the last section
    if current_section == 'scenario':
        scenario = ' '.join(section_content).strip()
    elif current_section == 'question':
        question_text = ' '.join(section_content).strip()
    elif current_section == 'ideal':
        ideal_concepts = ' '.join(section_content).strip()
    elif current_section == 'dangerous':
        dangerous_misconceptions = ' '.join(section_content).strip()

    return {
        "id": metadata.get('id', hash(file_path) % 10000),
        "category": metadata.get('category', 'General'),
        "scenario": scenario,
        "question": question_text,
        "evaluation_rubric": {
            "ideal_concepts": ideal_concepts or "Look for safe, prepared responses.",
            "dangerous_misconceptions": dangerous_misconceptions or "Avoid risky or harmful actions."
        },
        "follow_up_guidance": ""
    }

def get_default_question():
    """Returns a default question when parsing fails."""
    return {
        "id": 0,
        "category": "General",
        "scenario": "Sample Scenario",
        "question": "What would you do in this situation?",
        "evaluation_rubric": {
            "ideal_concepts": "Think about safety first.",
            "dangerous_misconceptions": "Avoid taking risks."
        },
        "follow_up_guidance": ""
    }

def load_questions(questions_dir="questions", num_questions=4):
    """
    Loads, parses, and randomly selects a number of questions from the questions directory.
    """
    # Find all markdown files but exclude any flood-related questions
    all_question_files = [f for f in glob.glob(os.path.join(questions_dir, "*.md")) if 'flood' not in os.path.basename(f).lower()]
    
    if not all_question_files:
        # Return a default question if none are found
        return [{
            'id': 0, 'category': 'Default', 'scenario': 'No questions found.',
            'question': 'Please check the /questions directory.',
            'evaluation_rubric': {'ideal_concepts': '', 'dangerous_misconceptions': ''},
            'follow_up_guidance': ''
        }]

    parsed_questions = [parse_markdown_question(f) for f in all_question_files]
    
    # Randomly select `num_questions`
    num_to_select = min(num_questions, len(parsed_questions))
    selected_questions = random.sample(parsed_questions, num_to_select)
    
    return selected_questions
