import numpy as np

def generate_final_report(evaluation_results):
    """
    Aggregates individual evaluation results into a final report.
    
    Args:
        evaluation_results (list): A list of evaluation dictionaries from the AI.
        
    Returns:
        dict: A final, comprehensive report.
    """
    if not evaluation_results:
        return {
            'overall_score': 0,
            'category_scores': {},
            'strengths': "No responses were evaluated.",
            'weaknesses': "Please complete the interview to get a report.",
            'recommendations': "Start the interview to assess your preparedness.",
            'misconceptions_detected': []
        }

    # Aggregate scores
    overall_scores = [r['overall_score'] for r in evaluation_results]
    overall_score = int(np.mean(overall_scores))

    # Aggregate category scores
    agg_category_scores = {}
    for result in evaluation_results:
        for category, score in result.get('category_scores', {}).items():
            if category not in agg_category_scores:
                agg_category_scores[category] = []
            agg_category_scores[category].append(score)
    
    final_category_scores = {cat: int(np.mean(scores)) for cat, scores in agg_category_scores.items()}

    # Aggregate text feedback
    strengths = " ".join([r['strengths'] for r in evaluation_results])
    weaknesses = " ".join([r['weaknesses'] for r in evaluation_results])
    misconceptions = [mc for r in evaluation_results for mc in r.get('misconceptions_detected', [])]

    # TODO: Use an LLM to summarize the aggregated text for a more coherent report
    # For now, we just combine them.
    
    # Base recommendations (avoid the phrase 'communication tree')
    recommendations = "Based on your answers, focus on the areas listed under 'Areas for Improvement'. Review the school's official emergency protocols and contact lists."

    # Include any question-specific follow-up guidance (e.g., contact a staff member)
    follow_up_notes = [r.get('follow_up_guidance') for r in evaluation_results if r.get('follow_up_guidance')]
    if follow_up_notes:
        # sanitize any banned phrases in follow-up notes
        import re
        banned_phrases = [r"communication tree"]
        sanitized_notes = []
        for n in follow_up_notes:
            s = n
            for p in banned_phrases:
                s = re.sub(p, 'school emergency contact list', s, flags=re.I)
            sanitized_notes.append(s)
        recommendations += "\n\nFollow-up guidance: " + "; ".join(sanitized_notes)

    # Apply a harsher penalty based on detected misconceptions so low scores show up more easily
    penalty_per_misconception = 5
    total_misconceptions = len(misconceptions)
    penalty = min(25, penalty_per_misconception * total_misconceptions)

    # Reduce overall score and category scores by the penalty (but not below 0)
    overall_score = max(0, overall_score - penalty)
    penalized_category_scores = {}
    for cat, score in final_category_scores.items():
        penalized = max(0, int(score - penalty))
        penalized_category_scores[cat] = penalized

    # Sanitize text fields to remove banned phrases
    import re
    banned_phrases = [r"communication tree"]
    def sanitize_text(text: str) -> str:
        if not isinstance(text, str):
            return text
        out = text
        for p in banned_phrases:
            out = re.sub(p, 'school emergency contact list', out, flags=re.I)
        return out

    strengths = sanitize_text(strengths)
    weaknesses = sanitize_text(weaknesses)

    return {
        'overall_score': overall_score,
        'category_scores': penalized_category_scores,
        'strengths': strengths,
        'weaknesses': weaknesses,
        'recommendations': recommendations,
        'misconceptions_detected': list(set(misconceptions)) # Unique misconceptions
    }
