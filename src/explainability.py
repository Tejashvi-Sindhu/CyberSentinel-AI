"""Human-readable explanations for model output."""
def explain_prediction(label: str, probability: float) -> str:
    return f"The model predicted {label} with a reported model score of {probability:.1%}. Review the original traffic and supporting evidence before taking action."
