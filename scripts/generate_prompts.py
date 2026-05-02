import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.common.io import read_json
from src.llm.runner import generate_prompts, save_generated_prompts

input_path = PROJECT_ROOT / "data" / "processed" / "annotated_milan_windows.json"
prompts_dir = PROJECT_ROOT / "prompts"
output_path = PROJECT_ROOT / "outputs" / "generated_prompts.json"

MAX_CHARS = 5000


def main() -> None:
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    data = read_json(input_path)
    sample = data[0]

    generated_prompts = generate_prompts(
        sample=sample,
        prompts_dir=prompts_dir,
        max_chars=MAX_CHARS,
    )

    save_generated_prompts(generated_prompts, output_path)

    print(f"Saved {len(generated_prompts)} generated prompts to {output_path}")


if __name__ == "__main__":
    main()