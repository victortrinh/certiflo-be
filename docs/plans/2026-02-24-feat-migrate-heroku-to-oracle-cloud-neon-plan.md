---
title: "feat: Migrate from Heroku to Oracle Cloud + Neon Postgres"
type: feat
status: active
date: 2026-02-24
origin: docs/brainstorms/2026-02-24-heroku-to-flyio-migration-brainstorm.md
---

# Migrate from Heroku to Oracle Cloud Always Free + Neon Postgres

## Overview

Migrate the Certiflo Flask backend from Heroku (paid) to Oracle Cloud Always Free tier + Neon Postgres (free tier). This eliminates all hosting costs while maintaining always-on availability for the 3 low-traffic portfolio/showcase websites this API serves.

**Approach changed from brainstorm:** Originally planned Fly.io + Neon, but research revealed Fly.io no longer has a free tier (~$0.50-2/month). Pivoted to Oracle Cloud Always Free (truly $0/month forever) per user preference for zero cost. (see brainstorm: `docs/brainstorms/2026-02-24-heroku-to-flyio-migration-brainstorm.md`)

## Problem Statement

The backend is currently hosted on Heroku with Heroku Postgres Essential 0, incurring monthly costs for 3 low-traffic portfolio/showcase websites. The sites receive very few visits per day and don't justify ongoing hosting expenses.

Additionally, the codebase has several issues that should be addressed during migration:
- Database credentials hardcoded in source code (`app/main/config.py:22-31`)
- `manage.py` hardcodes `create_app('dev')` — production runs with DEBUG=True
- Dependencies are from 2019 and have known incompatibilities with modern Python
- `flask-restplus` is abandoned (replaced by `flask-restx`)
- `SECRET_KEY` has a hardcoded fallback value committed to the repo

## Proposed Solution

**Infrastructure:**
- **Compute:** Oracle Cloud Always Free Ampere A1 VM (1 OCPU, 6GB RAM, ARM64, Ubuntu)
- **Database:** Neon Postgres free tier (0.5 GB storage, auto-suspend after 5 min idle, ~1-2s wake)
- **Web server:** nginx reverse proxy with Let's Encrypt SSL
- **App server:** gunicorn + systemd (auto-restart on crash)
- **Cost:** $0/month

**Code changes:**
- Upgrade dependencies to modern versions (Flask 2.x/3.x, flask-restx, PyJWT 2.x, etc.)
- Fix config to read from environment variables (DATABASE_URL, SECRET_KEY)
- Fix `manage.py` to use production config when deployed
- Add SQLAlchemy pool settings for Neon auto-suspend handling

## Technical Approach

### Architecture

```
Internet → Oracle Cloud VM (ports 80/443)
             → nginx (SSL termination, reverse proxy)
               → gunicorn (127.0.0.1:8000, 2 workers)
                 → Flask app (certiflo-be)
                   → Neon Postgres (external, SSL)
```

### Implementation Phases

#### Phase 1: Dependency Upgrade & Config Fixes (Local)

Update the codebase to work with modern Python and read config from environment. All changes tested locally before touching infrastructure.

**1.1 Upgrade dependencies**

Update `requirements.txt`:

```
# requirements.txt
Flask>=3.0,<4.0
flask-restx>=1.3,<2.0          # replaces flask-restplus
Flask-SQLAlchemy>=3.1,<4.0
Flask-Migrate>=4.0,<5.0
Flask-Bcrypt>=1.0,<2.0
Flask-HTTPAuth>=4.8,<5.0
flask-cors>=4.0,<5.0
psycopg2-binary>=2.9,<3.0
PyJWT>=2.8,<3.0
gunicorn>=22.0,<23.0
SQLAlchemy>=1.4,<2.0            # 1.4 is safest upgrade from 1.3
```

Remove unused packages: `Flask-Bootstrap`, `Flask-Login`, `Flask-Mail`, `Flask-RQ2`, `Flask-Script`, `Flask-Testing`, `Flask-WTF`.

**1.2 Replace flask-restplus with flask-restx**

In `app/__init__.py`, change:
```python
# Old
from flask_restplus import Api, Resource
# New
from flask_restx import Api, Resource
```

Apply the same import change across all controller and DTO files. `flask-restx` is a drop-in fork — the API is identical.

**1.3 Fix PyJWT 2.x breaking changes**

