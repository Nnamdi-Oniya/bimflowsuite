# BIMFlow Suite - Cloud-Native BIM Automation Platform

## Overview

**BIMFlow Suite** is a comprehensive, open-source BIM automation platform that streamlines Building Information Modeling processes through intelligent IFC generation, compliance checking, and detailed analysis. It combines a powerful python Django REST API backend with a modern React + Vite frontend to provide architects, engineers, and contractors with tools to:

- **Generate IFC files** programmatically from detailed project specifications
- **Upload and analyze** existing IFC files for comprehensive metrics extraction
- **Run compliance checks** against YAML-based rule packs with advanced clash detection
- **Manage projects** across multiple organizations with full multi-tenant support
- **Track project workflows** from concept through as-built documentation

## Key Features

| Feature | Description |
|---------|-------------|
| **Parametric IFC Generation** | Create building, bridge, and road IFC models from a comprehensive 30+ field project form |
| **IFC Analytics & Upload** | Import existing IFC files and extract detailed geometry metrics, component breakdowns, and project statistics |
| **Compliance Engine** | Evaluate IFC models against YAML rulepacks with rule-based condition checking and detailed reporting |
| **Advanced Clash Detection** | Detect hard (overlap) and soft (clearance) clashes between building elements with configurable tolerances |
| **Multi-Tenant Architecture** | Support for organizations with role-based access control and project segregation |
| **JWT Authentication** | Secure API access with token-based authentication and refresh mechanisms |
| **AWS S3 Integration** | Cloud storage support for IFC files with fallback to local file system storage |
| **Async Background Jobs** | Celery worker integration for long-running IFC generation and analysis tasks |
| **Comprehensive API Documentation** | Swagger/OpenAPI integration with interactive API explorer |

## Technology Stack

### Backend
- **Framework**: Django 5.2 with Django REST Framework
- **Database**: PostgreSQL (local development & production)
- **Task Queue**: Celery + Redis for async processing
- **Real-time**: Django Channels + Redis for WebSocket support
- **IFC Processing**: ifcopenshell for parsing and generating IFC files
- **API Documentation**: drf-yasg (Swagger) + GraphQL support
- **Authentication**: djangorestframework-simplejwt (JWT)

### Frontend
- **Framework**: React 18.3 with TypeScript + Vite
- **State Management**: React Hooks
- **3D Visualization**: Three.js + web-ifc-viewer
- **Testing**: Vitest + React Testing Library
- **UI Components**: Tailwind CSS + Lucide icons
- **Build Tool**: Vite with tree-shaking and code splitting

## Architecture at a Glance

```
┌─────────────────────────────────────────────┐
│  FRONTEND (React + Vite + TypeScript)      │
│  - Upload IFC / Generate New               │
│  - Compliance Checks / Analytics           │
│  - Account Management & Dashboard          │
└─────────────────┬───────────────────────────┘
                  │ HTTP (JWT)
                  ▼
┌─────────────────────────────────────────────┐
│  DJANGO REST API                            │
│  ├─ /auth/ (Users App)                      │
│  ├─ /generate/ (Parametric Generator)       │
│  ├─ /compliance/ (Compliance Engine)        │
│  └─ /analytics/ (Upload & Analysis)         │
└─────────────────┬───────────────────────────┘
                  │
         ┌────────┼────────┐
         ▼        ▼        ▼
    ┌────────┬────────┬────────┐
    │ Models │ Tasks  │Engines │
    └────────┴────────┴────────┘
                  │
                  ▼
    ┌──────────────────────────┐
    │ PostgreSQL + Redis + S3  │
    └──────────────────────────┘
```

### Application Structure

- **`apps/users/`** — User authentication, registration, organizations, demo requests, multi-tenant management
- **`apps/parametric_generator/`** — Project model (30+ metadata fields), IFC generation, Celery tasks for async processing
- **`apps/compliance_engine/`** — Rule engine (YAML evaluation), advanced clash detection, compliance check tracking
- **`apps/analytics/`** — IFC upload handling, geometry analysis, project metrics extraction
- **`config/settings/`** — Environment-specific configurations (local, development, production)
- **`rulepacks/`** — YAML rule definitions for building, bridge, road, tunnel, and generic assets

## Installation & Setup

### Quick Start (Automated Setup)

We provide an automated setup script that handles everything for you:

