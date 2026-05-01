import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

input_path = PROJECT_ROOT / "data" / "processed" / "milan_windows.json"
output_dir = PROJECT_ROOT / "outputs"


def main() -> None:
    with input_path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    sample = data[0]

    output_dir.mkdir(parents=True, exist_ok=True)

    (output_dir / "milan_event_level_example.txt").write_text(
        sample["event_level_text"][:5000],
        encoding="utf-8",
    )

    (output_dir / "milan_minute_level_example.txt").write_text(
        sample["minute_level_text"][:5000],
        encoding="utf-8",
    )

    (output_dir / "milan_hourly_level_example.txt").write_text(
        sample["hourly_text"][:5000],
        encoding="utf-8",
    )

    print(f"Saved output examples to {output_dir}")


if __name__ == "__main__":
    main()