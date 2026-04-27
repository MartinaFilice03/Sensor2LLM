from typing import List
import pandas as pd


def add_time_window_column(df: pd.DataFrame, window_minutes: int = 60) -> pd.DataFrame:
    """
    Add a time window column to a dataframe of sensor events based on the timestamp.
    """
    df = df.copy()
    df["window_start"] = df["timestamp"].dt.floor(f"{window_minutes}min")
    return df


def group_locations_by_window(df: pd.DataFrame, window_minutes: int = 60) -> pd.DataFrame:
    """
    Group ON events by fixed-size time windows and collect the involved locations.
    """
    df = df.copy()
    df = df[df["event"] == "ON"].copy()
    df["window_start"] = df["timestamp"].dt.floor(f"{window_minutes}min")

    grouped = (
        df.groupby(["date", "window_start"])["location"]
        .apply(list)
        .reset_index()
    )
    return grouped