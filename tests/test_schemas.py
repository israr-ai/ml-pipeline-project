import pytest
from pydantic import ValidationError

from src.schemas import PredictRequest

VALID_PAYLOAD = {
    "gender": "female",
    "race_ethnicity": "group B",
    "parent_education": "bachelor's degree",
    "lunch": "standard",
    "test_preparation_course": "completed",
    "reading_score": 72,
    "writing_score": 74,
}


def test_valid_payload_parses():
    req = PredictRequest(**VALID_PAYLOAD)
    assert req.gender.value == "female"
    assert req.reading_score == 72


def test_invalid_enum_value_rejected():
    payload = {**VALID_PAYLOAD, "gender": "unknown"}
    with pytest.raises(ValidationError):
        PredictRequest(**payload)


@pytest.mark.parametrize("score", [-1, 101])
def test_score_out_of_range_rejected(score):
    payload = {**VALID_PAYLOAD, "reading_score": score}
    with pytest.raises(ValidationError):
        PredictRequest(**payload)


def test_missing_field_rejected():
    payload = dict(VALID_PAYLOAD)
    del payload["lunch"]
    with pytest.raises(ValidationError):
        PredictRequest(**payload)
