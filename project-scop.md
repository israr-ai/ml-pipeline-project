# Student Performance Prediction System — Project Scope v2.0

## 1. Current State (v1.0)

- ML pipeline: data ingestion → transformation → training → prediction
- Flask web app with a single prediction form
- Model: CatBoost/Scikit-learn, serialized as `model.pkl` + `preprocessor.pkl`
- Dockerized, AWS deployment-ready (Elastic Beanstalk + ECR + CodePipeline)
- No authentication, no data persistence, no analytics

**Gap:** every prediction is a one-off — nothing is stored, no one can see trends, and anyone can hit the form.

---

## 2. Goal for v2.0

Turn the project from a "single prediction form" into a small **ML-powered web product** with:

1. User authentication (login/signup)
2. Prediction history stored per user
3. An analytics dashboard (charts) — **visible only after login**
4. Admin view (optional) to see aggregate stats across all users

---

## 3. Proposed Feature List

### A. Authentication (Priority: High)
- Signup / Login / Logout
- Session-based auth using **Flask-Login**
- Password hashing with `werkzeug.security` or `bcrypt`
- Route protection: `/dashboard`, `/history`, `/analytics` require login; `/`, `/predict` can stay public or also be gated — your call
- Optional: role field (`user` / `admin`) for future admin dashboard

### B. Database Layer (Priority: High)
Currently there's no DB — you're only working with CSVs in `artifacts/`. You'll need one to store users and predictions.

- **Dev:** SQLite (zero-config, fine for a portfolio project)
- **Prod (AWS):** PostgreSQL via AWS RDS (free tier eligible)
- Use **SQLAlchemy** as ORM (works with both without code changes)

**Suggested tables:**
```
users
 ├── id, name, email, password_hash, role, created_at

predictions
 ├── id, user_id (FK), gender, race_ethnicity, parental_education,
 │   lunch, test_prep, reading_score, writing_score,
 │   predicted_math_score, created_at
```

### C. Prediction History (Priority: Medium)
- After every prediction, save the input + output row to the `predictions` table (linked to `user_id`)
- `/history` page: paginated table of a user's past predictions

### D. Analytics Dashboard (Priority: High — this is the core ask)
A `/dashboard` or `/analytics` page, **login-required**, showing:

| Chart | Type | What it shows |
|---|---|---|
| Score distribution | Bar chart | Avg predicted math score by gender / by test prep completion |
| Score by parental education | Bar chart | Avg math score grouped by parental education level |
| Lunch type impact | Pie chart | % split of predictions by lunch type, or avg score by lunch type |
| Test prep effect | Pie / Bar | Completed vs not-completed test prep — score comparison |
| Personal trend | Line chart | Logged-in user's own predictions over time |
| Overall stats cards | Numbers | Total predictions made, average predicted score, highest/lowest |

**Tech for charts:**
- Simplest: **Chart.js** (CDN, no build step, works great with Flask/Jinja templates)
- Alternative: **Plotly** if you want more interactive charts
- Data flow: Flask route queries DB → aggregates with Pandas → passes JSON to template → Chart.js renders it

This fits your stack well since you're already using Pandas.

### E. Admin Panel (Priority: Low / stretch goal)
- Only visible to `role == admin`
- See aggregate analytics across **all users**, not just one
- Manage users (view/delete)

### F. API Layer (Priority: Low / stretch goal)
- Expose `/api/predict` as a JSON REST endpoint (separate from the HTML form)
- Useful if you ever want a React/Vue frontend or mobile client later
- Also looks good on a resume — "built REST API alongside web UI"

### G. CI/CD (already planned in your README)
- GitHub Actions or AWS CodePipeline: run tests → build Docker image → push to ECR → deploy to Elastic Beanstalk on every push to `main`

### H. Monitoring/Logging (already planned)
- You already have `logger.py` — extend it to log predictions and errors
- Optional: hook into AWS CloudWatch once deployed

---

## 4. Updated Project Structure

```text
mlproject/
│
├── artifacts/
│   ├── model.pkl
│   ├── preprocessor.pkl
│   └── ...
│
├── src/
│   ├── components/
│   ├── pipeline/
│   ├── auth/                  # NEW — login/signup logic
│   ├── analytics/              # NEW — aggregation queries for dashboard
│   ├── models_db.py            # NEW — SQLAlchemy models (User, Prediction)
│   ├── exception.py
│   ├── logger.py
│   └── utils.py
│
├── templates/
│   ├── index.html
│   ├── home.html
│   ├── login.html              # NEW
│   ├── signup.html             # NEW
│   ├── dashboard.html          # NEW — charts live here
│   └── history.html            # NEW
│
├── static/
│   └── js/dashboard.js         # NEW — Chart.js rendering logic
│
├── application.py
├── Dockerfile
├── requirements.txt
└── README.md
```

---

## 5. New Dependencies to Add

```text
flask-login
flask-sqlalchemy
werkzeug
psycopg2-binary   # only needed for Postgres in prod
```

(Chart.js is CDN-based — no pip install needed.)

---

## 6. Suggested Build Order (good for Claude Code sessions)

1. **DB models** — set up SQLAlchemy, `User` and `Prediction` models, run migrations
2. **Auth** — signup/login/logout, protect routes
3. **Wire prediction pipeline to DB** — every prediction saved with `user_id`
4. **History page** — simple table first, no charts yet
5. **Analytics dashboard** — Flask route to aggregate data with Pandas → Chart.js
6. **Polish UI** — Bootstrap/Tailwind for login + dashboard pages
7. **(Optional) Admin panel**
8. **(Optional) REST API**
9. **CI/CD + deploy**

Doing it in this order means at every step the app still runs — good for incremental commits.

---

## 7. Open Decisions (your call)

- Should the prediction form itself require login, or just the dashboard/history?
- SQLite for now, migrate to Postgres later — or start directly with Postgres on RDS?
- Chart.js (simpler, faster to ship) vs Plotly (more interactive, slightly heavier)?