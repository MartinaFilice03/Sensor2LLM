import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

prompts_path = PROJECT_ROOT / "outputs" / "generated_prompts.json"
predictions_path = PROJECT_ROOT / "results" / "predictions" / "llm_outputs.json"


def mock_generate(prompt: str) -> str:
    return (
        "The resident mainly moved between the bedroom, "
        "living room, bathroom, and kitchen during the observed period."
    )


def main() -> None:
    with prompts_path.open("r", encoding="utf-8") as f:
        prompts = json.load(f)

    predictions = []

    for item in prompts:
        output = mock_generate(item["prompt"])

        predictions.append({
            "run_id": item["run_id"],
            "prompt_type": item["prompt_type"],
            "representation": item["representation"],
            "output": output,
        })

    predictions_path.parent.mkdir(parents=True, exist_ok=True)

    with predictions_path.open("w", encoding="utf-8") as f:
        json.dump(predictions, f, indent=2, ensure_ascii=False)

    print(f"Saved {len(predictions)} predictions to {predictions_path}")


if __name__ == "__main__":
    main()