import sys
import json
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.preprocessing.data_to_text import (
    event_to_text,
    summarize_minute,
    summarize_hour,
)


def main() -> None:
    input_path = PROJECT_ROOT / "data" / "raw" / "milan.csv"
    output_path = PROJECT_ROOT / "data" / "processed" / "milan_windows.json"

    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    # -----------------------
    # Load data
    # -----------------------
    df = pd.read_csv(input_path, header=None)
    df.columns = ["date", "time", "location", "event"]

    # -----------------------
    # Timestamp parsing
    # -----------------------
    df["timestamp"] = pd.to_datetime(
        df["date"] + " " + df["time"],
        format="mixed",
        errors="coerce",
    )

    df = df.dropna(subset=["timestamp"]).copy()
    df = df.sort_values("timestamp").reset_index(drop=True)
    df = df.drop_duplicates(subset=["timestamp", "location", "event"]).copy()

    # FIX: ensure consistent date column
    df["date"] = df["timestamp"].dt.date.astype(str)

    # -----------------------
    # Event to text
    # -----------------------
    df["text"] = df.apply(
        lambda row: event_to_text(
            row["timestamp"],
            row["location"],
            row["event"],
        ),
        axis=1,
    )

    # -----------------------
    # Keep ON events (activity focus)
    # -----------------------
    df_on = df[df["event"] == "ON"].copy()

    # -----------------------
    # Minute aggregation
    # -----------------------
    df_on["minute"] = df_on["timestamp"].dt.strftime("%H:%M")

    minute_grouped = (
        df_on.groupby(["date", "minute"])["location"]
        .apply(list)
        .reset_index()
    )

    minute_grouped["minute_text"] = minute_grouped.apply(
        lambda row: summarize_minute(row["minute"], row["location"]),
        axis=1,
    )

    # -----------------------
    # Hour aggregation (FIXED)
    # -----------------------
    df_on["hour"] = df_on["timestamp"].dt.hour

    hour_grouped = (
        df_on.groupby(["date", "hour"])["location"]
        .apply(list)
        .reset_index()
    )

    hour_grouped["hour_text"] = hour_grouped.apply(
        lambda row: summarize_hour(str(row["hour"]), row["location"]),
        axis=1,
    )

    # -----------------------
    # Build final dataset
    # -----------------------
    dataset = []

    for day in sorted(df["date"].unique()):
        day_events = df[df["date"] == day]
        day_minutes = minute_grouped[minute_grouped["date"] == day]
        day_hours = hour_grouped[hour_grouped["date"] == day]

        item = {
            "date": day,
            "num_events": int(len(day_events)),

            # event-level representation
            "event_level_text": "\n".join(day_events["text"].tolist()),

            # minute-level representation
            "minute_level_text": "\n".join(day_minutes["minute_text"].tolist()),

            # hourly representation
            "hourly_text": "\n".join(day_hours["hour_text"].tolist()),
        }

        dataset.append(item)

    # -----------------------
    # Save output
    # -----------------------
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=2, ensure_ascii=False)

    print(f"Saved {len(dataset)} daily windows to {output_path}")


if __name__ == "__main__":
    main()