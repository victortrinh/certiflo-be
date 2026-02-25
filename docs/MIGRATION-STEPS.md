# Migration Steps: Heroku to Oracle Cloud + Neon Postgres

Step-by-step checklist for the manual infrastructure work. Phase 1 (code changes) is already done on branch `feat/migrate-heroku-to-oracle-cloud`.

---

## Phase 2: Oracle Cloud VM Setup

### Step 1: Create Oracle Cloud Account

1. Go to https://cloud.oracle.com and sign up
2. Credit card required for identity verification (never charged for Always Free resources)
3. Choose home region: **Toronto (ca-toronto-1)** recommended for Canadian sites

### Step 2: Provision the VM

1. Go to **Compute > Instances > Create Instance**
2. Settings:
   - **Image:** Ubuntu 22.04 (or 24.04) Minimal — ARM64 (aarch64)
   - **Shape:** VM.Standard.A1.Flex — **1 OCPU, 6 GB RAM** (Always Free eligible)
   - **Boot volume:** 50 GB
3. Download the SSH key pair during creation
4. Note the **public IP address** once the instance is running

> If Ampere A1 shape is unavailable in your region, try a different region. Availability varies.

### Step 3: Open Firewall Ports (Oracle Cloud Console)

This is separate from the VM's OS firewall — both must be configured.

1. Go to **Virtual Cloud Networks > [your VCN] > Security Lists > Default Security List**
2. Add **Ingress Rules:**

| Source CIDR | Protocol | Dest Port | Description |
|---|---|---|---|
| `0.0.0.0/0` | TCP | 80 | HTTP |
| `0.0.0.0/0` | TCP | 443 | HTTPS |

Port 22 (SSH) is already open by default.

### Step 4: SSH In and Set Up the VM

```bash
ssh -i /path/to/your-key.pem ubuntu@<VM_PUBLIC_IP>
```

Then run:

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python, pip, build tools, nginx, certbot
sudo apt install -y python3 python3-pip python3-venv git nginx certbot python3-certbot-nginx gcc libpq-dev

# Open OS firewall ports (iptables on Oracle Cloud Ubuntu)
sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport 80 -j ACCEPT
sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport 443 -j ACCEPT
sudo netfilter-persistent save

# Create app user
sudo useradd -m -s /bin/bash certiflo
sudo mkdir -p /opt/certiflo
sudo chown certiflo:certiflo /opt/certiflo
```

### Step 5: Deploy the Application

```bash
# Switch to app user
sudo su - certiflo
cd /opt/certiflo

# Clone the repo (use the migration branch)
git clone -b feat/migrate-heroku-to-oracle-cloud https://github.com/victortrinh/certiflo-be.git app
cd app

# Create virtual environment and install deps
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 6: Create Environment File

Generate a secret key first:

```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```

Then create the env file (fill in your Neon credentials from Phase 3, or use a placeholder for now):

```bash
sudo tee /opt/certiflo/.env > /dev/null << 'EOF'
FLASK_CONFIG=prod
DATABASE_URL=postgresql://<NEON_USER>:<NEON_PASSWORD>@<NEON_ENDPOINT>.neon.tech/certiflo?sslmode=require
SECRET_KEY=<PASTE_GENERATED_KEY_HERE>
EOF

# Restrict permissions
sudo chown certiflo:certiflo /opt/certiflo/.env
sudo chmod 600 /opt/certiflo/.env
```

### Step 7: Create systemd Service

```bash
sudo tee /etc/systemd/system/certiflo.service > /dev/null << 'EOF'
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
EOF

sudo systemctl daemon-reload
sudo systemctl enable certiflo
sudo systemctl start certiflo
```

Verify it's running:

```bash
sudo systemctl status certiflo
# Should show "active (running)"

curl http://127.0.0.1:8000/api/resource/getAll
# Should return JSON (or connection error if DB isn't set up yet)
```

### Step 8: Configure nginx

```bash
sudo tee /etc/nginx/sites-available/certiflo > /dev/null << 'EOF'
server {
    listen 80;
    server_name <YOUR_DOMAIN_OR_IP>;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
EOF

sudo ln -s /etc/nginx/sites-available/certiflo /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl restart nginx
```

Test from your local machine:

```bash
curl http://<VM_PUBLIC_IP>/api/resource/getAll
```

### Step 9: Set Up SSL (after DNS is pointed to the VM)

```bash
sudo certbot --nginx -d <your-domain>
```

Certbot will auto-configure nginx for HTTPS and set up auto-renewal.

### Phase 2 Checklist

- [ ] VM running and accessible via SSH
- [ ] Ports 80 + 443 open (Oracle Cloud security list AND OS iptables)
- [ ] App starts via systemd (`systemctl status certiflo` shows active)
- [ ] nginx proxies to the app on port 80
- [ ] SSL certificate provisioned (after DNS cutover)

---

## Phase 3: Database Migration

### Step 10: Create Neon Database

1. Go to https://console.neon.tech and sign up (free, no credit card)
2. Create a new project:
   - **Name:** certiflo
   - **Region:** US East (or closest to your Oracle Cloud region)
