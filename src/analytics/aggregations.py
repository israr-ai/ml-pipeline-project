import pandas as pd

PREDICTION_FIELDS = [
    "gender",
    "parental_education",
    "lunch",
    "test_preparation_course",
    "predicted_math_score",
]

EMPTY_DASHBOARD_DATA = {
    "total_predictions": 0,
    "average_score": 0,
    "highest_score": 0,
    "avg_by_gender": {},
    "avg_by_parental_education": {},
    "count_by_lunch": {},
    "avg_by_test_prep": {},
}


def predictions_to_dataframe(predictions):
    return pd.DataFrame(
        [{field: getattr(prediction, field) for field in PREDICTION_FIELDS} for prediction in predictions]
    )


def _avg_by(df, column):
    return {
        str(key): round(float(value), 2)
        for key, value in df.groupby(column)["predicted_math_score"].mean().items()
    }


def _count_by(df, column):
    return {
        str(key): int(value)
        for key, value in df.groupby(column)["predicted_math_score"].count().items()
    }


def build_dashboard_data(predictions):
    df = predictions_to_dataframe(predictions)

    if df.empty:
        return dict(EMPTY_DASHBOARD_DATA)

    return {
        "total_predictions": int(len(df)),
        "average_score": round(float(df["predicted_math_score"].mean()), 2),
        "highest_score": round(float(df["predicted_math_score"].max()), 2),
        "avg_by_gender": _avg_by(df, "gender"),
        "avg_by_parental_education": _avg_by(df, "parental_education"),
        "count_by_lunch": _count_by(df, "lunch"),
        "avg_by_test_prep": _avg_by(df, "test_preparation_course"),
    }
