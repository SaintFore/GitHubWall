import pytest
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
