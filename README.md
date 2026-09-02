# Assignment Design Assistant

A Flask web app that lets students fill in and save the sections required by
an Applications-Development assignment brief (Design Document → Build →
Testing → Evaluation) directly in a browser, instead of a blank Word file.
Responses are stored in **PostgreSQL** and can be exported to **Excel** by a
tutor/admin for marking or record-keeping. The section structure is generic
enough to reuse for any similar "design → build → test → evaluate"
assignment, on any platform.

## Features
- Guided online form covering Task A–D (Design, Build, Testing, Evaluation)
  exactly as laid out in the assignment brief, with marks shown per section
- Save as **draft** any time, or **Submit Final**
- Re-open and continue a saved draft
- Tutor/admin dashboard (password-protected) listing every submission
- One-click **export to Excel** (`.xlsx`) of all responses for marking
- PostgreSQL storage via SQLAlchemy; schema also provided as raw SQL

## Project structure
```
assignment-writer/
├── app.py            # Flask routes
├── models.py          # SQLAlchemy model + form field definitions
├── extensions.py       # db = SQLAlchemy() (shared instance)
├── schema.sql          # Raw PostgreSQL schema (optional — app also auto-creates it)
├── requirements.txt
├── Procfile             # gunicorn start command for Render/Heroku-style hosts
├── render.yaml           # Render Blueprint (web service + managed Postgres)
├── .env.example
├── templates/
│   ├── base.html
│   ├── form.html
│   ├── success.html
│   ├── admin_login.html
│   └── admin.html
└── static/
    └── style.css
```

## 1. Run locally

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env             # then edit .env with your own values
# quickest local option — SQLite, no Postgres needed:
export DATABASE_URL=sqlite:///local_dev.db
export SECRET_KEY=dev
export ADMIN_PASSWORD=admin123

flask --app app run --debug
```

Visit `http://127.0.0.1:5000`. The tutor dashboard is at `/admin`.

### Using a real local PostgreSQL instead of SQLite
```bash
createdb assignment_writer
export DATABASE_URL=postgresql://postgres:postgres@localhost:5432/assignment_writer
psql "$DATABASE_URL" -f schema.sql     # optional — the app also does this automatically
flask --app app run --debug
```

## 2. Push to GitHub

```bash
cd assignment-writer
git add .
git commit -m "Assignment Design Assistant - initial build"
gh repo create assignment-design-assistant --public --source=. --remote=origin --push
```
(No `gh` CLI? Create an empty repo on github.com, then:)
```bash
git remote add origin https://github.com/<your-username>/assignment-design-assistant.git
git branch -M main
git push -u origin main
```

## 3. Deploy on Render

**Option A — Blueprint (recommended, one click):**
1. Push this repo to GitHub (step 2).
2. In the Render dashboard: **New → Blueprint**, point it at your repo.
   Render reads `render.yaml` and provisions both the web service and a
   free managed PostgreSQL database automatically, wiring `DATABASE_URL`
   for you.
3. Set the `ADMIN_PASSWORD` environment variable in the Render dashboard
   (it's marked `sync: false` in the blueprint so it isn't stored in git).
4. Deploy. Render runs `pip install -r requirements.txt` then
   `gunicorn app:app`.

**Option B — Manual setup:**
1. **New → PostgreSQL** on Render, create a free database, copy its
   *Internal Database URL*.
2. **New → Web Service**, connect your GitHub repo.
   - Build command: `pip install -r requirements.txt`
   - Start command: `gunicorn app:app`
3. Add environment variables on the web service:
   - `DATABASE_URL` = the Postgres URL from step 1
   - `SECRET_KEY` = any random string
   - `ADMIN_PASSWORD` = the password tutors will use to view `/admin`
4. Deploy. The app creates its own table on first boot, or you can run
   `schema.sql` against the database yourself.

## 4. Exporting responses

Log in at `/admin` with `ADMIN_PASSWORD`, then click **Export All to Excel**
to download an `.xlsx` with one row per student and one column per task —
ready to hand to a marker or drop into a gradebook.

## Notes for reuse
The `FIELD_GROUPS` list in `models.py` is the single source of truth for the
form, the confirmation page, and the Excel export column order. To adapt
this app to a *different* assignment brief, edit that list (and the matching
`db.Column` definitions) — everything else (routes, templates, export logic)
stays the same.
