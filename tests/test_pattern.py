import pytest
import tempfile
import json
import os
from src.core.pattern import Pattern


def test_pattern_creation():
    """Test pattern object creation"""
    data = [[0, 1, 2], [3, 4, 0]] * 3 + [[0, 1, 2]]  # 7 rows
    pattern = Pattern(name="test", data=data)
    assert pattern.name == "test"
    assert pattern.width == 3
    assert pattern.height == 7
    assert pattern.data == data


def test_pattern_validation_valid():
    """Test valid pattern validation"""
    data = [[0, 1, 2, 3, 4]] * 7
    pattern = Pattern(name="test", data=data)
    assert pattern.validate() is True


def test_pattern_validation_invalid_value():
    """Test invalid value validation"""
    data = [[0, 1, 5]] * 7  # 5 is out of range
    with pytest.raises(ValueError, match="Invalid level"):
        Pattern(name="test", data=data)


def test_pattern_validation_invalid_height():
    """Test height is not 7"""
    data = [[0, 1]] * 5  # height is 5
    with pytest.raises(ValueError, match="Height must be 7"):
        Pattern(name="test", data=data)


def test_pattern_width_property():
    """Test width property returns correct column count"""
    data = [[0, 1, 2, 3, 4, 0, 1, 2, 3, 4, 0]] * 7
    pattern = Pattern(name="wide", data=data)
    assert pattern.width == 11


def test_pattern_validate_inconsistent_row_width():
    """Test validation catches rows with different widths"""
    data = [[0, 1, 2], [0, 1]] * 3 + [[0, 1, 2]]
    with pytest.raises(ValueError, match="inconsistent width"):
        Pattern(name="test", data=data)


def test_load_pattern_from_json():
    """Test loading a pattern from a JSON file"""
    from src.core.pattern import load_pattern

    pattern_data = {
        "name": "heart",
        "width": 7,
        "height": 7,
        "data": [[0, 0, 1, 1, 0, 0, 0]] * 7,
    }

    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump(pattern_data, f)
        temp_path = f.name

    try:
        pattern = load_pattern(temp_path)
        assert pattern.name == "heart"
        assert pattern.width == 7
        assert pattern.height == 7
    finally:
        os.unlink(temp_path)


def test_load_pattern_file_not_found():
    """Test loading a nonexistent file raises FileNotFoundError"""
    from src.core.pattern import load_pattern

    with pytest.raises(FileNotFoundError):
        load_pattern("/nonexistent/path.json")


def test_load_pattern_invalid_json():
    """Test loading invalid JSON raises JSONDecodeError"""
    from src.core.pattern import load_pattern

    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        f.write("invalid json content")
        temp_path = f.name

    try:
        with pytest.raises(json.JSONDecodeError):
            load_pattern(temp_path)
    finally:
        os.unlink(temp_path)
