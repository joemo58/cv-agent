import json
import pytest
from pathlib import Path
from cv_agent.io import read_text_file, write_text_file, write_json_file, ensure_output_dir


def test_can_read_text_file(tmp_path):
    f = tmp_path / "test.md"
    f.write_text("hello", encoding="utf-8")
    assert read_text_file(f) == "hello"


def test_missing_file_raises_useful_error(tmp_path):
    with pytest.raises(FileNotFoundError, match="not found"):
        read_text_file(tmp_path / "missing.md")


def test_can_write_text_file(tmp_path):
    f = tmp_path / "out.md"
    write_text_file(f, "content")
    assert f.read_text(encoding="utf-8") == "content"


def test_can_create_output_directory(tmp_path):
    d = tmp_path / "nested" / "dir"
    ensure_output_dir(d)
    assert d.is_dir()


def test_can_write_json(tmp_path):
    f = tmp_path / "data.json"
    write_json_file(f, {"key": "value"})
    data = json.loads(f.read_text(encoding="utf-8"))
    assert data == {"key": "value"}
