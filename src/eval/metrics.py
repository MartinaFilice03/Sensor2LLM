from typing import Dict


def compute_sentence_length(output: str) -> float:
    sentences = [s for s in output.split(".") if s.strip()]

    if not sentences:
        return 0.0

    total_words = sum(len(sentence.split()) for sentence in sentences)

    return round(total_words / len(sentences), 2)


def count_active_rooms(output: str) -> int:
    rooms = [
        "bedroom",
        "bathroom",
        "kitchen",
        "living room",
        "dining room",
        "work area",
        "lounge chair",
        "outside door",
    ]

    output_lower = output.lower()

    return sum(1 for room in rooms if room in output_lower)


def compute_temporal_coverage(output: str) -> str:
    output_lower = output.lower()

    time_keywords = [
        "during",
        "later",
        "then",
        "after",
        "before",
        "at",
        "over time",
    ]

    count = sum(1 for word in time_keywords if word in output_lower)

    if count >= 4:
        return "high"

    if count >= 2:
        return "medium"

    return "low"


def compute_movement_density(output: str) -> str:
    movement_words = [
        "movement",
        "activity",
        "transition",
        "motion",
        "detected",
    ]

    output_lower = output.lower()

    count = sum(output_lower.count(word) for word in movement_words)

    if count >= 8:
        return "high"

    if count >= 3:
        return "medium"

    return "low"


def score_output(output: str) -> Dict[str, object]:
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

    behavior_inference = (
        "high"
        if (
            "bedroom" in output_lower
            and (
                "kitchen" in output_lower
                or "living room" in output_lower
            )
        )
        else "medium"
    )

    return {
        "clarity": clarity,
        "faithfulness": faithfulness,
        "behavior_inference": behavior_inference,
        "hallucination_risk": hallucination_risk,
        "sentence_length": compute_sentence_length(output),
        "active_rooms": count_active_rooms(output),
        "temporal_coverage": compute_temporal_coverage(output),
        "movement_density": compute_movement_density(output),
    }


def summarize_scores(scores: Dict[str, object]) -> str:
    return (
        f"Clarity: {scores['clarity']}; "
        f"Faithfulness: {scores['faithfulness']}; "
        f"Behavior inference: {scores['behavior_inference']}; "
        f"Hallucination risk: {scores['hallucination_risk']}; "
        f"Sentence length: {scores['sentence_length']}; "
        f"Active rooms: {scores['active_rooms']}; "
        f"Temporal coverage: {scores['temporal_coverage']}; "
        f"Movement density: {scores['movement_density']}."
    )