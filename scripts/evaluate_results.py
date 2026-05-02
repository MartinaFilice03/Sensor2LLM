import csv
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.common.io import read_json
from src.eval.metrics import score_output, summarize_scores


predictions_path = PROJECT_ROOT / "results" / "predictions" / "llm_outputs.json"
metrics_dir = PROJECT_ROOT / "results" / "metrics"

run_results_path = metrics_dir / "run_results.csv"
summary_path = metrics_dir / "summary.csv"


def main() -> None:
    if not predictions_path.exists():
        raise FileNotFoundError(
            f"Missing predictions file: {predictions_path}\n"
            "Create results/predictions/llm_outputs.json before running this script."
        )

    outputs = read_json(predictions_path)

    metrics_dir.mkdir(parents=True, exist_ok=True)

    rows = []

    for item in outputs:
        scores = score_output(item["output"])

        rows.append({
            "run_id": item["run_id"],
            "date": item["date"],
            "representation": item["representation"],
            "prompt_type": item["prompt_type"],
            "model": item.get("model", "unknown"),
            "clarity": scores["clarity"],
            "faithfulness": scores["faithfulness"],
            "behavior_inference": scores["behavior_inference"],
            "hallucination_risk": scores["hallucination_risk"],
            "summary": summarize_scores(scores),
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
            "reason": "Minute-level aggregation provides a compact representation while preserving useful temporal information.",
            "limitation": "The evaluation is qualitative and based on a limited sample.",
            "next_step": "Evaluate more days and compare outputs from multiple LLMs.",
        })

    print(f"Saved run results to {run_results_path}")
    print(f"Saved summary to {summary_path}")


if __name__ == "__main__":
    main()