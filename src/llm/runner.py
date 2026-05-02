import json
from pathlib import Path
from typing import Dict, List

from src.llm.prompt import build_prompt, load_prompt_template, truncate_text


def generate_prompts(
    sample: Dict,
    prompts_dir: Path,
    max_chars: int = 5000,
) -> List[Dict]:
    """
    Generate prompts for different textual representations of the same sensor window.
    """
    summary_template = load_prompt_template(prompts_dir / "summary_prompt.txt")
    analysis_template = load_prompt_template(prompts_dir / "analysis_prompt.txt")
    aggregated_template = load_prompt_template(prompts_dir / "aggregated_prompt.txt")
    hourly_template = load_prompt_template(prompts_dir / "hourly_prompt.txt")

    event_level_text = truncate_text(sample["event_level_text"], max_chars)
    minute_level_text = truncate_text(sample["minute_level_text"], max_chars)
    hourly_text = truncate_text(sample["hourly_text"], max_chars)

    return [
        {
            "run_id": "run_001",
            "date": sample["date"],
            "representation": "event_level",
            "prompt_type": "summary",
            "prompt": build_prompt(summary_template, event_level_text),
        },
        {
            "run_id": "run_002",
            "date": sample["date"],
            "representation": "event_level",
            "prompt_type": "analysis",
            "prompt": build_prompt(analysis_template, event_level_text),
        },
        {
            "run_id": "run_003",
            "date": sample["date"],
            "representation": "minute_level",
            "prompt_type": "aggregated",
            "prompt": build_prompt(aggregated_template, minute_level_text),
        },
        {
            "run_id": "run_004",
            "date": sample["date"],
            "representation": "hourly_level",
            "prompt_type": "hourly",
            "prompt": build_prompt(hourly_template, hourly_text),
        },
    ]


def save_generated_prompts(generated_prompts: List[Dict], output_path: Path) -> None:
    """
    Save generated prompts to a JSON file.
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8") as f:
        json.dump(generated_prompts, f, indent=2, ensure_ascii=False)