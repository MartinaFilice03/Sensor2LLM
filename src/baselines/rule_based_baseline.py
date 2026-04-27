from typing import Dict
import pandas as pd


def compute_simple_baseline(df: pd.DataFrame) -> Dict:
    """
    Compute a simple rule-based baseline summary from ON events.
    """
    df_on = df[df["event"] == "ON"].copy()

    if df_on.empty:
        return {
            "most_used_room": None,
            "active_room_count": 0,
            "outside_door_detected": False,
            "night_activity": False,
        }

    room_counts = df_on["location"].value_counts()
    most_used_room = room_counts.idxmax()
    active_room_count = int(df_on["location"].nunique())
    outside_door_detected = bool((df_on["location"] == "OutsideDoor").any())
    night_activity = bool((df_on["timestamp"].dt.hour < 6).any())

    return {
        "most_used_room": most_used_room,
        "active_room_count": active_room_count,
        "outside_door_detected": outside_door_detected,
        "night_activity": night_activity,
    }