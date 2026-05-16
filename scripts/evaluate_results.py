import csv
import json
from pathlib import Path

from src.eval.metrics import score_output

PROJECT_ROOT = Path(__file__).resolve().parents[1]

prompts_path = PROJECT_ROOT / "outputs" / "generated_prompts.json"

metrics_dir = PROJECT_ROOT / "results" / "metrics"

summary_path = metrics_dir / "summary.csv"


def save_representation_csv(rows, representation_name):
    output_path = metrics_dir / f"{representation_name}.csv"

    with output_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    print(f"Saved {representation_name} results to {output_path}")


def main() -> None:
    if not prompts_path.exists():
        raise FileNotFoundError(
            f"Missing prompts file: {prompts_path}"
        )

    with prompts_path.open("r", encoding="utf-8") as f:
        prompts = json.load(f)

    metrics_dir.mkdir(parents=True, exist_ok=True)

    grouped_rows = {
        "event_level": [],
        "minute_level": [],
        "hourly_level": [],
    }

    representation_scores = {
        "event_level": [],
        "minute_level": [],
        "hourly_level": [],
    }

    for item in prompts:
        representation = item["representation"]

        scores = score_output(item["prompt"])

        row = {
            "run_id": item["run_id"],
            "date": item["date"],
            "representation": representation,
            "prompt_type": item["prompt_type"],
            "clarity": scores["clarity"],
            "faithfulness": scores["faithfulness"],
            "behavior_inference": scores["behavior_inference"],
            "hallucination_risk": scores["hallucination_risk"],
            "sentence_length": scores["sentence_length"],
            "active_rooms": scores["active_rooms"],
            "temporal_coverage": scores["temporal_coverage"],
            "movement_density": scores["movement_density"],
        }

        grouped_rows[representation].append(row)

        score_value = 0

        if scores["faithfulness"] == "high":
            score_value += 1

        if scores["behavior_inference"] == "high":
            score_value += 1

        if scores["temporal_coverage"] == "high":
            score_value += 1

        representation_scores[representation].append(score_value)

    for representation, rows in grouped_rows.items():
        if rows:
            save_representation_csv(rows, representation)

    with summary_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "representation",
                "avg_score",
            ],
        )

        writer.writeheader()

        for representation, scores in representation_scores.items():
            avg_score = round(sum(scores) / len(scores), 2)

            writer.writerow({
                "representation": representation,
                "avg_score": avg_score,
            })

    print(f"Saved summary to {summary_path}")


if __name__ == "__main__":
    main()