```bash
# Download and run the setup script
curl -O https://raw.githubusercontent.com/Nnamdi-Oniya/bimflowsuite/main/setup.sh
chmod +x setup.sh
./setup.sh
```

The script will:
1. ✅ Clone the repository
2. ✅ Check all prerequisites (Python, Node.js, PostgreSQL)
3. ✅ Create PostgreSQL database and user
4. ✅ Set up Python virtual environment
5. ✅ Install backend dependencies
6. ✅ Configure environment variables (using `.env.example` as template)
7. ✅ Run Django migrations
8. ✅ Install frontend dependencies
9. ✅ Display startup instructions

**📝 Note:** The script will prompt you for a database password. If you press Enter, it will use a default password.

**📝 Environment Variables:** A `.env` file is automatically created from `.env.example` template with proper database credentials.

---

### Manual Setup (If Script Fails or Doesn't Work)

If you prefer to set up manually or the script doesn't work in your environment:

### System Requirements

- **Python**: 3.10 or higher
- **Node.js**: 18+ with npm
- **Database**: PostgreSQL 12+
- **Cache/Queue**: Redis 6+
- **Storage**: Local disk or AWS S3 (optional)
- **OS**: macOS, Linux, or Windows (WSL2 recommended)

#### 1. Clone Repository & Create Virtual Environment

```bash
# Clone the repo
git clone https://github.com/Nnamdi-Oniya/bimflowsuite.git
cd bimflowsuite/bimflowsuite

# Create Python virtual environment
python3.10 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

#### 2. Create PostgreSQL Database

```bash
# Connect to PostgreSQL
psql -U postgres

# Create database and user (in psql terminal)
CREATE USER bimflow_user WITH PASSWORD 'secure_password';
ALTER USER bimflow_user CREATEDB;
CREATE DATABASE bimflowsuite_db OWNER bimflow_user;
GRANT ALL PRIVILEGES ON DATABASE bimflowsuite_db TO bimflow_user;
\q
```

#### 3. Install Python Dependencies

```bash
pip install -r requirements/local.txt
```

#### 4. Configure Environment Variables

Copy `.env.example` to `.env` and update with your values:

```bash
cp .env.example .env
```

Edit the `.env` file with your configuration:

```bash
# Database (Use your credentials)
DATABASE_URL=postgresql://bimflow_user:secure_password@localhost:5432/bimflowsuite_db

# Django
DJANGO_SECRET_KEY=your-secret-key-change-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Celery & Redis
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

# File Storage (Local)
USE_S3=False

# Email (Console backend for local dev)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173,http://localhost:8000
```

**📝 Tip:** See `.env.example` for all available configuration options including S3, email, and security settings.

#### 5. Run Migrations

```bash
DJANGO_SETTINGS_MODULE=config.settings.local python manage.py migrate
```

#### 6. Create Superuser (Optional)

```bash
python manage.py createsuperuser
# Follow prompts to create admin account
```

#### 7. Install Frontend Dependencies

```bash
cd ../bimflowsuite-ui
npm install
```

---

### Starting the Application

You need to run **4 services** in separate terminal windows:

#### Terminal 1: Django Backend

```bash
cd bimflowsuite
source .venv/bin/activate
python manage.py runserver
# Runs on http://localhost:8000
```

#### Terminal 2: React Frontend

```bash
cd bimflowsuite-ui
npm run dev
# Runs on http://localhost:5173
```

#### Terminal 3: Celery Worker (for async tasks)

```bash
cd bimflowsuite
source .venv/bin/activate
celery -A bimflowsuite worker -l info
```

#### Terminal 4: Redis Server (if not already running)

```bash
redis-server
# Runs on localhost:6379
```

---

### Verify Installation

Check that everything is set up correctly:

```bash
# Check database connection and models
cd bimflowsuite
python check_database.py
```

You should see:
```
🔍 PostgreSQL Database Inspection
✅ Connection successful!
📋 Found X tables
✅ Model data inspection completed successfully!
```

---

---

#### 4. Setup PostgreSQL Database (if not already installed)

```bash
# Install PostgreSQL
brew install postgresql  # macOS
# or
sudo apt-get install postgresql-12 postgresql-contrib-12  # Linux

# Start PostgreSQL service
brew services start postgresql  # macOS
# or
sudo systemctl start postgresql  # Linux
```

#### 5. Setup Redis (for Celery & Channels)

```bash
# Install Redis
brew install redis  # macOS
# or
sudo apt-get install redis-server  # Linux

