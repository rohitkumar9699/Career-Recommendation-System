# Career Recommendation System

A Django REST API and Angular 18 single-page application for student registration, authentication, academic assessment, career recommendations, profile updates, and administrator student-record management. Recommendations are generated from the bundled model and scaler files in `Backend/model/`.

## Purpose

The purpose of this project is to help students, especially those from **rural areas**, discover a wider range of career opportunities when they are transitioning from school to higher education or professional life.

## Problem Statement

In rural areas, many children are aware of only **10–15 common career choices**, such as engineering, medicine, teaching, or government jobs. However, there are **200+ career paths and opportunities** available across different fields.

Due to limited career awareness, guidance, and access to reliable information, students may choose careers based only on what they already know rather than exploring options that match their **interests, skills, and abilities**.

## Our Solution

Our project aims to bridge this career-awareness gap by collecting relevant information about students and using it to provide **personalized career recommendations**.

The system helps students:

- Explore a wider range of career options.
- Discover careers they may not have previously known about.
- Receive career recommendations based on their provided information and assessment results.
- Make more informed career decisions after completing school.

The goal is to ensure that **limited career awareness does not limit a student's future opportunities**.

## Requirements

- Python 3.10 or newer
- Node.js and npm
- A PostgreSQL database for persistent production deployment (local development uses SQLite)

## Project Structure

```text
Backend/
  api/                         Django app, API views, serializers, models, and ML logic
  career_recommendation_system/ Django project settings and WSGI configuration
  model/                       ourmodel.pkl and scaler.pkl
  manage.py
  requirements.txt
frontend/
  src/app/                     Angular component and API services
  public/                      Static assets
  angular.json
  package.json
  proxy.conf.json              Local `/api` proxy to Django
Backend/vercel.json             Vercel Python function configuration
frontend/vercel.json            Vercel Angular build and routing configuration
```

## Backend Setup

```powershell
cd Backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

The API is available at `http://localhost:8000/`. The local database is `Backend/db.sqlite3`. Create an administrator account for Django admin with `python manage.py createsuperuser` if needed.

### Backend Configuration

The default settings use SQLite. Set these environment variables when using PostgreSQL/Supabase:

- `USE_SUPABASE_DB=1`
- `SUPABASE_DB_URL` or `DATABASE_URL`
- `SUPABASE_DB_NAME` (default `postgres`)
- `SUPABASE_DB_USER` (default `postgres`)
- `SUPABASE_DB_PASSWORD`
- `SUPABASE_DB_HOST`
- `SUPABASE_DB_PORT` (default `5432`)

Optional settings are `DJANGO_SECRET_KEY` and `DJANGO_DEBUG`. `DJANGO_DEBUG` is enabled when set to `1`; otherwise it is disabled.

## Frontend Setup

With the backend running:

```powershell
cd frontend
npm install
npm start
```

Open `http://localhost:4200/`. The Angular development proxy sends `/api` requests to `http://localhost:8000`. A production build can be created with:

```powershell
npm run build
```

The build is written to `frontend/dist/frontend/browser`. Unit tests use Karma:

```powershell
npm test
```

## API

All application endpoints use the `/api/` prefix. JWT-protected endpoints require `Authorization: Bearer <access-token>`.

| Method | Endpoint | Purpose |
| --- | --- | --- |
| GET | `/api/health/` | Health check |
| POST | `/api/register/` | Register a student with `username`, `email`, `password`, `mobile`, and `gender` |
| POST | `/api/login/` | Student login with `email` and `password`; returns student data and access/refresh JWTs |
| GET | `/api/students/me/` | Return the authenticated student profile |
| PUT | `/api/students/update/` | Update authenticated student `name` and 10-digit `mobile` |
| POST | `/api/assessment/submit/` | Submit one assessment and return three recommendations |
| POST | `/api/token/` | SimpleJWT token endpoint |
| POST | `/api/token/refresh/` | Refresh a JWT |
| POST | `/api/admin/login/` | Admin login with `email` and `password` |
| GET | `/api/admin/students/` | List student records |
| POST | `/api/admin/search/` | Find a student by `{ "email": "..." }` |
| POST | `/api/admin/delete/` | Delete a student by `{ "student_id": <id> }` |

Assessment submissions require `gender`, `absence_days`, `weekly_self_study_hours`, and scores for `math_score`, `history_score`, `physics_score`, `chemistry_score`, `biology_score`, `english_score`, and `geography_score`. Scores must be from 0 to 100. The frontend also sends `part_time_job`, `extracurricular_activities`, `total_score`, and `average_score`.

The current admin endpoints are publicly permitted by the Django views and use the stored `AdminUser` password value directly. Protect them before exposing the API publicly.

## Deploying on Vercel

Deploy the backend and frontend as two separate Vercel projects.

### 1. Deploy Django

1. Create a Vercel project from this repository and set its **Root Directory** to `Backend`.
2. Keep the included `Backend/vercel.json`; it sends requests to `api/index.py`, which loads the Django WSGI application.
3. Add production environment variables in Vercel: `DJANGO_SECRET_KEY`, `DJANGO_DEBUG=0`, `USE_SUPABASE_DB=1`, and the PostgreSQL variables listed above.
4. Run migrations against the production PostgreSQL database before using the API:

   ```powershell
   cd Backend
   $env:USE_SUPABASE_DB="1"
   $env:SUPABASE_DB_URL="<postgres-connection-url>"
   python manage.py migrate
   ```

   Do not use the default SQLite database for production: Vercel function storage is not a persistent application database.
5. Confirm the deployment with `https://<backend-project>.vercel.app/api/health/`.

The trained files `Backend/model/ourmodel.pkl` and `Backend/model/scaler.pkl` must remain in the deployment.

### 2. Deploy Angular

1. Create a second Vercel project from the same repository and set its **Root Directory** to `frontend`.
2. In the applicable Vercel config (`vercel.json` at the repository root when Root Directory is the repository, or `frontend/vercel.json` when Root Directory is `frontend`), replace `REPLACE_WITH_BACKEND_PROJECT.vercel.app` with the deployed backend hostname.
3. Deploy. The configuration runs `npm run build`, serves Angular's `dist/frontend/browser` output, proxies `/api/*` to Django, and rewrites other paths to `index.html` for the single-page application.

The frontend source uses same-origin `/api` URLs, so local requests use `frontend/proxy.conf.json` and deployed requests use the Vercel rewrite.

## License

No license file is currently included in this repository.
