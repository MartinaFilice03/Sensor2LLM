import json
from pathlib import Path
from typing import Any


def read_json(path: Path) -> Any:
    """
    Read a JSON file and return its content.
    """
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def write_json(data: Any, path: Path) -> None:
    """
    Write data to a JSON file.
    """
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def read_text(path: Path) -> str:
    """
    Read a text file.
    """
    return path.read_text(encoding="utf-8")


def write_text(content: str, path: Path) -> None:
    """
    Write text content to a file.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")