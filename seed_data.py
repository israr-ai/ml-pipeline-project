import random
from datetime import datetime, timedelta, timezone

from application import application
from src.models_db import Prediction, User, db

GENDERS = ["male", "female"]
RACE_GROUPS = ["group A", "group B", "group C", "group D", "group E"]
PARENTAL_EDUCATION = [
    "associate's degree",
    "bachelor's degree",
    "high school",
    "master's degree",
    "some college",
    "some high school",
]
LUNCH_TYPES = ["standard", "free/reduced"]
TEST_PREP = ["none", "completed"]

PREDICTIONS_PER_USER = 12


def random_prediction(user_id, days_ago):
    reading_score = random.randint(40, 100)
    writing_score = random.randint(40, 100)
    test_prep = random.choice(TEST_PREP)
    base_score = (reading_score + writing_score) / 2
    prep_bonus = 5 if test_prep == "completed" else 0
    predicted_math_score = max(0, min(100, base_score + prep_bonus + random.uniform(-8, 8)))

    return Prediction(
        user_id=user_id,
        gender=random.choice(GENDERS),
        race_ethnicity=random.choice(RACE_GROUPS),
        parental_education=random.choice(PARENTAL_EDUCATION),
        lunch=random.choice(LUNCH_TYPES),
        test_preparation_course=test_prep,
        reading_score=reading_score,
        writing_score=writing_score,
        predicted_math_score=round(predicted_math_score, 2),
        created_at=datetime.now(timezone.utc) - timedelta(days=days_ago, hours=random.randint(0, 23)),
    )


if __name__ == "__main__":
    with application.app_context():
        users = User.query.all()
        if not users:
            print("No users found - create a user (signup) before seeding predictions.")
        else:
            for user in users:
                for i in range(PREDICTIONS_PER_USER):
                    days_ago = int(i * 30 / PREDICTIONS_PER_USER)
                    db.session.add(random_prediction(user.id, days_ago))
                print(f"Seeded {PREDICTIONS_PER_USER} predictions for {user.email}")

            db.session.commit()
            print(f"Done - {len(users)} users seeded.")
