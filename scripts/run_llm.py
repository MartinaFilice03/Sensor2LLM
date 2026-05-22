import json
from pathlib import Path
import random

PROJECT_ROOT = Path(__file__).resolve().parents[1]

prompts_path = PROJECT_ROOT / "outputs" / "generated_prompts.json"
predictions_path = PROJECT_ROOT / "results" / "predictions" / "llm_outputs.json"


def mock_generate(prompt: str, prompt_type: str) -> str:
    variations = [
        "The resident mainly moved between the bedroom, living room, bathroom, and kitchen.",
        "The activity shows frequent transitions across indoor spaces with repeated kitchen usage.",
        "The resident spent most of the time alternating between resting and kitchen-related activity.",
        "Movement is concentrated in bedroom and living areas with occasional kitchen visits.",
    ]

    # slight conditioning on prompt type
    if prompt_type == "hourly":
        return random.choice(variations) + " This is observed on an hourly basis."

    if prompt_type == "event":
        return random.choice(variations) + " This is based on individual sensor events."

    return random.choice(variations)


def main() -> None:
    if not prompts_path.exists():
        raise FileNotFoundError(f"Missing prompts: {prompts_path}")

    with prompts_path.open("r", encoding="utf-8") as f:
        prompts = json.load(f)

    predictions = []

    for item in prompts:
        output = mock_generate(
            item["prompt"],
            item.get("prompt_type", "")
        )

        predictions.append({
            "run_id": item.get("run_id"),
            "prompt_type": item.get("prompt_type"),
            "representation": item.get("representation"),
            "output": output,
        })

    predictions_path.parent.mkdir(parents=True, exist_ok=True)

    with predictions_path.open("w", encoding="utf-8") as f:
        json.dump(predictions, f, indent=2, ensure_ascii=False)

    print(f"Saved {len(predictions)} predictions to {predictions_path}")


if __name__ == "__main__":
    main()