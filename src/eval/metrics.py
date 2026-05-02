from typing import Dict


def score_output(output: str) -> Dict[str, str]:
    """
    Assign simple qualitative scores to an LLM output.

    The scores are heuristic and are used for a first qualitative evaluation.
    """
    output_lower = output.lower()

    clarity = "high" if len(output.split()) >= 40 else "medium"

    faithfulness = "high"
    hallucination_risk = "low"

    hallucination_keywords = [
        "cooking",
        "sleeping",
        "watching tv",
        "working",
        "eating",
        "leaving the house",
    ]

    for keyword in hallucination_keywords:
        if keyword in output_lower:
            hallucination_risk = "medium"
            faithfulness = "medium"
            break

    behavior_inference = "high" if (
        "bedroom" in output_lower
        and ("kitchen" in output_lower or "living room" in output_lower)
    ) else "medium"

    return {
        "clarity": clarity,
        "faithfulness": faithfulness,
        "behavior_inference": behavior_inference,
        "hallucination_risk": hallucination_risk,
    }


def summarize_scores(scores: Dict[str, str]) -> str:
    """
    Create a short textual summary from qualitative scores.
    """
    return (
        f"Clarity: {scores['clarity']}; "
        f"Faithfulness: {scores['faithfulness']}; "
        f"Behavior inference: {scores['behavior_inference']}; "
        f"Hallucination risk: {scores['hallucination_risk']}."
    )