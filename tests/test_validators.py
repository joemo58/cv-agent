import pytest
from cv_agent.validators import validate_inputs

VALID_CV = "x" * 300
VALID_JD = "x" * 300


def test_empty_base_cv_fails():
    with pytest.raises(ValueError, match="empty"):
        validate_inputs("", VALID_JD, 2, "direct", "engineer")


def test_empty_jd_fails():
    with pytest.raises(ValueError, match="empty"):
        validate_inputs(VALID_CV, "", 2, "direct", "engineer")


def test_short_base_cv_fails():
    with pytest.raises(ValueError, match="300"):
        validate_inputs("x" * 299, VALID_JD, 2, "direct", "engineer")


def test_short_jd_fails():
    with pytest.raises(ValueError, match="300"):
        validate_inputs(VALID_CV, "x" * 299, 2, "direct", "engineer")


def test_invalid_max_pages_too_low_fails():
    with pytest.raises(ValueError, match="max_pages"):
        validate_inputs(VALID_CV, VALID_JD, 0, "direct", "engineer")


def test_invalid_max_pages_too_high_fails():
    with pytest.raises(ValueError, match="max_pages"):
        validate_inputs(VALID_CV, VALID_JD, 5, "direct", "engineer")


def test_overly_long_tone_fails():
    with pytest.raises(ValueError, match="tone"):
        validate_inputs(VALID_CV, VALID_JD, 2, "x" * 201, "engineer")


def test_overly_long_target_role_fails():
    with pytest.raises(ValueError, match="target_role"):
        validate_inputs(VALID_CV, VALID_JD, 2, "direct", "x" * 201)


def test_valid_inputs_pass():
    validate_inputs(VALID_CV, VALID_JD, 2, "direct", "engineer")
