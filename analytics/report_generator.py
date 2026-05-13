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
    
    recommendations = "Based on your answers, focus on the areas listed under 'Areas for Improvement'. A detailed review of the school's official emergency protocols is highly recommended."

    return {
        'overall_score': overall_score,
        'category_scores': final_category_scores,
        'strengths': strengths,
        'weaknesses': weaknesses,
        'recommendations': recommendations,
        'misconceptions_detected': list(set(misconceptions)) # Unique misconceptions
    }