# Start Redis service
brew services start redis  # macOS
# or
redis-server  # Linux
```

---

For specific queues (geometry tasks):

```bash
celery -A bimflowsuite worker -Q geometry -c 1 -l info
```

## Running Tests

### Backend Unit Tests

```bash
cd bimflowsuite
DJANGO_SETTINGS_MODULE=config.settings.local pytest apps/ -v
# or
DJANGO_SETTINGS_MODULE=config.settings.local python manage.py test
```

### Frontend Tests

See [bimflowsuite-ui/README.md](../bimflowsuite-ui/README.md#running-tests) for frontend testing instructions.

## Build for Production

### Backend

```bash
cd bimflowsuite
# Collect static files
DJANGO_SETTINGS_MODULE=config.settings.production python manage.py collectstatic --noinput

# Run with production server (e.g., Gunicorn)
gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 4
```

### Frontend

See [bimflowsuite-ui/README.md](../bimflowsuite-ui/README.md#build-for-production) for frontend build instructions.

## API Endpoints Overview

## API Endpoints Overview

### Authentication
- `POST /api/v1/auth/login/` — Get JWT access & refresh tokens
- `POST /api/v1/auth/register/` — Create new user account
- `POST /api/v1/auth/request-submission/` — Submit demo request
- `POST /api/token/refresh/` — Refresh expired access token

### Projects & IFC Generation
- `GET /api/v1/generate/projects/` — List user projects (paginated, filterable)
- `POST /api/v1/generate/projects/` — Create new project
- `GET /api/v1/generate/projects/{id}/` — Get project details (all 30+ fields)
- `PUT /api/v1/generate/projects/{id}/` — Update project
- `DELETE /api/v1/generate/projects/{id}/` — Delete project
- `POST /api/v1/generate/ifcs/create_for_project/` — Generate IFC from project
- `GET /api/v1/generate/ifcs/` — List generated IFCs
- `GET /api/v1/generate/ifcs/{id}/` — Get IFC details & download link

### Upload & Analytics
- `POST /api/v1/analytics/upload_ifc/` — Upload existing IFC file
- `GET /api/v1/analytics/uploaded_ifcs/` — List uploaded files
- `GET /api/v1/analytics/uploaded_ifcs/{id}/` — Get analysis results
- `POST /api/v1/analytics/project-summary/` — Get project metrics

### Compliance Checks
- `POST /api/v1/compliance/checks/` — Create compliance check
- `GET /api/v1/compliance/checks/` — List compliance results
- `GET /api/v1/compliance/checks/{id}/` — Get detailed compliance report
- `GET /api/v1/compliance/rulepacks/` — List available rule packs

### Organizations & Users
- `GET /api/v1/organizations/` — List organizations
- `POST /api/v1/organizations/` — Create organization
- `GET /api/v1/organization-members/` — List org members
- `POST /api/v1/organization-members/` — Invite member

### API Documentation
- `GET /swagger/` — Interactive Swagger UI
- `GET /redoc/` — ReDoc documentation
- `GET /graphql/` — GraphQL endpoint (alternative to REST)

## API Usage Examples

### 1. User Authentication

```bash
# Login
curl -X POST http://localhost:8000/api/v1/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"user@example.com","password":"password123"}'

# Response
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}

# Use access token in Authorization header
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### 2. Create a Project

```bash
curl -X POST http://localhost:8000/api/v1/generate/projects/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Downtown Office Tower",
    "description": "Modern 20-story office complex",
    "project_number": "DOC-2024-001",
    "status": "schematic",
    "building_type": "office",
    "client_name": "Acme Corp",
    "country": "USA",
    "city_address": "San Francisco, CA",
    "latitude": 37.7749,
    "longitude": -122.4194,
    "length_unit": "m",
    "area_unit": "m2",
    "ifc_schema_version": "ifc4"
  }'
```

### 3. Generate IFC File

```bash
curl -X POST http://localhost:8000/api/v1/generate/ifcs/create_for_project/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "project_id": 1,
    "asset_type": "building",
    "specifications": {
      "floor_count": 20,
      "floor_height": 3.5,
      "building_height": 70,
      "total_area": 50000
    }
  }'

# Response (IFC generation queued in Celery)
{
  "id": 42,
  "project": 1,
  "asset_type": "building",
  "status": "generating",
  "created_at": "2025-01-31T10:30:00Z"
}
```

### 4. Upload & Analyze IFC

