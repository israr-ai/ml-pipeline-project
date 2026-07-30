"""End-to-end style test: drives a full user journey through the app via the
Flask test client (signup -> predict -> history -> dashboard -> logout)."""

from src.models_db import Prediction, User

PREDICT_FORM_DATA = {
    "gender": "female",
    "race_ethnicity": "group B",
    "parent_education": "bachelor's degree",
    "lunch": "standard",
    "test_preparation_course": "completed",
    "reading_score": "72",
    "writing_score": "74",
}


def test_full_user_journey(client, app):
    signup_resp = client.post(
        "/signup",
        data={"name": "Journey User", "email": "journey@example.com", "password": "password123"},
        follow_redirects=True,
    )
    assert signup_resp.status_code == 200

    predict_resp = client.post("/predictdata", data=PREDICT_FORM_DATA, follow_redirects=True)
    assert predict_resp.status_code == 200

    history_resp = client.get("/history")
    assert history_resp.status_code == 200

    dashboard_resp = client.get("/dashboard")
    assert dashboard_resp.status_code == 200

    with app.app_context():
        user = User.query.filter_by(email="journey@example.com").first()
        assert user is not None
        assert Prediction.query.filter_by(user_id=user.id).count() == 1

    client.get("/logout")
    after_logout = client.get("/dashboard", follow_redirects=False)
    assert after_logout.status_code == 302
