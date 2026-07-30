# Student Performance Prediction System

## Project state

**v1.0:** ML pipeline (data ingestion → transformation → training → prediction) behind a single Flask
prediction form. Model is CatBoost/Scikit-learn, serialized as `artifacts/model.pkl` +
`artifacts/preprocessor.pkl`. No auth, no DB, no analytics — every prediction was a stateless one-off.

**v2.0 (current):** Full ML-powered web product, built on top of v1.0:
1. User authentication (login/signup/forgot-password) — `src/auth/`
2. Predictions persisted per user in the DB (SQLite locally, Postgres in prod) — `src/models_db.py`
3. Prediction history page — `templates/history.html`
4. Analytics dashboard (charts via `static/js/dashboard.js`), visible only after login —
   `src/analytics/`, `templates/_analytics_dashboard.html`
5. Admin dashboard for aggregate stats across all users — `src/admin/`
6. JSON REST API for predictions (`/api/predict`) validated with Pydantic — `src/schemas.py`
7. Dockerized, deployable to Render or AWS (Elastic Beanstalk + ECR)
8. Pytest test suite (unit + route + e2e) under `tests/` — `pytest`

See `project-scop.md` in the repo root for the full scope doc (feature list, DB schema, build order).

Remaining/possible next steps: CI/CD pipeline, model retraining pipeline, richer monitoring.

## Conventions

- **DB models**: every new SQLAlchemy model goes in `src/models_db.py`.
- **Passwords**: hash with `werkzeug.security` (`generate_password_hash` / `check_password_hash`), not
  a custom scheme or a different library.
- **Route handlers**: no unnecessary try/except. Only catch an error if there's a specific, different
  thing to do for that failure — otherwise let it propagate.
- **Data validation**: use Pydantic or WTForms for form/input validation, not manual `request.form.get`
  checks scattered through route handlers.
- **Enums over hardcoded strings**: things like user role (`user` / `admin`) should be Python enums,
  not raw string literals compared around the codebase.
- **Reusable logic**: extract shared logic into `src/utils.py` or a dedicated module — don't duplicate
  it across routes/components.
- **Frontend styling**: Tailwind CSS (CDN, `<script src="https://cdn.tailwindcss.com">`), matching
  `templates/home.html` and `templates/index.html`. Don't introduce Bootstrap or another CSS framework
  — keep new templates (login, signup, dashboard, history) visually consistent with the existing ones.
- **Tests**: every new route/model/module should get pytest coverage in `tests/`, mirroring the
  existing split — pure-logic unit tests (`test_schemas.py`, `test_analytics.py`), route tests via the
  Flask test client (`test_auth.py`, `test_admin.py`, `test_api_predict.py`), and full-journey tests in
  `test_e2e_flow.py`. Tests run against a temp on-disk SQLite DB (set up in `tests/conftest.py`) so they
  never touch the real `DATABASE_URL`. Admin routes use manual `validate_csrf()` (not `FlaskForm`), so
  it isn't bypassed by `WTF_CSRF_ENABLED=False` — tests that POST to them must fetch a real token first
  (see `test_admin.py::test_admin_can_delete_other_user`).