```bash
curl -X POST http://localhost:8000/api/v1/analytics/upload_ifc/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -F "file=@path/to/model.ifc"

# Response
{
  "id": 15,
  "filename": "model.ifc",
  "file_size": 2048576,
  "upload_date": "2025-01-31T10:35:00Z",
  "analysis_status": "processing"
}

# Later, get analysis results
curl -X GET http://localhost:8000/api/v1/analytics/uploaded_ifcs/15/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"

# Response (when ready)
{
  "id": 15,
  "analysis_results": {
    "total_elements": 1234,
    "walls": 456,
    "doors": 78,
    "windows": 120,
    "slabs": 25,
    "total_volume": 125000,
    "total_surface_area": 45000
  }
}
```

### 5. Run Compliance Check

```bash
curl -X POST http://localhost:8000/api/v1/compliance/checks/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "generated_ifc": 42,
    "rule_pack": "default_building",
    "include_clash": true
  }'

# Get compliance results
curl -X GET http://localhost:8000/api/v1/compliance/checks/100/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"

# Response
{
  "id": 100,
  "generated_ifc": 42,
  "rule_pack": "default_building",
  "status": "passed",
  "results": [
    {
      "rule": "wall_height_check",
      "category": "building_dimensions",
      "severity": "high",
      "passed": true,
      "condition": "avg_wall_height < 50"
    },
    {
      "rule": "door_clearance",
      "category": "accessibility",
      "severity": "warning",
      "passed": false,
      "details": [{"message": "Door frame 800mm < minimum 850mm"}]
    }
  ],
  "clash_results": {
    "summary": {
      "total_clashes": 2,
      "hard_clashes": 1,
      "soft_clashes": 1
    },
    "clashes": [
      {
        "id_a": "0x1234",
        "name_a": "Wall_EXT_01",
        "id_b": "0x5678",
        "name_b": "Duct_HVAC_02",
        "type": "hard",
        "severity": "high",
        "description": "Overlap detected between exterior wall and HVAC duct"
      }
    ]
  },
  "checked_at": "2025-01-31T10:45:00Z"
}
```

## Understanding Core Concepts

### Projects (30+ Metadata Fields)

Every project stores comprehensive BIM information organized into sections:

**Basic Information**
- Name, Description, Project Number, Status (concept/schematic/detailed/as-built)

**Client & Location**
- Client name, Country, City/Address, Coordinates (latitude/longitude), Elevation, True North

**Building Information**
- Building Type (residential/office/hospital/etc.), Climate Zone, Design Temperature

**Units & Precision**
- Length Unit (mm/m), Area Unit (m2/mm2), Volume Unit (m3/mm3), Angle Unit (degree/radian)

**IFC Configuration**
- IFC Schema Version (IFC2x3, IFC4, IFC4x3)

**Materials** (JSON flexible structure)
- Walls, Slabs, Columns with properties: thickness, thermal conductivity, fire rating

**Authoring & Approval**
- Author name, Company, Approval status, Revision ID, Change notes

### IFC Generation Workflow

1. **User creates Project** with specifications
2. **Frontend calls** `POST /api/v1/generate/ifcs/create_for_project/`
3. **Backend queues** Celery task
4. **Celery worker** loads appropriate generator (building.py, road.py, etc.)
5. **Generator** uses ifcopenshell to construct IFC entities
6. **IFC file saved** to S3 or local storage
7. **GeneratedIFC record** updated with status="completed"

### Compliance Check Workflow

1. **User initiates** compliance check on IFC (generated or uploaded)
2. **RuleEngine** loads YAML rulepack (e.g., default_building.yaml)
3. **Conditions evaluated** against IFC geometry
4. **AdvancedClashDetector** runs hard/soft clash detection
5. **Results stored** in ComplianceCheck with pass/fail per rule
6. **Frontend displays** violations with remediation guidance

### YAML Rulepack Format

```yaml
rules:
  - name: wall_height_limit
    category: dimensional_requirements
    severity: high
    condition: "max_wall_height < 50"
    description: "Wall height must not exceed 50 meters"
    
  - name: door_accessibility
    category: accessibility
    severity: warning
    condition: "door_width >= 0.85"
    description: "Door openings must be minimum 850mm wide"
    
  - name: column_spacing
    category: structural
    severity: info
    condition: "avg_column_spacing > 5"
    description: "Columns should be spaced more than 5m apart"
```

## Environment Configuration Details