In `app/main/model/user.py`:
```python
# Old (PyJWT 1.x): encode returns bytes
return jwt.encode(payload, key, algorithm='HS256')
# PyJWT 2.x: encode returns str — no change needed for encode

# Old (PyJWT 1.x): decode doesn't require algorithms
payload = jwt.decode(auth_token, key)
# New (PyJWT 2.x): algorithms is required
payload = jwt.decode(auth_token, key, algorithms=['HS256'])
```

In `app/main/service/auth_service.py` and `app/main/service/user_service.py`, remove any `.decode('utf-8')` calls on JWT tokens (PyJWT 2.x returns strings, not bytes).

**1.4 Fix config.py — environment variables**

```python
# app/main/config.py
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-only-fallback-key')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,    # Detect stale connections after Neon suspend
        'pool_size': 3,           # Keep pool small for free tier
        'pool_recycle': 280,      # Recycle before Neon's 5-min suspend
    }

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL', 'postgresql://postgres:postgres@localhost:5432/certiflo'
    )

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']  # Fail loud if missing
```

Remove all hardcoded Heroku Postgres credentials from the file.

**1.5 Fix manage.py — config selection from environment**

```python
# manage.py
import os
from flask_migrate import Migrate
from app import blueprint
from app.main import create_app, db

config_name = os.environ.get('FLASK_CONFIG', 'dev')
app = create_app(config_name)
app.register_blueprint(blueprint)

migrate = Migrate(app, db)

if __name__ == '__main__':
    app.run()
```

Remove `Flask-Script` usage (`Manager`, `MigrateCommand`). Flask-Migrate 4.x uses Flask's built-in CLI (`flask db upgrade` instead of `python manage.py db upgrade`).

Update the gunicorn entry point: gunicorn still imports `manage:app`.

**1.6 Fix Flask-SQLAlchemy 3.x changes**

Flask-SQLAlchemy 3.x requires the app context for `db.init_app(app)` but no longer needs `SQLALCHEMY_TRACK_MODIFICATIONS`. The `create_app` factory in `app/main/__init__.py` should work as-is, but verify model definitions still work (3.x changed how `db.Model` metaclass works slightly).

**1.7 Test locally**

```bash
# Install updated deps
pip install -r requirements.txt

# Run with local Postgres
export DATABASE_URL="postgresql://postgres:postgres@localhost:5432/certiflo"
export FLASK_CONFIG="dev"
export SECRET_KEY="test-secret-key"

# Run migrations
flask db upgrade

# Start app
gunicorn manage:app --bind 127.0.0.1:8000

# Test a few endpoints
curl http://localhost:8000/api/resource/getAll
curl http://localhost:8000/api/location/getAll
```

**Success criteria for Phase 1:**
- [x] All imports resolve (no flask-restplus, no Flask-Script)
- [x] App starts without errors
- [ ] GET endpoints return data
- [ ] POST/PUT/DELETE endpoints work with JWT auth
- [ ] `flask db upgrade` runs successfully

---

#### Phase 2: Oracle Cloud VM Setup

**2.1 Create Oracle Cloud account**

