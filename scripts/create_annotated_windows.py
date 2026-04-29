import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

input_path = PROJECT_ROOT / "data" / "processed" / "milan_windows.json"
output_path = PROJECT_ROOT / "data" / "processed" / "annotated_milan_windows.json"

with input_path.open("r", encoding="utf-8") as f:
    data = json.load(f)

annotations = {
    "2009-10-16": {
        "summary_gold": "The day shows repeated indoor activity across multiple rooms, with the bedroom and kitchen among the most active areas.",
        "qa_pairs": [
            {
                "question": "What kind of behavior is observed during this day?",
                "answer": "The resident shows repeated movement across the bedroom, living room, kitchen, and other areas, suggesting normal indoor activity."
            },
            {
                "question": "Which rooms appear to be the most active?",
                "answer": "The bedroom and kitchen appear among the most active rooms."
            }
        ]
    }
}

for item in data:
    day = item["date"]

    if day in annotations:
        item.update(annotations[day])
    else:
        item["summary_gold"] = ""
        item["qa_pairs"] = []

with output_path.open("w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"Saved annotated dataset to {output_path}")