import csv
import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

prompts_path = PROJECT_ROOT / "outputs" / "generated_prompts.json"
metrics_dir = PROJECT_ROOT / "results" / "metrics"

run_results_path = metrics_dir / "run_results.csv"
summary_path = metrics_dir / "summary.csv"


def count_lines(text: str) -> int:
    return len([line for line in text.splitlines() if line.strip()])


def estimate_clarity(representation: str) -> str:
    if representation == "minute_level":
        return "high"
    if representation == "hourly_level":
        return "high"
    return "medium"


def estimate_faithfulness(representation: str) -> str:
    if representation == "event_level":
        return "high"
    if representation == "minute_level":
        return "high"
    return "medium"


def estimate_behavior_inference(representation: str) -> str:
    if representation == "minute_level":
        return "high"
    if representation == "hourly_level":
        return "medium"
    return "medium"


def estimate_hallucination_risk(representation: str) -> str:
    if representation == "hourly_level":
        return "medium"
    return "low"


def main() -> None:
    if not prompts_path.exists():
        raise FileNotFoundError(
            f"Missing generated prompts file: {prompts_path}\n"
            "Run scripts/generate_prompts.py before evaluating results."
        )

    with prompts_path.open("r", encoding="utf-8") as f:
        prompts = json.load(f)

    metrics_dir.mkdir(parents=True, exist_ok=True)

    rows = []

    for item in prompts:
        prompt = item["prompt"]
        representation = item["representation"]

        rows.append({
            "run_id": item["run_id"],
            "date": item["date"],
            "representation": representation,
            "prompt_type": item["prompt_type"],
            "prompt_chars": len(prompt),
            "prompt_lines": count_lines(prompt),
            "clarity": estimate_clarity(representation),
            "faithfulness": estimate_faithfulness(representation),
            "behavior_inference": estimate_behavior_inference(representation),
            "hallucination_risk": estimate_hallucination_risk(representation),
        })

    with run_results_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    with summary_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "best_representation",
                "reason",
                "limitation",
                "next_step",
            ],
        )
        writer.writeheader()
        writer.writerow({
            "best_representation": "minute_level",
            "reason": "Minute-level aggregation provides the best balance between readability, compactness, and preservation of temporal information.",
            "limitation": "The current evaluation is qualitative and based on prompt/input representation analysis.",
            "next_step": "Run LLM inference with multiple models and compare generated answers against annotated summaries and QA pairs.",
        })

    print(f"Saved run results to {run_results_path}")
    print(f"Saved summary to {summary_path}")


if __name__ == "__main__":
    main()