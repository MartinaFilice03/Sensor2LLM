import csv
import json
from pathlib import Path

from src.eval.metrics import score_output

PROJECT_ROOT = Path(__file__).resolve().parents[1]

prompts_path = PROJECT_ROOT / "results" / "predictions" / "llm_outputs.json"
metrics_dir = PROJECT_ROOT / "results" / "metrics"
summary_path = metrics_dir / "summary.csv"


def save_representation_csv(rows, representation_name):
    output_path = metrics_dir / f"{representation_name}.csv"

    if not rows:
        print(f"[WARN] No rows for {representation_name}, skipping CSV export.")
        return

    with output_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    print(f"Saved {representation_name} results to {output_path}")


def main() -> None:
    if not prompts_path.exists():
        raise FileNotFoundError(f"Missing prompts file: {prompts_path}")

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
        representation = item.get("representation")

        if representation not in grouped_rows:
            continue

        # IMPORTANT: assumes score_output returns dict of metrics
        scores = score_output(item["output"])

        row = {
            "run_id": item.get("run_id"),
            "date": item.get("date"),
            "representation": representation,
            "prompt_type": item.get("prompt_type"),

            "clarity": scores.get("clarity"),
            "faithfulness": scores.get("faithfulness"),
            "behavior_inference": scores.get("behavior_inference"),
            "hallucination_risk": scores.get("hallucination_risk"),
            "sentence_length": scores.get("sentence_length"),
            "active_rooms": scores.get("active_rooms"),
            "temporal_coverage": scores.get("temporal_coverage"),
            "movement_density": scores.get("movement_density"),
        }

        grouped_rows[representation].append(row)

        # safer scoring
        score_value = 0
        score_value += 1 if scores.get("faithfulness") == "high" else 0
        score_value += 1 if scores.get("behavior_inference") == "high" else 0
        score_value += 1 if scores.get("temporal_coverage") == "high" else 0

        representation_scores[representation].append(score_value)

    # save CSVs
    for representation, rows in grouped_rows.items():
        save_representation_csv(rows, representation)

    # summary
    with summary_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["representation", "avg_score"])
        writer.writeheader()

        for representation, scores in representation_scores.items():
            avg_score = (
                round(sum(scores) / len(scores), 2)
                if scores else 0.0
            )

            writer.writerow({
                "representation": representation,
                "avg_score": avg_score,
            })

    print(f"Saved summary to {summary_path}")


if __name__ == "__main__":
    main()