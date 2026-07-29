# Student Performance Prediction System

## Project state

**v1.0 (current):** ML pipeline (data ingestion → transformation → training → prediction) behind a
single Flask prediction form. Model is CatBoost/Scikit-learn, serialized as `artifacts/model.pkl` +
`artifacts/preprocessor.pkl`. Dockerized, AWS deployment-ready (Elastic Beanstalk + ECR). No auth, no
DB, no analytics — every prediction is a stateless one-off.

**v2.0 (in progress):** Turning this into a small ML-powered web product:
1. User authentication (login/signup)
2. Prediction history stored per user
3. An analytics dashboard (charts), visible only after login
4. Admin view (stretch) for aggregate stats across all users

See `project-scop.md` in the repo root for the full scope doc (feature list, DB schema, build order).

Build order: DB models → auth → wire prediction pipeline to DB → history page → analytics dashboard →
UI polish → optional admin/API → CI/CD. Each step should leave the app in a runnable state.

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
</content>
</invoke>