3. Note **both** connection strings from the dashboard:
   - **Direct** (for migrations/pg_dump): `postgresql://...@ep-xxx.neon.tech/certiflo?sslmode=require`
   - **Pooled** (for the app): `postgresql://...@ep-xxx-pooler.neon.tech/certiflo?sslmode=require`

### Step 11: Check Heroku Database Size

```bash
heroku pg:info --app certiflo-be
```

Verify the data is under 0.5 GB (Neon free tier limit).

### Step 12: Export from Heroku Postgres

Run this on your local machine (needs `pg_dump` installed):

```bash
# Get the database URL from Heroku
heroku config:get DATABASE_URL --app certiflo-be

# Export the database
pg_dump --no-owner --no-acl --format=custom \
  "<HEROKU_DATABASE_URL>" \
  -f certiflo_backup.dump
```

### Step 13: Import to Neon

Use the **direct** connection string (NOT pooled):

```bash
pg_restore --no-owner --no-acl --clean --if-exists \
  -d "postgresql://<NEON_USER>:<NEON_PASSWORD>@<NEON_DIRECT_ENDPOINT>.neon.tech/certiflo?sslmode=require" \
  certiflo_backup.dump
```

Some errors about dropping non-existent objects are normal with `--clean --if-exists`.

### Step 14: Fix Sequences

After pg_restore, auto-increment sequences may be out of sync. Connect to Neon and run:

```bash
psql "postgresql://<NEON_USER>:<NEON_PASSWORD>@<NEON_DIRECT_ENDPOINT>.neon.tech/certiflo?sslmode=require"
```

Then execute:

```sql
SELECT setval(pg_get_serial_sequence('"users"', 'id'), COALESCE(MAX(id), 0) + 1, false) FROM "users";
SELECT setval(pg_get_serial_sequence('"employees"', 'id'), COALESCE(MAX(id), 0) + 1, false) FROM "employees";
SELECT setval(pg_get_serial_sequence('"locations"', 'id'), COALESCE(MAX(id), 0) + 1, false) FROM "locations";
SELECT setval(pg_get_serial_sequence('"products"', 'id'), COALESCE(MAX(id), 0) + 1, false) FROM "products";
SELECT setval(pg_get_serial_sequence('"resources"', 'id'), COALESCE(MAX(id), 0) + 1, false) FROM "resources";
SELECT setval(pg_get_serial_sequence('"telephones"', 'id'), COALESCE(MAX(id), 0) + 1, false) FROM "telephones";
SELECT setval(pg_get_serial_sequence('"emails"', 'id'), COALESCE(MAX(id), 0) + 1, false) FROM "emails";
SELECT setval(pg_get_serial_sequence('"openings"', 'id'), COALESCE(MAX(id), 0) + 1, false) FROM "openings";
SELECT setval(pg_get_serial_sequence('"manufacturer"', 'id'), COALESCE(MAX(id), 0) + 1, false) FROM "manufacturer";
SELECT setval(pg_get_serial_sequence('"manufacturerImages"', 'id'), COALESCE(MAX(id), 0) + 1, false) FROM "manufacturerImages";
SELECT setval(pg_get_serial_sequence('"realizations"', 'id'), COALESCE(MAX(id), 0) + 1, false) FROM "realizations";
SELECT setval(pg_get_serial_sequence('"realizationTypes"', 'id'), COALESCE(MAX(id), 0) + 1, false) FROM "realizationTypes";
SELECT setval(pg_get_serial_sequence('"tankers"', 'id'), COALESCE(MAX(id), 0) + 1, false) FROM "tankers";
SELECT setval(pg_get_serial_sequence('"tankerTypes"', 'id'), COALESCE(MAX(id), 0) + 1, false) FROM "tankerTypes";
SELECT setval(pg_get_serial_sequence('"assemblies"', 'id'), COALESCE(MAX(id), 0) + 1, false) FROM "assemblies";
SELECT setval(pg_get_serial_sequence('"assemblyTypes"', 'id'), COALESCE(MAX(id), 0) + 1, false) FROM "assemblyTypes";
SELECT setval(pg_get_serial_sequence('"galleries"', 'id'), COALESCE(MAX(id), 0) + 1, false) FROM "galleries";
SELECT setval(pg_get_serial_sequence('"galleryImages"', 'id'), COALESCE(MAX(id), 0) + 1, false) FROM "galleryImages";
SELECT setval(pg_get_serial_sequence('"jobPostings"', 'id'), COALESCE(MAX(id), 0) + 1, false) FROM "jobPostings";
SELECT setval(pg_get_serial_sequence('"blacklist_tokens"', 'id'), COALESCE(MAX(id), 0) + 1, false) FROM "blacklist_tokens";
```

### Step 15: Validate Data

Run this on Neon to get row counts, then compare with Heroku:

