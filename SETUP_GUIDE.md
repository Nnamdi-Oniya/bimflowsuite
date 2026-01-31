# BIMFlow Suite - Setup Guide

Complete guide for setting up BIMFlow Suite for development or production deployment.

## Table of Contents
1. [Quick Start (Automated)](#quick-start-automated)
2. [Manual Setup](#manual-setup)
3. [Verify Installation](#verify-installation)
4. [Troubleshooting](#troubleshooting)
5. [Database Management](#database-management)

---

## Quick Start (Automated)

The fastest way to get BIMFlow Suite running on your machine.

### Prerequisites
- **macOS/Linux**: Bash shell
- **All OS**: PostgreSQL, Redis, Python 3.11+, Node.js 18+

### Run Setup Script

```bash
# Option 1: Direct from GitHub
curl -O https://raw.githubusercontent.com/Nnamdi-Oniya/bimflowsuite/main/setup.sh
chmod +x setup.sh
./setup.sh

# Option 2: Clone and run
git clone https://github.com/Nnamdi-Oniya/bimflowsuite.git
cd bimflowsuite/bimflowsuite
bash setup.sh
```

The script will:
- ✅ Validate all prerequisites
- ✅ Clone repository (if needed)
- ✅ Create PostgreSQL database
- ✅ Set up Python virtual environment
- ✅ Install all dependencies
- ✅ Configure environment variables
- ✅ Run migrations
- ✅ Install frontend dependencies
- ✅ Display startup commands

### After Setup Completes

The script will display 4 commands to start services. Run each in a separate terminal:

```bash
# Terminal 1: Django Backend
cd bimflowsuite
source .venv/bin/activate
python manage.py runserver

# Terminal 2: React Frontend
cd bimflowsuite-ui
npm run dev

# Terminal 3: Celery Worker
cd bimflowsuite
source .venv/bin/activate
celery -A bimflowsuite worker -l info

# Terminal 4: Redis (if not already running)
redis-server
```

---

## Manual Setup

Follow these steps if you prefer to set up manually or the script doesn't work.

### Step 1: Prerequisites

Install required software:

**macOS:**
```bash
brew install python@3.11 node postgresql redis
brew services start postgresql
brew services start redis
```

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install python3.11 python3.11-venv nodejs postgresql postgresql-contrib redis-server
sudo systemctl start postgresql
sudo systemctl start redis-server
```

**Verify installations:**
```bash
python3.11 --version
node --version
npm --version
psql --version
redis-cli ping
```

### Step 2: Clone Repository

```bash
git clone https://github.com/Nnamdi-Oniya/bimflowsuite.git
cd bimflowsuite/bimflowsuite
```

### Step 3: Create PostgreSQL Database

```bash
# Connect to PostgreSQL
psql -U postgres

# Execute in psql terminal:
CREATE USER bimflow_user WITH PASSWORD 'bimflow_password_secure';
ALTER USER bimflow_user CREATEDB;
CREATE DATABASE bimflowsuite_db OWNER bimflow_user;
GRANT ALL PRIVILEGES ON DATABASE bimflowsuite_db TO bimflow_user;
\q
```

### Step 4: Setup Python Environment

```bash
# Create virtual environment
python3.11 -m venv .venv

# Activate it
source .venv/bin/activate  # macOS/Linux
# or
.venv\Scripts\activate  # Windows
```

### Step 5: Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements/local.txt
```

### Step 6: Configure Environment

Copy `.env.example` to `.env` and update with your configuration:

```bash
cp .env.example .env
```

Edit the `.env` file with your settings:

```bash
# Database
DATABASE_URL=postgresql://bimflow_user:bimflow_password_secure@localhost:5432/bimflowsuite_db

# Django
DJANGO_SETTINGS_MODULE=config.settings.local
SECRET_KEY=your-secret-key-change-this
DEBUG=True

# Celery & Redis
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

# File Storage
USE_S3=False

# CORS (for local frontend dev)
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173,http://localhost:8000

# Email (console output in development)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

**💡 Tip:** See `.env.example` for complete list of available configuration options including AWS S3, email, logging, and security settings.

### Step 7: Run Migrations

```bash
python manage.py migrate
```

### Step 8: Create Admin User (Optional)

```bash
python manage.py createsuperuser
# Follow prompts
```

### Step 9: Install Frontend

```bash
cd ../bimflowsuite-ui
npm install
```

### Step 10: Start Services

Open 4 terminal windows and run:

**Terminal 1 - Backend:**
```bash
cd bimflowsuite
source .venv/bin/activate
python manage.py runserver
```

**Terminal 2 - Frontend:**
```bash
cd bimflowsuite-ui
npm run dev
```

**Terminal 3 - Celery Worker:**
```bash
cd bimflowsuite
source .venv/bin/activate
celery -A bimflowsuite worker -l info
```

**Terminal 4 - Redis:**
```bash
redis-server
```

---

## Verify Installation

### Check Database Connection

```bash
cd bimflowsuite
python check_database.py
```

Expected output:
```
🔍 PostgreSQL Database Inspection
===
✅ Connection successful!
📦 Database size: ...
📋 Found X tables:
   ✓ auth_user
   ✓ users_organization
   ✓ users_requestsubmission
   ✓ parametric_generator_project
   ✓ parametric_generator_generatedifc
   ✓ compliance_engine_compliancecheck
   ✓ compliance_engine_rulepack
   ✓ analytics_analyticsrun
All checks passed! Database is ready to use.
```

### Test API Endpoints

```bash
# Get JWT token
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"password"}'

# List projects (using token)
curl -H "Authorization: Bearer <your_token>" \
  http://localhost:8000/api/v1/bim-projects/projects/

# View API documentation
# Swagger: http://localhost:8000/swagger/
# GraphQL: http://localhost:8000/graphql/
```

### Test Frontend

Open browser:
- Frontend: `http://localhost:5173`
- Backend API: `http://localhost:8000/api/v1/`
- Admin Panel: `http://localhost:8000/admin/`

---

## Troubleshooting

### PostgreSQL Connection Error

**Problem:** `psycopg2.OperationalError: FATAL: Ident authentication failed`

**Solution:**
```bash
# Update PostgreSQL password
psql -U postgres
ALTER USER bimflow_user WITH PASSWORD 'new_password';
\q

# Update .env file with new password
```

### Redis Connection Error

**Problem:** `ConnectionError: Error 111 connecting to localhost:6379`

**Solution:**
```bash
# Check if Redis is running
redis-cli ping

# If not running, start it
redis-server

# macOS Homebrew
brew services start redis
```

### Migration Errors

**Problem:** `django.db.utils.ProgrammingError: relation "..." does not exist`

**Solution:**
```bash
# Reset migrations (WARNING: Deletes all data)
python manage.py migrate users zero
python manage.py migrate parametric_generator zero
python manage.py migrate compliance_engine zero
python manage.py migrate analytics zero

# Re-run all migrations
python manage.py migrate
```

### Port Already in Use

**Problem:** `Address already in use: ('127.0.0.1', 8000)`

**Solution:**
```bash
# Find process using port 8000
lsof -i :8000

# Kill process
kill -9 <PID>

# Or use different port
python manage.py runserver 8001
```

### Module Not Found Errors

**Problem:** `ModuleNotFoundError: No module named 'ifcopenshell'`

**Solution:**
```bash
# Reinstall dependencies
pip install --force-reinstall -r requirements/local.txt

# Or install specific package
pip install ifcopenshell
```

---

## Database Management

### Backup Database

**PostgreSQL:**
```bash
pg_dump -U bimflow_user -h localhost bimflowsuite_db > backup.sql
```

### Restore Database

```bash
psql -U bimflow_user -h localhost bimflowsuite_db < backup.sql
```

### Reset Database (WARNING: Deletes all data)

```bash
# Drop and recreate database
dropdb -U postgres bimflowsuite_db
createdb -U postgres -O bimflow_user bimflowsuite_db

# Run migrations
python manage.py migrate
```

### Create Database Snapshots

```bash
# For development snapshot
pg_dump -U bimflow_user -h localhost -F c bimflowsuite_db > snapshot_20260131.dump

# Restore from snapshot
pg_restore -U bimflow_user -h localhost -d bimflowsuite_db snapshot_20260131.dump
```

---

## Environment Variables Reference

### Required Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://user:pass@host:5432/db` |
| `SECRET_KEY` | Django secret key | `your-secret-key` |
| `DJANGO_SETTINGS_MODULE` | Settings file to use | `config.settings.local` |

### Optional Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DEBUG` | Enable debug mode | `False` |
| `ALLOWED_HOSTS` | Allowed hostnames | `localhost,127.0.0.1` |
| `CELERY_BROKER_URL` | Celery broker URL | `redis://localhost:6379/0` |
| `USE_S3` | Use AWS S3 for storage | `False` |
| `CORS_ALLOWED_ORIGINS` | CORS allowed origins | `http://localhost:3000` |

---

## Getting Help

- **Documentation**: See [README.md](README.md)
- **API Docs**: Visit `http://localhost:8000/swagger/`
- **Issues**: GitHub Issues on repository
- **Contributing**: See [CONTRIBUTING.md](CONTRIBUTING.md)

---

**Last Updated:** January 31, 2026
