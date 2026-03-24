# Brainstorm: Migrate from Heroku to Fly.io + Neon Postgres

**Date:** 2026-02-24
**Status:** Approved
**Participants:** Victor, Claude

## What We're Building

Migration of the Certiflo Flask backend from Heroku (paid) to Fly.io + Neon Postgres (free). This backend serves 3 similar low-traffic portfolio/showcase websites as a bilingual CRUD API.

## Why This Approach

**Current state:**
- Heroku hosting with Heroku Postgres Essential 0 (paid)
- Flask 1.0.2 API with 20 endpoints, ~3,800 lines of code
- No background workers, no file storage, no Redis in use
- Very low traffic portfolio sites

**Goal:** Eliminate hosting costs while maintaining always-on availability.

**Why Fly.io + Neon over alternatives:**
- **Render (rejected):** Free tier sleeps after 15 min, causing ~30s cold starts
- **Oracle Cloud VPS (rejected):** Too much maintenance overhead for portfolio sites
- **Railway (rejected):** No free tier available
- Fly.io free tier keeps VMs running 24/7 (no cold starts)
- Neon free Postgres wakes in ~1-2s (negligible vs 30s compute cold starts)
- Reasonable setup complexity — needs a Dockerfile but the app is simple

## Key Decisions

1. **Hosting platform:** Fly.io (free tier — 3 shared-CPU VMs, 256MB RAM each)
2. **Database:** Neon Postgres (free tier — 0.5 GB storage, auto-suspend after 5 min idle with ~1-2s wake)
3. **Database migration:** Export from Heroku Postgres via `pg_dump`, import to Neon via `pg_restore` or `psql`
4. **Containerization:** Add Dockerfile for Fly.io deployment (gunicorn + Flask)
5. **Config cleanup:** Move hardcoded database URL to environment variable (`DATABASE_URL`)
6. **Deploy workflow:** `fly deploy` from CLI (optionally add GitHub Actions later)

## Migration Steps (High Level)

1. Create Neon Postgres database
2. Export Heroku Postgres data with `pg_dump`
3. Import data into Neon with `psql`/`pg_restore`
4. Update app config to read `DATABASE_URL` from environment
5. Create Dockerfile for the Flask app
6. Create `fly.toml` configuration
7. Deploy to Fly.io with `fly deploy`
8. Set environment variables (DATABASE_URL, SECRET_KEY)
9. Verify all 3 websites work against the new backend
10. Update DNS/frontend configs to point to the Fly.io URL
11. Decommission Heroku

## Open Questions

None — approach is agreed upon. Details to be worked out during planning phase.

## Context

- App uses old dependencies (Flask 1.0.2, flask-restplus — deprecated in favor of flask-restx)
- Database URL is currently hardcoded in config.py — must be fixed during migration
- `manage.py` hardcodes `create_app('dev')` — needs a production config path
- No tests exist in the codebase
- Procfile release phase runs `python manage.py db upgrade` — need equivalent on Fly.io
