import json
from pathlib import Path


def read_text_file(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {path}")


def write_text_file(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8")


def write_json_file(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def ensure_output_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)
