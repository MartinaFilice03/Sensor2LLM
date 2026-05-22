import pandas as pd


def to_event_text(df: pd.DataFrame) -> str:
    """
    Convert raw sensor events into event-level text.
    """
    lines = []

    for _, row in df.iterrows():
        lines.append(
            f"{row['timestamp']} - "
            f"{row['location']} sensor turned "
            f"{row['event']}"
        )

    return "\n".join(lines)


def to_minute_text(df: pd.DataFrame) -> str:
    """
    Aggregate sensor activations per minute.
    """
    grouped = (
        df.groupby(
            df["timestamp"].dt.floor("min")
        )["location"]
        .apply(list)
        .reset_index()
    )

    lines = []

    for _, row in grouped.iterrows():
        locations = ", ".join(row["location"])

        lines.append(
            f"{row['timestamp']}: "
            f"activity detected in {locations}"
        )

    return "\n".join(lines)


def to_hourly_text(df: pd.DataFrame) -> str:
    """
    Aggregate sensor activity per hour.
    """
    grouped = (
        df.groupby(
            df["timestamp"].dt.hour
        )["location"]
        .value_counts()
        .reset_index(name="count")
    )

    lines = []

    for _, row in grouped.iterrows():
        lines.append(
            f"Hour {row['timestamp']}: "
            f"{row['location']} active "
            f"{row['count']} times"
        )

    return "\n".join(lines)


def build_representation(
    df: pd.DataFrame,
    level: str,
) -> str:
    """
    Build textual representation
    from raw sensor events.
    """
    if level == "event_level":
        return to_event_text(df)

    if level == "minute_level":
        return to_minute_text(df)

    if level == "hourly_level":
        return to_hourly_text(df)

    raise ValueError(
        f"Unknown representation: {level}"
    )