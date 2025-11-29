import re
from typing import Dict, List, Tuple

def explain_prediction(text: str, predict_func) -> List[Tuple[str, float]]:
    """
    Simulates LIME (Local Interpretable Model-agnostic Explanations).
    
    Args:
        text: The input text.
        predict_func: A function that takes text and returns a dict with 'spam_probability'.
        
    Returns:
        List of (word, contribution_score) tuples.
        Positive score = contributes to SPAM.
        Negative score = contributes to HAM.
    """
    original_prob = predict_func(text)['spam_probability']
    words = re.findall(r'\w+', text.lower())
    unique_words = set(words)
    
    contributions = []
    
    for word in unique_words:
        # Remove word and re-predict
        # We use a simple regex replace for the simulation
        modified_text = re.sub(r'\b' + re.escape(word) + r'\b', '', text, flags=re.IGNORECASE)
        new_prob = predict_func(modified_text)['spam_probability']
        
        # If prob drops significantly when word is removed, it was contributing to SPAM
        # If prob increases, it was contributing to HAM (keeping it safe)
        contribution = original_prob - new_prob
        
        if abs(contribution) > 0.01: # Filter noise
            contributions.append((word, contribution))
            
    # Sort by absolute contribution
    contributions.sort(key=lambda x: abs(x[1]), reverse=True)
    return contributions[:10] # Top 10 features
