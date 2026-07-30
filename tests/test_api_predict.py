VALID_PAYLOAD = {
    "gender": "female",
    "race_ethnicity": "group B",
    "parent_education": "bachelor's degree",
    "lunch": "standard",
    "test_preparation_course": "completed",
    "reading_score": 72,
    "writing_score": 74,
}


def test_api_predict_rejects_non_json_body(client):
    response = client.post("/api/predict", data="not json")
    assert response.status_code == 400


def test_api_predict_rejects_invalid_payload(client):
    response = client.post("/api/predict", json={"gender": "invalid"})
    assert response.status_code == 400
    assert "details" in response.get_json()


def test_api_predict_returns_score_for_valid_payload(client):
    response = client.post("/api/predict", json=VALID_PAYLOAD)
    assert response.status_code == 200
    body = response.get_json()
    assert "predicted_math_score" in body
    assert isinstance(body["predicted_math_score"], float)
