import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

input_path = PROJECT_ROOT / "data" / "processed" / "annotated_milan_windows.json"
prompts_dir = PROJECT_ROOT / "prompts"
output_path = PROJECT_ROOT / "outputs" / "generated_prompts.json"

MAX_CHARS = 5000


def load_prompt(filename: str) -> str:
    return (prompts_dir / filename).read_text(encoding="utf-8")


def truncate_text(text: str, max_chars: int) -> str:
    """
    Truncate text without cutting a line in the middle.
    """
    if len(text) <= max_chars:
        return text

    truncated = text[:max_chars]
    last_newline = truncated.rfind("\n")

    if last_newline != -1:
        return truncated[:last_newline]

    return truncated


def main() -> None:
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    with input_path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    sample = data[0]

    summary_template = load_prompt("summary_prompt.txt")
    analysis_template = load_prompt("analysis_prompt.txt")
    aggregated_template = load_prompt("aggregated_prompt.txt")
    hourly_template = load_prompt("hourly_prompt.txt")

    event_level_text = truncate_text(sample["event_level_text"], MAX_CHARS)
    minute_level_text = truncate_text(sample["minute_level_text"], MAX_CHARS)
    hourly_text = truncate_text(sample["hourly_text"], MAX_CHARS)

    generated_prompts = [
        {
            "run_id": "run_001",
            "date": sample["date"],
            "representation": "event_level",
            "prompt_type": "summary",
            "prompt": summary_template.replace("{events}", event_level_text),
        },
        {
            "run_id": "run_002",
            "date": sample["date"],
            "representation": "event_level",
            "prompt_type": "analysis",
            "prompt": analysis_template.replace("{events}", event_level_text),
        },
        {
            "run_id": "run_003",
            "date": sample["date"],
            "representation": "minute_level",
            "prompt_type": "aggregated",
            "prompt": aggregated_template.replace("{events}", minute_level_text),
        },
        {
            "run_id": "run_004",
            "date": sample["date"],
            "representation": "hourly_level",
            "prompt_type": "hourly",
            "prompt": hourly_template.replace("{events}", hourly_text),
        },
    ]

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8") as f:
        json.dump(generated_prompts, f, indent=2, ensure_ascii=False)

    print(f"Saved {len(generated_prompts)} generated prompts to {output_path}")


if __name__ == "__main__":
    main()