```sql
SELECT 'users' as tbl, count(*) FROM "users"
UNION ALL SELECT 'employees', count(*) FROM "employees"
UNION ALL SELECT 'locations', count(*) FROM "locations"
UNION ALL SELECT 'products', count(*) FROM "products"
UNION ALL SELECT 'resources', count(*) FROM "resources"
UNION ALL SELECT 'telephones', count(*) FROM "telephones"
UNION ALL SELECT 'emails', count(*) FROM "emails"
UNION ALL SELECT 'openings', count(*) FROM "openings"
UNION ALL SELECT 'manufacturer', count(*) FROM "manufacturer"
UNION ALL SELECT 'manufacturerImages', count(*) FROM "manufacturerImages"
UNION ALL SELECT 'realizations', count(*) FROM "realizations"
UNION ALL SELECT 'realizationTypes', count(*) FROM "realizationTypes"
UNION ALL SELECT 'tankers', count(*) FROM "tankers"
UNION ALL SELECT 'tankerTypes', count(*) FROM "tankerTypes"
UNION ALL SELECT 'assemblies', count(*) FROM "assemblies"
UNION ALL SELECT 'assemblyTypes', count(*) FROM "assemblyTypes"
UNION ALL SELECT 'galleries', count(*) FROM "galleries"
UNION ALL SELECT 'galleryImages', count(*) FROM "galleryImages"
UNION ALL SELECT 'jobPostings', count(*) FROM "jobPostings"
UNION ALL SELECT 'blacklist_tokens', count(*) FROM "blacklist_tokens"
ORDER BY tbl;

-- Verify French accented text survived
SELECT "nameEn", "nameFr" FROM "locations" LIMIT 5;

-- Verify large text fields (base64 images)
SELECT id, length(image) FROM "galleryImages" LIMIT 5;
```

### Step 16: Update Environment File with Neon Credentials

Now that Neon is set up, update the env file on the Oracle Cloud VM:

```bash
ssh ubuntu@<VM_PUBLIC_IP>
sudo nano /opt/certiflo/.env
# Update DATABASE_URL with the actual Neon DIRECT connection string

# Restart the app
sudo systemctl restart certiflo
```

### Step 17: Run Migrations on Neon

```bash
sudo su - certiflo
cd /opt/certiflo/app
source venv/bin/activate
export FLASK_APP=manage:app
flask db upgrade
```

### Phase 3 Checklist

- [ ] Neon database created and accessible
- [ ] Data imported — row counts match Heroku
- [ ] French text and large text fields are intact
- [ ] Sequences correctly set (no duplicate key errors on INSERT)
- [ ] Migrations run successfully against Neon
- [ ] App on Oracle Cloud connects to Neon and returns data

---

## Phase 4: Cutover & Verification

### Step 18: Verify End-to-End

```bash
# Test public endpoints
curl https://<YOUR_DOMAIN>/api/resource/getAll
curl https://<YOUR_DOMAIN>/api/location/getAll
curl https://<YOUR_DOMAIN>/api/employee/getAll

# Test authentication
curl -X POST https://<YOUR_DOMAIN>/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@certiflo.com", "password": "..."}'

# Test authenticated write (use token from login response)
curl -X POST https://<YOUR_DOMAIN>/api/resource/save \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"key": "test", "value": "test", "page": "test", "language": "en"}'
```

### Step 19: Update Frontend Websites

In all 3 frontend codebases:

1. Find the old Heroku API URL (e.g., `https://certiflo-be.herokuapp.com`)
2. Replace with the new Oracle Cloud URL (e.g., `https://<your-domain>`)
3. Deploy the updated frontends
4. Verify each site loads and displays data correctly

### Step 20: Parallel Running Period (1-2 weeks)

Keep Heroku running as a rollback target. If anything goes wrong with Oracle Cloud:
- Revert the frontend API URL back to Heroku
- Investigate and fix the issue on Oracle Cloud

### Step 21: Decommission Heroku

After 1-2 weeks of stable operation:

1. Remove the Heroku Postgres add-on
2. Delete the Heroku app: `heroku apps:destroy certiflo-be --confirm certiflo-be`
3. Cancel any paid Heroku plans

### Phase 4 Checklist

- [ ] All 3 frontend websites display data correctly from new backend
- [ ] Admin can log in and perform CRUD operations
- [ ] No errors in `journalctl -u certiflo` logs
- [ ] Heroku decommissioned after confidence period

---

## Ongoing: Deploying Code Changes

After the migration is complete, deploy updates with:

```bash
ssh ubuntu@<VM_PUBLIC_IP>
sudo su - certiflo
cd /opt/certiflo/app
git pull origin prod
source venv/bin/activate
pip install -r requirements.txt
export FLASK_APP=manage:app
flask db upgrade  # only if there are new migrations
exit  # back to ubuntu user
sudo systemctl restart certiflo
```

## Troubleshooting

**App won't start:**
```bash
sudo journalctl -u certiflo -n 50 --no-pager
```

**502 Bad Gateway from nginx:**
- Check if gunicorn is running: `sudo systemctl status certiflo`
- Check if it's listening: `curl http://127.0.0.1:8000/`

**Database connection errors after idle:**
- The Neon free tier suspends after 5 min idle. `pool_pre_ping=True` in config.py handles this automatically.
- First request after idle takes ~1-2s for Neon to wake up. This is normal.

**SSL certificate renewal:**
- Certbot sets up auto-renewal. Verify with: `sudo certbot renew --dry-run`
