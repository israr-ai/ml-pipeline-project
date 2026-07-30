import os
import sys
import tempfile
from pathlib import Path

import pytest

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

_tmp_dir = tempfile.mkdtemp(prefix="mlproject-tests-")
os.environ["DATABASE_URL"] = f"sqlite:///{Path(_tmp_dir, 'test.db').as_posix()}"
os.environ.setdefault("SECRET_KEY", "test-secret-key")

from application import application as flask_app  # noqa: E402
from src.models_db import User, UserRole, db  # noqa: E402


@pytest.fixture(scope="session")
def app():
    flask_app.config.update(TESTING=True, WTF_CSRF_ENABLED=False)
    yield flask_app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture(autouse=True)
def _clean_db(app):
    yield
    with app.app_context():
        db.session.remove()
        for table in reversed(db.metadata.sorted_tables):
            db.session.execute(table.delete())
        db.session.commit()


@pytest.fixture()
def make_user(app):
    from werkzeug.security import generate_password_hash

    def _make_user(email="user@example.com", password="password123", name="Test User", role=UserRole.USER):
        with app.app_context():
            user = User(
                name=name,
                email=email,
                password_hash=generate_password_hash(password),
                role=role,
            )
            db.session.add(user)
            db.session.commit()
            return user.id

    return _make_user
