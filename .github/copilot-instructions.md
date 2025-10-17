### Copilot instructions for the Mergington High School demo app

This file gives concise, action-oriented guidance so an AI coding agent can be productive immediately in this repository.

1) Big-picture architecture (what matters)
- Backend: FastAPI app located at `src/app.py` and `src/backend/routers/*.py`. Key components:
  - `src/app.py` mounts the static frontend (`/static`) and includes routers `activities` and `auth`.
  - `src/backend/database.py` provides the data layer. During local development this repo uses an in-memory collection implementation; production originally intended to use MongoDB (see original comments).
  - Routers implement endpoints in `src/backend/routers/activities.py` and `src/backend/routers/auth.py`. Modify these to change API behaviour.
- Frontend: static single-page UI in `src/static/` (HTML, CSS, JS). `src/static/app.js` fetches `/activities` and renders cards; filters/search/registration all happen client-side.

2) How the data flows
- Frontend calls GET `/activities` (with optional day/start_time/end_time query params). Backend `activities` router queries `activities_collection` and returns a dict keyed by activity name.
- POST `/activities/{activity_name}/signup` and `/unregister` require a `teacher_username` query param (basic auth-like flow) and update `participants` on the backend collection.
- `database.init_database()` seeds the activities from `initial_activities` when the app starts if the collection is empty.

3) Developer workflows / important commands
- Run locally (from project root):
  - Create and activate venv (project already has `.venv` in the dev container):

    ```bash
    source .venv/bin/activate
    ```

  - Install dependencies (if needed):

    ```bash
    pip install -r src/requirements.txt
    ```

  - Start the app (from the `src` directory):

    ```bash
    PYTHONPATH=. .venv/bin/python -m uvicorn app:app --reload --port 8001
    ```

  - Open the frontend at: `http://localhost:8001/static/index.html` and API docs at `http://localhost:8001/docs`.

- Tests: there are no unit tests in the repo. When adding tests, prefer pytest and place tests under `tests/`.

4) Project-specific conventions and patterns
- The repo favors small explicit modules: routers in `src/backend/routers/*`, data seeded in `database.py` as `initial_activities`.
- Activities are represented as dicts keyed by name with fields:
  - `description`, `schedule` (human), `schedule_details` (structured: days, start_time, end_time), `max_participants`, `participants` (list of emails).
- The frontend infers categories (sports/arts/academic/community/technology) by heuristics in `src/static/app.js` — change here to adjust category mapping.
- Authentication is intentionally lightweight: teacher login returns user info; the frontend stores it in localStorage and passes `teacher_username` as a query param for protected actions.

5) Integration points & external dependencies
- MongoDB: the original production code expected MongoDB (`pymongo`), but the repo includes an in-memory fallback used in development. If you re-enable MongoDB, update `src/backend/database.py` and environment for `MongoClient('mongodb://localhost:27017/')`.
- Argon2 is used to hash teacher passwords in `database.py`.

6) Common changes and examples
- Add a new activity: update `initial_activities` in `src/backend/database.py` (this seeds new activity on init) and restart the app. Example entry format exists in that file.
- Change activity filtering behaviour: modify `src/static/app.js` functions `getActivityType`, `formatSchedule`, and `displayFilteredActivities`.
- Adjust signup/unregister flows: edit endpoints in `src/backend/routers/activities.py`.

7) Safety and testing notes for agents
- Be conservative editing API signatures. Many UI behaviors depend on exact JSON shapes (frontend expects `schedule_details` and `participants` arrays).
- When adding or renaming fields, update both backend and frontend together.

8) Quick checklist for PRs by an AI agent
- Run `python -m pip install -r src/requirements.txt` in the project venv (if dependencies changed).
- Run the server locally and verify the frontend renders and `/activities` returns expected JSON.
- If changing any API shapes, update `src/static/app.js` accordingly; ensure no console errors in the browser.
- Add or update small unit tests under `tests/` where appropriate.

If anything above is unclear, tell me which area you'd like more examples for (frontend rendering, router APIs, or database seeding) and I'll extend this doc.
