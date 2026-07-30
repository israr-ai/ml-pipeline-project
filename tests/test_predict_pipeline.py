from src.pipeline.predict_pipeline import CustomData, PredictPipeline


def _sample_custom_data():
    return CustomData(
        gender="female",
        race_ethnicity="group B",
        parent_education="bachelor's degree",
        lunch="standard",
        test_preparation_course="completed",
        reading_score=72,
        writing_score=74,
    )


def test_get_data_as_data_frame_has_expected_shape():
    df = _sample_custom_data().get_data_as_data_frame()
    assert list(df.columns) == [
        "gender",
        "race_ethnicity",
        "parent_education",
        "lunch",
        "test_preparation_course",
        "reading_score",
        "writing_score",
    ]
    assert len(df) == 1
    assert df.iloc[0]["gender"] == "female"


def test_predict_pipeline_returns_a_score():
    df = _sample_custom_data().get_data_as_data_frame()
    result = PredictPipeline().predict(df)
    assert len(result) == 1
    assert 0 <= float(result[0]) <= 100