1. Sign up at [cloud.oracle.com](https://cloud.oracle.com) (credit card required for identity verification, never charged for Always Free resources)
2. Choose a home region close to your users (Toronto — `ca-toronto-1` recommended for Canadian sites)

**2.2 Provision Always Free Ampere A1 VM**

1. Compute → Instances → Create Instance
2. Image: Ubuntu 22.04 (or 24.04) Minimal — ARM64 (aarch64)
3. Shape: VM.Standard.A1.Flex — 1 OCPU, 6 GB RAM (Always Free eligible)
4. Boot volume: 50 GB (within Always Free 200 GB total)
5. Download the SSH key pair during creation

**2.3 Configure Oracle Cloud networking**

Open ports in the VCN Security List (this is separate from the VM's OS firewall):
1. Virtual Cloud Networks → Select your VCN → Security Lists → Default Security List
2. Add Ingress Rules:
   - Source: `0.0.0.0/0`, Protocol: TCP, Destination Port: 80 (HTTP)
   - Source: `0.0.0.0/0`, Protocol: TCP, Destination Port: 443 (HTTPS)
   - Port 22 (SSH) is already open by default

**2.4 Set up the VM**

SSH into the VM and run:

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python, pip, and build tools (for psycopg2-binary on ARM64)
sudo apt install -y python3 python3-pip python3-venv git nginx certbot python3-certbot-nginx gcc libpq-dev

# Open firewall ports (iptables on Oracle Cloud Ubuntu)
sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport 80 -j ACCEPT
sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport 443 -j ACCEPT
sudo netfilter-persistent save

# Create app user
sudo useradd -m -s /bin/bash certiflo
sudo mkdir -p /opt/certiflo
sudo chown certiflo:certiflo /opt/certiflo
```

**2.5 Deploy the application**

```bash
# As the certiflo user
sudo su - certiflo
cd /opt/certiflo

# Clone the repo
git clone https://github.com/victortrinh/certiflo-be.git app
cd app

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

**2.6 Create environment file**

```bash
# /opt/certiflo/.env
FLASK_CONFIG=prod
DATABASE_URL=postgresql://<user>:<password>@<endpoint>.neon.tech/certiflo?sslmode=require
SECRET_KEY=<generate-with-python3-c-import-secrets-print-secrets.token_hex(32)>
```

**2.7 Create systemd service**

```ini
# /etc/systemd/system/certiflo.service
[Unit]
Description=Certiflo Flask Backend
After=network.target

[Service]
User=certiflo
Group=certiflo
WorkingDirectory=/opt/certiflo/app
EnvironmentFile=/opt/certiflo/.env
ExecStart=/opt/certiflo/app/venv/bin/gunicorn manage:app --bind 127.0.0.1:8000 --workers 2 --timeout 120 --access-logfile - --error-logfile -
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable certiflo
sudo systemctl start certiflo
sudo systemctl status certiflo
```

**2.8 Configure nginx**

```nginx
# /etc/nginx/sites-available/certiflo
server {
    listen 80;
    server_name <your-domain-or-ip>;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/certiflo /etc/nginx/sites-enabled/
sudo rm /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl restart nginx
```

**2.9 Set up SSL with Let's Encrypt**

Note: The domain must already point to the VM's IP for certbot HTTP validation to work. If DNS hasn't been switched yet, use certbot's DNS challenge method or set up SSL after DNS cutover.

```bash
sudo certbot --nginx -d <your-domain>
# Certbot auto-configures nginx for HTTPS and sets up auto-renewal via systemd timer
```

**Success criteria for Phase 2:**
- [ ] VM is running and accessible via SSH
- [ ] Ports 80 and 443 are open (both Oracle Cloud security list AND OS firewall)
- [ ] App starts via systemd and responds on 127.0.0.1:8000
- [ ] nginx proxies to the app and serves on port 80
- [ ] SSL certificate is provisioned and HTTPS works

---

#### Phase 3: Database Migration

**3.1 Create Neon database**

1. Sign up at [console.neon.tech](https://console.neon.tech)
2. Create a new project (region: US East or closest to your Oracle Cloud region)
3. Note both connection strings:
   - **Direct** (for migrations/pg_dump): `postgresql://...@ep-xxx.neon.tech/certiflo?sslmode=require`
   - **Pooled** (for the app): `postgresql://...@ep-xxx-pooler.neon.tech/certiflo?sslmode=require`

**3.2 Check current database size**

```bash
heroku pg:info --app <your-heroku-app-name>
```

Verify the data size is under 0.5 GB (Neon free tier limit). Given this is a CMS for portfolio sites, it should be well under.

**3.3 Export from Heroku Postgres**

```bash
pg_dump --no-owner --no-acl --format=custom \
  "postgres://tvyrdwzbnsjfdf:<password>@ec2-107-20-168-237.compute-1.amazonaws.com:5432/d5c7g5fvfrekii" \
  -f certiflo_backup.dump
```

**3.4 Import to Neon** (use DIRECT connection, not pooled)

```bash
pg_restore --no-owner --no-acl --clean --if-exists \
  -d "postgresql://<neon-user>:<neon-password>@ep-xxx.neon.tech/certiflo?sslmode=require" \
  certiflo_backup.dump
```

**3.5 Fix sequences after restore**

After pg_restore, auto-increment sequences may not be synced with existing data. Run this for each table:

```sql
-- Connect to Neon and run for each table with an id column:
SELECT setval(pg_get_serial_sequence('users', 'id'), COALESCE(MAX(id), 0) + 1, false) FROM users;
SELECT setval(pg_get_serial_sequence('employees', 'id'), COALESCE(MAX(id), 0) + 1, false) FROM employees;
-- ... repeat for all 20 tables
```

**3.6 Validate data**

```sql
-- Compare row counts between Heroku and Neon for each table
SELECT 'users' as tbl, count(*) FROM users
UNION ALL SELECT 'employees', count(*) FROM employees
UNION ALL SELECT 'locations', count(*) FROM locations
UNION ALL SELECT 'products', count(*) FROM products
-- ... all 20 tables

-- Verify French accented text survived
SELECT "nameEn", "nameFr" FROM locations LIMIT 5;

-- Verify large text fields (base64 images)
SELECT id, length(image) FROM "galleryImages" LIMIT 5;
```

**3.7 Run migrations against Neon**

On the Oracle Cloud VM:
```bash
cd /opt/certiflo/app
source venv/bin/activate
export DATABASE_URL="postgresql://...@ep-xxx.neon.tech/certiflo?sslmode=require"  # Direct connection
export FLASK_CONFIG=prod
flask db upgrade
```

**Success criteria for Phase 3:**
- [ ] Neon database created and accessible
- [ ] All data imported — row counts match Heroku
- [ ] French text and large text fields are intact
- [ ] Sequences are correctly set (no duplicate key errors on INSERT)
- [ ] Migrations run successfully against Neon

---

#### Phase 4: Cutover & Verification

**4.1 Verify the Oracle Cloud backend end-to-end**

```bash
# Test public endpoints
curl https://<your-domain>/api/resource/getAll
curl https://<your-domain>/api/location/getAll
curl https://<your-domain>/api/employee/getAll

# Test authentication
curl -X POST https://<your-domain>/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@certiflo.com", "password": "..."}'

# Test authenticated write (use token from login response)
curl -X POST https://<your-domain>/api/resource/save \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"key": "test", "value": "test", "page": "test", "language": "en"}'
```

**4.2 Update frontend websites**

Since the API URL is hardcoded in the frontend code:
1. Find and replace the old Heroku URL with the new Oracle Cloud URL in all 3 frontend codebases
2. Deploy the updated frontends
3. Verify each site loads and displays data correctly

**4.3 Parallel running period**

Keep Heroku running for 1-2 weeks as a rollback target. The frontends now point to Oracle Cloud, but if anything goes wrong, you can revert the frontend URL change.

**4.4 Decommission Heroku**

After the confidence period:
1. Remove the Heroku Postgres add-on
2. Delete the Heroku app
3. Cancel any paid Heroku plans

**Success criteria for Phase 4:**
- [ ] All 3 frontend websites display data correctly from the new backend
- [ ] Admin can log in and perform CRUD operations
- [ ] No errors in `journalctl -u certiflo` logs
- [ ] Heroku decommissioned after confidence period

---

## Alternative Approaches Considered

| Approach | Why Rejected |
|---|---|
| **Fly.io + Neon** | Fly.io deprecated free tier. Pay-as-you-go ~$0.50-2/month. (original brainstorm choice) |
| **Render + Neon** | Truly free but ~30s cold starts after 15 min idle. User prefers always-on. |
| **Stay on Heroku** | Ongoing monthly cost for very low traffic sites. |

(see brainstorm: `docs/brainstorms/2026-02-24-heroku-to-flyio-migration-brainstorm.md`)

## System-Wide Impact

### Interaction Graph

- Frontend websites (3) call backend API via hardcoded URL → URL must change in all 3 frontends
- Backend connects to Postgres via SQLAlchemy → connection string changes from Heroku to Neon
- JWT tokens signed with SECRET_KEY → if key changes, existing sessions are invalidated (acceptable for low-traffic admin panel)
- Database migrations run via `flask db upgrade` → must be run manually on VM (no release phase automation like Heroku)

### Error & Failure Propagation

- **Neon auto-suspend (5 min idle):** First DB query after idle may take ~1-2s. `pool_pre_ping=True` ensures stale connections are replaced before query execution, preventing 500 errors.
- **VM crash:** systemd `Restart=always` restarts gunicorn within 5 seconds. nginx returns 502 during the restart window.
- **SSL certificate expiry:** certbot systemd timer auto-renews. If renewal fails, sites get certificate warnings after 90 days.

### State Lifecycle Risks

- **During migration window:** If both Heroku and Oracle Cloud are live with different databases, writes could go to the wrong DB. Mitigation: update frontend URLs only after Oracle Cloud is verified.
- **Sequence reset:** pg_restore may not sync auto-increment sequences. Explicit `setval()` calls in Phase 3.5 prevent duplicate key errors.

## Acceptance Criteria

### Functional Requirements

- [ ] All 20 GET endpoints return correct data from Neon Postgres
- [ ] JWT authentication works (login, token validation, logout/blacklist)
- [ ] CRUD operations work on all endpoints
- [ ] All 3 frontend websites display correctly with the new backend URL
- [ ] French/English bilingual content displays correctly (accented characters preserved)

### Non-Functional Requirements

- [ ] API responds within 2 seconds (including after Neon cold start)
- [ ] App auto-restarts on crash (systemd)
- [ ] HTTPS with valid SSL certificate
- [ ] No credentials hardcoded in source code
- [ ] Total hosting cost: $0/month

### Quality Gates

- [ ] All dependency upgrades tested locally before deploying
- [ ] Data validation: row counts match between Heroku and Neon
- [ ] Heroku kept as rollback for 1-2 weeks post-migration

## Dependencies & Prerequisites

1. **Oracle Cloud account** with Always Free eligibility (new account required if existing account has used free trial)
2. **Neon account** (free, no credit card required)
3. **Domain name** (if using custom domain for the API — otherwise use the VM's public IP)
4. **Access to all 3 frontend codebases** to update the hardcoded API URL
5. **Heroku CLI** installed locally for `pg_dump` from Heroku Postgres
6. **Local Python 3.11+** for testing dependency upgrades

## Risk Analysis & Mitigation

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Oracle Cloud Always Free VM unavailable in chosen region | Medium | Blocks migration | Try multiple regions; Ampere A1 availability varies |
| Dependencies don't work together after upgrade | Medium | Delays Phase 1 | Test locally first; pin specific versions if needed |
| Data loss during pg_dump/pg_restore | Low | Critical | Validate data counts and content after restore; keep Heroku as backup |
| Oracle Cloud discontinues Always Free tier | Very low | Must re-migrate | Unlikely for existing resources; Oracle has maintained this since 2019 |
| Neon free tier limits exceeded | Low | DB access paused | 0.5 GB and 100 CU-hours is generous for this workload |
| psycopg2-binary wheels unavailable for ARM64 | Low | Blocks VM setup | Install `libpq-dev` and `gcc` to build from source |

## Deploy Process (Ongoing)

After initial setup, deploying code changes:

```bash
# SSH into Oracle Cloud VM
ssh ubuntu@<vm-ip>

# Switch to app user and pull changes
sudo su - certiflo
cd /opt/certiflo/app
git pull origin develop

# Activate venv, install any new deps
source venv/bin/activate
pip install -r requirements.txt

# Run migrations if needed
flask db upgrade

# Restart the service
sudo systemctl restart certiflo
```

Consider writing a simple `deploy.sh` script that wraps these steps.

## Sources & References

### Origin

- **Brainstorm document:** [docs/brainstorms/2026-02-24-heroku-to-flyio-migration-brainstorm.md](docs/brainstorms/2026-02-24-heroku-to-flyio-migration-brainstorm.md) — Key decisions carried forward: free hosting priority, Neon Postgres for database, always-on requirement. Approach changed from Fly.io to Oracle Cloud after discovering Fly.io no longer has a free tier.

### Internal References

- App config: `app/main/config.py` (hardcoded credentials to fix)
- Entry point: `manage.py` (hardcoded dev config to fix)
- Models: `app/main/model/` (20 models, all follow same pattern)
- Auth: `app/main/service/auth_service.py` (JWT handling needs PyJWT 2.x update)

### External References

- [Oracle Cloud Always Free Tier](https://www.oracle.com/cloud/free/)
- [Neon Postgres Free Tier](https://neon.tech/pricing)
- [Neon: Migrate from Heroku](https://neon.com/docs/import/migrate-from-heroku)
- [Neon: SQLAlchemy Connection Guide](https://neon.com/docs/guides/sqlalchemy)
- [flask-restx Documentation](https://flask-restx.readthedocs.io/)
- [PyJWT 2.x Migration Guide](https://pyjwt.readthedocs.io/en/stable/changelog.html)