### Settings Hierarchy

1. **`config/settings/common.py`** — Base configuration (shared)
2. **`config/settings/local.py`** — Development (PostgreSQL default)
3. **`config/settings/development.py`** — Development with extended logging
4. **`config/settings/production.py`** — Production with security hardening

### Key Environment Variables

| Variable | Purpose | Example |
|----------|---------|---------|
| `DJANGO_SETTINGS_MODULE` | Choose settings file | `config.settings.local` |
| `DATABASE_URL` | PostgreSQL connection | `postgresql://user:pass@localhost/bimflow_db` |
| `CELERY_BROKER_URL` | Redis connection | `redis://localhost:6379/0` |
| `USE_S3` | Enable AWS S3 storage | `True` or `False` |
| `AWS_STORAGE_BUCKET_NAME` | S3 bucket name | `bimflow-production` |
| `BIMFLOW_RULEPACKS_DIR` | Path to rule packs | `/app/rulepacks` |
| `JWT_EXPIRATION_HOURS` | Token expiration | `24` |
| `DEBUG` | Django debug mode | `False` (production) |
| `SECRET_KEY` | Django secret key | (generate with Django) |

### File Storage Options

**Local Development (USE_S3=False)**
```bash
USE_S3=False
# IFC files stored at: /media/ifc_files/YYYY/MM/DD/filename.ifc
# Served by Django's static file handler
```

**Production (USE_S3=True)**
```bash
USE_S3=True
AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
AWS_STORAGE_BUCKET_NAME=bimflow-production
AWS_S3_REGION_NAME=us-east-1
# IFC files stored at: s3://bimflow-production/media/ifc_files/YYYY/MM/DD/filename.ifc
```

## Project Structure

```
bimflowsuite/
├── config/                          # Django settings module
│   ├── settings/
│   │   ├── common.py               # Shared settings
│   │   ├── local.py                # Development
│   │   ├── development.py          # Extended dev
│   │   └── production.py           # Production
│   ├── urls.py                     # URL routing
│   ├── asgi.py                     # ASGI/Channels config
│   └── wsgi.py                     # WSGI config
│
├── apps/
│   ├── users/                      # User management & auth
│   │   ├── models.py               # User, Organization, RequestSubmission
│   │   ├── views.py                # Login, Register, Account viewsets
│   │   └── urls.py
│   │
│   ├── parametric_generator/       # IFC generation
│   │   ├── models.py               # Project, GeneratedIFC
│   │   ├── generators/             # building.py, road.py, bridge.py
│   │   ├── tasks.py                # Celery tasks
│   │   ├── views.py                # Project & IFC viewsets
│   │   └── urls.py
│   │
│   ├── compliance_engine/          # Rule evaluation & clash detection
│   │   ├── models.py               # ComplianceCheck, RulePack
│   │   ├── rule_engine.py          # YAML rule evaluation
│   │   ├── clash_detector.py       # Advanced clash detection
│   │   ├── views.py                # Compliance check viewsets
│   │   ├── rulepacks/              # YAML rule files
│   │   └── urls.py
│   │
│   └── analytics/                  # IFC upload & analysis
│       ├── models.py               # UploadedIFC, Analysis
│       ├── views.py                # Upload & analysis viewsets
│       └── urls.py
│
├── rulepacks/                      # Global rule packs
│   ├── default_building.yaml
│   ├── default_bridge.yaml
│   ├── default_road.yaml
│   └── default_*.yaml
│
├── requirements/
│   ├── local.txt                   # Development dependencies
│   └── prod.txt                    # Production dependencies
│
├── staticfiles/                    # Collected static assets
├── media/                          # Local file uploads
├── manage.py                       # Django management
└── README.md                       # This file
```

## Important Environment Variables

**Database Configuration**
- `DATABASE_URL` — Full PostgreSQL connection string
- `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT` — Individual DB parameters

**Django Core**
- `DJANGO_SECRET_KEY` — Secret key for CSRF protection (generate new for production)
- `DEBUG` — Enable debug mode (False in production)
- `ALLOWED_HOSTS` — Comma-separated list of allowed domain names
- `BASE_URL` — Base URL for email links and external references

**JWT Authentication**
- `JWT_ALGORITHM` — Signing algorithm (HS256)
- `JWT_EXPIRATION_HOURS` — Access token lifetime (default: 24)
- `JWT_REFRESH_EXPIRATION_DAYS` — Refresh token lifetime (default: 7)

