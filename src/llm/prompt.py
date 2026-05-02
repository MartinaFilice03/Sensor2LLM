from pathlib import Path


def load_prompt_template(prompt_path: Path) -> str:
    """
    Load a prompt template from a text file.
    """
    return prompt_path.read_text(encoding="utf-8")


def build_prompt(template: str, events: str) -> str:
    """
    Fill a prompt template with a textual sensor representation.
    """
    return template.replace("{events}", events)


def truncate_text(text: str, max_chars: int = 5000) -> str:
    """
    Truncate text without cutting the last line in the middle.
    """
    if len(text) <= max_chars:
        return text

    truncated = text[:max_chars]
    last_newline = truncated.rfind("\n")

    if last_newline != -1:
        return truncated[:last_newline]

    return truncated