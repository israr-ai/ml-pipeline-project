import enum
import os
from datetime import datetime, timezone

from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def get_database_uri():
    database_url = os.environ.get("DATABASE_URL")
    if database_url:
        if database_url.startswith("postgres://"):
            database_url = database_url.replace("postgres://", "postgresql+psycopg2://", 1)
        elif database_url.startswith("postgresql://"):
            database_url = database_url.replace("postgresql://", "postgresql+psycopg2://", 1)
        return database_url

    required = ["DB_USER", "DB_PASS", "DB_HOST", "DB_NAME"]
    missing = [name for name in required if not os.environ.get(name)]
    if missing:
        raise RuntimeError(
            "Database is not configured: set DATABASE_URL, or all of "
            f"{', '.join(required)}. Missing: {', '.join(missing)}. "
            "See .env.example."
        )

    return (
        f"postgresql+psycopg2://{os.environ['DB_USER']}:{os.environ['DB_PASS']}"
        f"@{os.environ['DB_HOST']}/{os.environ['DB_NAME']}"
    )


class UserRole(enum.Enum):
    USER = "user"
    ADMIN = "admin"


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum(UserRole), default=UserRole.USER, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    reset_token = db.Column(db.String(64), unique=True, nullable=True)
    reset_token_expires_at = db.Column(db.DateTime, nullable=True)

    predictions = db.relationship(
        "Prediction", backref="user", lazy=True, cascade="all, delete-orphan"
    )


class Prediction(db.Model):
    __tablename__ = "predictions"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    race_ethnicity = db.Column(db.String(20), nullable=False)
    parental_education = db.Column(db.String(50), nullable=False)
    lunch = db.Column(db.String(20), nullable=False)
    test_preparation_course = db.Column(db.String(20), nullable=False)
    reading_score = db.Column(db.Float, nullable=False)
    writing_score = db.Column(db.Float, nullable=False)
    predicted_math_score = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
