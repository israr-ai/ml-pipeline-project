from types import SimpleNamespace

from src.analytics.aggregations import EMPTY_DASHBOARD_DATA, build_dashboard_data


def _prediction(gender, parental_education, lunch, test_prep, score):
    return SimpleNamespace(
        gender=gender,
        parental_education=parental_education,
        lunch=lunch,
        test_preparation_course=test_prep,
        predicted_math_score=score,
    )


def test_empty_predictions_returns_empty_dashboard():
    assert build_dashboard_data([]) == EMPTY_DASHBOARD_DATA


def test_dashboard_aggregates_are_computed_correctly():
    predictions = [
        _prediction("male", "bachelor's degree", "standard", "completed", 80),
        _prediction("male", "bachelor's degree", "standard", "none", 60),
        _prediction("female", "high school", "free/reduced", "completed", 90),
    ]

    data = build_dashboard_data(predictions)

    assert data["total_predictions"] == 3
    assert data["average_score"] == round((80 + 60 + 90) / 3, 2)
    assert data["highest_score"] == 90
    assert data["avg_by_gender"]["male"] == 70.0
    assert data["avg_by_gender"]["female"] == 90.0
    assert data["count_by_lunch"]["standard"] == 2
    assert data["count_by_lunch"]["free/reduced"] == 1
