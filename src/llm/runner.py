import json
from pathlib import Path
from typing import Dict, List

from src.llm.prompt import (
    build_prompt,
    load_prompt_template,
    truncate_text,
)


def generate_prompts(
    sample: Dict,
    prompts_dir: Path,
    max_chars: int = 5000,
) -> List[Dict]:
    """
    Generate prompts for multiple sensor-text representations.
    """

    templates = {
        "summary": load_prompt_template(
            prompts_dir / "summary_prompt.txt"
        ),
        "analysis": load_prompt_template(
            prompts_dir / "analysis_prompt.txt"
        ),
        "aggregated": load_prompt_template(
            prompts_dir / "aggregated_prompt.txt"
        ),
        "hourly": load_prompt_template(
            prompts_dir / "hourly_prompt.txt"
        ),
    }

    representations = {
        "event_level": truncate_text(
            sample["event_level_text"],
            max_chars
        ),
        "minute_level": truncate_text(
            sample["minute_level_text"],
            max_chars
        ),
        "hourly_level": truncate_text(
            sample["hourly_text"],
            max_chars
        ),
    }

    experiments = [
        {
            "run_id": "run_001",
            "representation": "event_level",
            "prompt_type": "summary",
        },
        {
            "run_id": "run_002",
            "representation": "event_level",
            "prompt_type": "analysis",
        },
        {
            "run_id": "run_003",
            "representation": "minute_level",
            "prompt_type": "aggregated",
        },
        {
            "run_id": "run_004",
            "representation": "hourly_level",
            "prompt_type": "hourly",
        },
    ]

    generated_prompts = []

    for exp in experiments:
        text = representations[exp["representation"]]
        template = templates[exp["prompt_type"]]

        generated_prompts.append(
            {
                "run_id": exp["run_id"],
                "date": sample["date"],
                "representation": exp["representation"],
                "prompt_type": exp["prompt_type"],
                "prompt": build_prompt(template, text),
            }
        )

    return generated_prompts


def save_generated_prompts(
    generated_prompts: List[Dict],
    output_path: Path,
) -> None:
    """
    Save generated prompts to JSON.
    """
    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with output_path.open(
        "w",
        encoding="utf-8",
    ) as f:
        json.dump(
            generated_prompts,
            f,
            indent=2,
            ensure_ascii=False,
        )