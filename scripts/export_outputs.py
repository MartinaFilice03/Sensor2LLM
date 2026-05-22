import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

input_path = PROJECT_ROOT / "data" / "processed" / "milan_windows.json"
output_dir = PROJECT_ROOT / "outputs"


def save_text(path: Path, text: str, limit: int = 5000):
    path.write_text(text[:limit], encoding="utf-8")


def main() -> None:
    if not input_path.exists():
        raise FileNotFoundError(f"Missing input: {input_path}")

    with input_path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    if not data:
        raise ValueError("Empty dataset")

    output_dir.mkdir(parents=True, exist_ok=True)

    # take first 3 samples instead of 1
    samples = data[:3]

    for i, sample in enumerate(samples):
        prefix = f"sample_{i}"

        save_text(
            output_dir / f"{prefix}_event_level.txt",
            sample.get("event_level_text", ""),
        )

        save_text(
            output_dir / f"{prefix}_minute_level.txt",
            sample.get("minute_level_text", ""),
        )

        save_text(
            output_dir / f"{prefix}_hourly_level.txt",
            sample.get("hourly_text", ""),
        )

    print(f"Saved {len(samples)} samples to {output_dir}")


if __name__ == "__main__":
    main()