# Student Performance Prediction System
## Live Demo

Application URL:

https://student-performance-app-bj20.onrender.com

---

## AWS Deployment

Deployed using:

* AWS Elastic Beanstalk
* AWS ECR (Elastic Container Registry)
* AWS CodePipeline

Deployment URL:

http://your-elasticbeanstalk-url.us-east-1.elasticbeanstalk.com

---

## Source Code

GitHub Repository:

https://github.com/israr-ai/ml-pipeline-project

---

## Screenshots

### Home Page

![alt text](assets/image-2.png)

### Prediction Page

![alt text](assets/image.png)

### Prediction Result
![alt text](assets/image-1.png)


## Project Overview

This project is an end-to-end Machine Learning web product that predicts a student's Mathematics score based on demographic and academic factors such as gender, race/ethnicity, parental education level, lunch type, test preparation course, reading score, and writing score.

The project includes data preprocessing, model training, prediction pipeline creation, a Flask web application with user accounts and an analytics dashboard, Docker containerization, and cloud deployment readiness.

---

## Features

* Student score prediction using Machine Learning
* Data preprocessing and feature engineering
* User authentication (signup, login, forgot/reset password)
* Prediction history stored per user (SQLite locally, PostgreSQL in production)
* Analytics dashboard with charts, visible after login
* Admin dashboard with aggregate stats across all users
* JSON REST API for predictions (`/api/predict`), validated with Pydantic
* Flask-based web application with a user-friendly prediction form
* Dockerized application (docker-compose for app + Postgres)
* Production-ready project structure
* AWS and Render deployment support

---

## Project Structure

```text
mlproject/
│
├── artifacts/
│   ├── model.pkl
│   ├── preprocessor.pkl
│   ├── train.csv
│   ├── test.csv
│   └── data.csv
│
├── notebook/
│   └── project.ipynb
│
├── src/
│   ├── components/          # data ingestion, transformation, model training
│   ├── pipeline/             # train/predict pipelines
│   ├── auth/                 # login, signup, password reset routes
│   ├── admin/                 # admin dashboard routes
│   ├── analytics/             # aggregation queries for the dashboard
│   ├── models_db.py           # SQLAlchemy models (User, Prediction, ...)
│   ├── schemas.py             # Pydantic schemas for the REST API
│   ├── exception.py
│   ├── logger.py
│   └── utils.py
│
├── templates/
│   ├── index.html
│   ├── home.html
│   ├── login.html / signup.html
│   ├── forgot_password.html / reset_password.html
│   ├── dashboard.html / _analytics_dashboard.html
│   ├── history.html
│   └── admin.html
│
├── static/js/dashboard.js     # analytics dashboard charts
├── assets/                    # README screenshots
├── application.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── requirements-train.txt
├── setup.py
└── README.md
```

---

## Dataset Features

The model uses the following input features:

* Gender
* Race/Ethnicity
* Parental Level of Education
* Lunch Type
* Test Preparation Course
* Reading Score
* Writing Score

### Target Variable

* Mathematics Score

---

## Technologies Used

### Programming Language

* Python

### Libraries

* Pandas
* NumPy
* Scikit-Learn
* CatBoost
* Dill

### Web Framework

* Flask
* Flask-SQLAlchemy, Flask-Login, Flask-WTF
* Pydantic (REST API validation)

### Database

* SQLite (local development)
* PostgreSQL (production)

### Containerization

* Docker & Docker Compose

### Version Control

* Git & GitHub

### Cloud Deployment

* Render
* AWS Elastic Beanstalk
* AWS ECR
* AWS CodePipeline

---

## Machine Learning Workflow

1. Data Ingestion
2. Data Validation
3. Data Transformation
4. Feature Engineering
5. Model Training
6. Model Evaluation
7. Model Serialization
8. Prediction Pipeline
9. Web Application Development
10. Docker Deployment

---

## Installation

### Clone Repository

```bash
git clone <repository-url>
cd mlproject
```

### Create Virtual Environment

```bash
conda create -p venv python=3.11 -y
conda activate venv
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

To retrain the model locally (data ingestion → transformation → training notebooks/scripts), also
install the training-only extras (CatBoost, XGBoost, Jupyter):

```bash
pip install -r requirements.txt -r requirements-train.txt
```

`requirements.txt` alone is what's used for serving/deployment (Docker, Render) — it stays free of
these heavier training-only packages.

---

## Run Application Locally

```bash
python application.py
```

Open:

```text
http://localhost:5000
```

---

## Running Tests

Install the test-only dependencies (pytest, on top of the serving requirements):

```bash
pip install -r requirements.txt -r requirements-dev.txt
```

Run the suite:

```bash
pytest
```

The suite lives under `tests/` and covers:

* `test_schemas.py` — Pydantic validation for the `/api/predict` request schema
* `test_analytics.py` — dashboard aggregation logic
* `test_predict_pipeline.py` — the prediction pipeline against the real trained model artifacts
* `test_auth.py` — signup, login, logout, and access control on protected routes
* `test_admin.py` — admin-only access and user deletion (including CSRF)
* `test_api_predict.py` — the JSON `/api/predict` endpoint
* `test_e2e_flow.py` — a full user journey (signup → predict → history → dashboard → logout)

Tests run against a temporary on-disk SQLite database (created fresh per run), so they never touch
your local `.env` / `DATABASE_URL` or the production database.

---

## Docker Setup

### Build Docker Image

```bash
docker build -t student-performance .
```

### Run Docker Container

```bash
docker run -p 5000:5000 student-performance
```

Open:

```text
http://localhost:5000
```

---

## Model Performance

The model predicts student mathematics scores based on educational and demographic factors.

Evaluation metrics and model comparison were performed during training to select the best-performing model.

---

## Future Improvements

* CI/CD Pipeline Integration
* Monitoring and Logging
* Model Retraining Pipeline

---

## Author

**Israr Shekh**

Full Stack Developer | Data Science & Machine Learning Enthusiast

Skills:

* Python
* Flask
* Machine Learning
* Docker
* AWS
* Laravel
* Power BI

---

## License

This project is developed for educational and portfolio purposes.
