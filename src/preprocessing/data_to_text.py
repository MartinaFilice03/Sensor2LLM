from typing import List


def normalize_location(location: str) -> str:
    mapping = {
        "LivingRoom": "living room",
        "DiningRoom": "dining room",
        "OutsideDoor": "outside door",
        "LoungeChair": "lounge chair",
        "WorkArea": "work area",
        "Bedroom": "bedroom",
        "Bathroom": "bathroom",
        "Kitchen": "kitchen",
    }
    return mapping.get(location, location.lower())


def event_to_text(timestamp, location: str, event: str) -> str:
    time_str = timestamp.strftime("%H:%M")
    loc = normalize_location(location)

    if event == "ON":
        return f"At {time_str}, movement detected in the {loc}."
    elif event == "OFF":
        return f"At {time_str}, no more movement in the {loc}."
    elif event == "OPEN":
        return f"At {time_str}, the {loc} was opened."
    elif event == "CLOSE":
        return f"At {time_str}, the {loc} was closed."
    else:
        return f"At {time_str}, an unknown event occurred in the {loc}."


def summarize_minute(minute: str, locations: List[str]) -> str:
    unique_locations = sorted(set(normalize_location(loc) for loc in locations))

    if len(unique_locations) == 1:
        return f"At {minute}, activity occurred in the {unique_locations[0]}."
    return f"At {minute}, activity occurred in multiple areas: {', '.join(unique_locations)}."


def summarize_hour(hour: str, locations: List[str]) -> str:
    unique_locations = sorted(set(normalize_location(loc) for loc in locations))

    if len(unique_locations) == 1:
        return f"During the hour starting at {hour}, activity was detected only in the {unique_locations[0]}."
    return f"During the hour starting at {hour}, activity was detected in these areas: {', '.join(unique_locations)}."