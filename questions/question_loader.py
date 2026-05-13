import os
import glob
import random
import markdown

def parse_markdown_question(file_path):
    """
    Parses a single markdown file into a structured question dictionary.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # A simple parser based on "---" separators
    parts = content.split('---')
    
    # Metadata
    md = markdown.Markdown(extensions=['meta'])
    md.convert(parts[1])
    metadata = md.meta
    
    # Main content
    main_content = parts[2].strip()
    scenario_question_split = main_content.split('### Question')
    scenario = scenario_question_split[0].replace('### Scenario', '').strip()
    question = scenario_question_split[1].strip()

    # Rubric and Follow-up
    rubric_followup_split = parts[3].strip().split('### Follow-up Guidance')
    rubric_text = rubric_followup_split[0].replace('### Evaluation Rubric', '').strip()
    follow_up = rubric_followup_split[1].strip() if len(rubric_followup_split) > 1 else ""

    # Parse rubric
    ideal_concepts_split = rubric_text.split('#### Dangerous Misconceptions:')
    ideal_concepts = ideal_concepts_split[0].replace('#### Ideal Concepts to Mention:', '').strip()
    dangerous_misconceptions = ideal_concepts_split[1].strip()

    return {
        'id': metadata.get('id', [None])[0],
        'category': metadata.get('category', ["General"])[0],
        'scenario': scenario,
        'question': question,
        'evaluation_rubric': {
            'ideal_concepts': ideal_concepts,
            'dangerous_misconceptions': dangerous_misconceptions
        },
        'follow_up_guidance': follow_up
    }

def load_questions(questions_dir="questions", num_questions=4):
    """
    Loads, parses, and randomly selects a number of questions from the questions directory.
    """
    all_question_files = glob.glob(os.path.join(questions_dir, "*.md"))
    
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