**Celery & Redis**
- `CELERY_BROKER_URL` — Redis broker address
- `CELERY_RESULT_BACKEND` — Redis result backend
- `CELERY_TASK_TIME_LIMIT` — Max task execution time (seconds)
- `CELERY_TASK_SOFT_TIME_LIMIT` — Graceful task timeout

**File Storage (S3)**
- `USE_S3` — Enable S3 storage (True/False)
- `AWS_ACCESS_KEY_ID` — AWS access key
- `AWS_SECRET_ACCESS_KEY` — AWS secret key
- `AWS_STORAGE_BUCKET_NAME` — S3 bucket name
- `AWS_S3_REGION_NAME` — AWS region (default: us-east-1)

**Rule Packs**
- `BIMFLOW_RULEPACKS_DIR` — Path to rule pack YAML files (default: ./rulepacks)

## Developer Best Practices

### Code Organization

**Generators**
- Add new parametric generators to `apps/parametric_generator/generators/`
- Expose a `generate_<asset_type>(spec)` function that accepts JSON spec and returns IFC string
- Use ifcopenshell consistently for all geometry creation
- Example: `building.py`, `road.py`, `bridge.py`

**Rule Packs**
- Name YAML files as `default_<asset_type>.yaml` (e.g., `default_building.yaml`)
- Load packs via `RulePack.get_default_pack(asset_type_code)` from `BIMFLOW_RULEPACKS_DIR`
- Validate YAML syntax before committing (use `yaml.safe_load()` in Python)

**Celery Tasks**
- Delegate CPU-intensive work (IFC generation, clash detection, analysis) to Celery
- Use task time limits and soft time limits for long-running operations
- Implement proper error handling and logging with full stack traces
- Consider task partitioning for very large models (spatial tiling)

**Error Handling**
- Catch `ifcopenshell` parsing errors as `ValueError`
- Log full exceptions with `logger.error()` for debugging
- Return meaningful HTTP error responses with context
- Wrap database transactions around multi-step operations

### Performance Optimization

**Database**
- Add database indexes on frequently filtered fields (status, project_id, created_at)
- Use select_related() for foreign keys, prefetch_related() for reverse relations
- Limit API responses with pagination (default 20 items)
- Consider caching project summaries (TTL: 1 hour)

**IFC Processing**
- Stream large IFC files to disk/S3 before processing in workers
- Use ifcopenshell geometry settings wisely (INCLUDE_CURVES, USE_PYTHON_OPENCASCADE)
- Monitor memory usage during shape creation; use temporal working directories
- Split analysis into spatial partitions for massive models (>100MB)

**API Responses**
- Implement pagination for list endpoints
- Use JSON serialization efficiently (exclude unnecessary fields)
- Compress responses with gzip
- Implement HTTP caching headers (ETag, Cache-Control)

### Security Practices

**Authentication & Authorization**
- Always verify JWT token signature and expiration
- Implement organization-level scoping in querysets
- Use permission_classes on all ViewSets
- Check object-level permissions before allowing CRUD operations

**Secrets Management**
- Never commit `.env` files or `SECRET_KEY` to version control
- Use environment variables for all secrets
- Rotate AWS access keys regularly
- Use AWS IAM roles in production instead of hardcoded keys

**Data Protection**
- Encrypt sensitive fields (use django-encrypted-model-fields if needed)
- Implement CORS policy to allow only trusted origins
- Enable HTTPS in production (use secure cookies and HSTS)
- Sanitize user input in all API endpoints

### Testing Best Practices

**Unit Tests**
- Test each generator function with varied specifications
- Mock external dependencies (S3, Redis, ifcopenshell)
- Test rule evaluation with multiple condition types
- Test permission checks for multi-tenant scenarios

**Integration Tests**
- Test full workflows (create project → generate IFC → compliance check)
- Test Celery task processing and error handling
- Test S3 upload/download flows
- Test JWT authentication and token refresh

**Test Structure**
```bash
apps/
├── parametric_generator/
│   ├── tests/
│   │   ├── test_models.py
│   │   ├── test_generators.py
│   │   ├── test_views.py
│   │   └── test_tasks.py
```

## Troubleshooting Guide

### Database Connection Issues

**Problem**: `psycopg2.OperationalError: could not connect to server`

