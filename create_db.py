from application import application
from src.models_db import db

if __name__ == "__main__":
    with application.app_context():
        db.create_all()
        print("Tables created at", application.config["SQLALCHEMY_DATABASE_URI"])