**Solutions**:
1. Verify PostgreSQL is running: `pg_isready -h localhost -p 5432`
2. Check DATABASE_URL in `.env` file
3. Verify credentials: `psql -U bimflow_user -d bimflow_db`
4. Check PostgreSQL logs: `/var/log/postgresql/postgresql.log`

### Redis Connection Issues

**Problem**: `redis.ConnectionError: Error -2 connecting to localhost:6379`

**Solutions**:
1. Verify Redis is running: `redis-cli ping` (should return PONG)
2. Check Redis configuration: `redis-cli CONFIG GET port`
3. Restart Redis: `brew services restart redis`
4. Check for port conflicts: `lsof -i :6379`

### IFC Generation Failures

**Problem**: Celery task fails during IFC generation

**Solutions**:
1. Check Celery worker logs for full error traceback
2. Verify ifcopenshell is correctly installed: `python -c "import ifcopenshell; print(ifcopenshell.__version__)"`
3. Check available disk space in working directory
4. Try with smaller specification (fewer floors, less complexity)
5. Monitor memory: `top` or `htop` while task runs

### Compliance Check Timeouts

**Problem**: Compliance check hangs or times out

**Solutions**:
1. Increase Celery task timeout in settings
2. Check if IFC file is corrupted: `ifcopenshell.open(file_path)` in Python REPL
3. Split large models into spatial partitions
4. Monitor CPU/memory during processing
5. Consider using a dedicated Celery worker for geometry tasks: `celery -A bimflowsuite worker -Q geometry -c 1`

### S3 Upload Failures

**Problem**: `NoCredentialsError` or `InvalidAccessKeyId` when uploading to S3

**Solutions**:
1. Verify AWS credentials in `.env`: `echo $AWS_ACCESS_KEY_ID`
2. Check AWS IAM permissions for S3 bucket
3. Verify S3 bucket exists and is accessible
4. Confirm region matches bucket location
5. Use AWS CLI to test: `aws s3 ls s3://bucket-name/`

### Frontend Issues

For frontend-specific troubleshooting, see [bimflowsuite-ui/README.md](../bimflowsuite-ui/README.md#troubleshooting)

## Contributing

### Workflow

1. Create a feature branch: `git checkout -b feature/my-feature`
2. Make changes and commit: `git commit -m "Add new feature"`
3. Run tests: `npm run test` and `pytest`
4. Push changes: `git push origin feature/my-feature`
5. Create Pull Request for review

### Code Quality

- Follow PEP 8 for Python (use `black` for formatting)
- Follow ESLint rules for TypeScript/React (use `eslint`)
- Add docstrings to Python functions and classes
- Add JSDoc comments to TypeScript functions
- Keep functions small and focused (single responsibility)

### Commit Messages

```
type(scope): subject line (50 chars max)

Detailed explanation of changes (72 chars per line)
- Bullet point 1
- Bullet point 2

Fixes #issue-number
```

Examples:
- `feat(compliance): add soft clash detection`
- `fix(generator): handle duplicate wall names`
- `docs(readme): update setup instructions`
- `refactor(models): simplify project serializer`

## Deployment

### Development Environment

See [Installation & Setup](#installation--setup) above.

### Staging Environment

```bash
DJANGO_SETTINGS_MODULE=config.settings.development python manage.py runserver
```

### Production Environment

1. Use production settings: `DJANGO_SETTINGS_MODULE=config.settings.production`
2. Enable S3 storage: `USE_S3=True`
3. Use Gunicorn or similar WSGI server
4. Use Daphne or Uvicorn for ASGI (WebSockets)
5. Set up proper logging and monitoring
6. Enable security headers and HTTPS

## Resources & Documentation

- **Django Documentation**: https://docs.djangoproject.com/
- **Django REST Framework**: https://www.django-rest-framework.org/
- **ifcopenshell API**: https://ifcopenshell.org/python.html
- **React Documentation**: https://react.dev
- **Vite Documentation**: https://vitejs.dev
- **Architecture Diagrams**: See [architecture_diagram.md](architecture_diagram.md)

## License

BIMFlow Suite is released under the [MIT License](LICENSE).

## Support & Community

- **Issues**: Report bugs on GitHub Issues
- **Discussions**: Start technical discussions in GitHub Discussions
- **Email**: info@bimflowsuite.com

## Changelog

See [release/](release/) folder for version history and release notes.

---

**Last Updated**: January 31, 2026  
**Current Version**: 1.0.0  
**Python**: 3.11+  
**Django**: 5.2+  
**React**: 18.3+