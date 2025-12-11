# BIM-Automation-Toolkits
BIMFlow Suite is a cloud-native BIM automation platform designed to enhance Building Information Modeling (BIM) processes. It aims to streamline workflows through a comprehensive software solution that integrates user management, data visualization, and compliance checking, ultimately improving efficiency and collaboration in construction and architecture projects.

A collection of tools and services for programmatic BIM generation, rule-based compliance checking, and a thorough analysis.

This repository contains a Django-based backend (project: `bimflow/`) and a React + Vite frontend (`bimflow-ui/`). The backend hosts parametric IFC generators, a compliance engine that evaluates IFC models against YAML "rulepacks", and supporting apps for analytics and intent capture.

## Quick architecture

- Backend (Django): `bimflow/` — multiple Django apps (see below). Entrypoint: `bimflow/manage.py`.
- Frontend (React + Vite): `bimflow-ui/` (run with `npm run dev`).
- Rulepacks: YAML rule definitions under `bimflow/rulepacks/` and `bimflow/compliance_engine/rulepacks/`.
- Runtime: env vars via `python-dotenv`; settings live in `bimflow/settings.py` and per-environment under `bimflow/settings/`.

## Getting started (development)

### Prerequisites

- Python 3.10+
- Node.js 18+ / npm
- Redis for Channels & Celery when running real-time or background workers
- Database: PostgreSQL

### Backend (local)

1. Create and activate a virtual environment (zsh):

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install Python dependencies:

```bash
pip install -r bimflow/requirements.txt
```

3. Run migrations and start the development server (default `settings.py` uses SQLite):

```bash
cd bimflow
# Use the default consolidated settings, or point to an env-specific module
DJANGO_SETTINGS_MODULE=bimflow.settings python manage.py migrate
DJANGO_SETTINGS_MODULE=bimflow.settings python manage.py runserver
```

Notes: `bimflow/settings/development.py` contains an example Postgres configuration; if you switch to Postgres, set appropriate env vars and `DJANGO_SETTINGS_MODULE=bimflow.settings.development`.

### Frontend (local)

```bash
cd bimflow-ui
npm install
npm run dev
```

### Build frontend for production

```bash
cd bimflow-ui
npm run build
```

## Background workers and realtime

- Celery tasks (long-running generation or compliance checks) use Redis as broker/default. Example worker command:

```bash
# run from project root
celery -A bimflow worker -l info
```

- Channels (WebSockets) needs a running Redis channel layer. In production use Daphne or Uvicorn with ASGI application (`bimflow.asgi.application`).

## Important environment variables

Some environment variables are required for runtime features:

- `DATABASE_URL` or Postgres-specific vars used in `settings/development.py`
- `BIMFLOW_RULEPACKS_DIR` — folder for rulepack YAMLs (defaults to `compliance_engine/rulepacks`)
- `OPENAI_API_KEY`, `STRIPE_API_KEY`, `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN` — external integrations (provide sandbox keys locally)
- `CELERY_BROKER_URL`, `CELERY_RESULT_BACKEND` — e.g. `redis://localhost:6379/0`


## Key backend components (where to look)

- `bimflow/settings.py` — central defaults (SQLite, Channels, Celery, JWT config)
- `bimflow/urls.py` — top-level routes (Admin, `/api/v1/`, JWT token endpoints, GraphQL, Swagger)
- `parametric_generator/` — IFC generation: `generators/` (e.g., `building.py`), `models.py`, and `tasks.py` for async runs
- `compliance_engine/` — `rule_engine.py`, `clash_detector.py`, `models.py` (`ComplianceCheck`, `RulePack`), and the `rulepacks/` folder
- `api/v1/` — REST endpoints and auth handlers

## Project-specific conventions

- Generators: add new generators to `parametric_generator/generators/` as modules exposing `generate_*` functions that accept a JSON spec and return an IFC string.
- Rulepacks: named `default_<asset>.yaml`; `RulePack.get_default_pack(asset_type_code)` loads the YAML from `BIMFLOW_RULEPACKS_DIR`.
- Long-running geometry work (IFC parsing, clash detection) should be executed in Celery workers — `ifcopenshell` operations can be CPU/memory heavy.

## Running tests

Backend tests (Django):

```bash
cd bimflow
DJANGO_SETTINGS_MODULE=bimflow.settings python manage.py test
```

## Rule engine & clash detector (quick notes)

- `compliance_engine/rule_engine.py` loads YAML rulepacks and evaluates rules against an IFC string; results are persisted as `ComplianceCheck` records.
- `compliance_engine/clash_detector.py` contains an `AdvancedClashDetector` that uses `ifcopenshell.geom` to compute bounding boxes and check hard/soft clashes. Expect these calls to sometimes fail silently — add logging when debugging geometry issues.

## Safe-edit guidance and common pitfalls

- Do not rename or remove `core/` or `parametric_generator` models without updating foreign keys (e.g., `ComplianceCheck.model`).
- `core1/` looks experimental — search for imports before refactoring or deleting.
- When changing settings, avoid committing secrets
- When editing rulepacks, ensure YAML schema matches loader expectations; the `RulePack` model loads YAML with `yaml.safe_load`.


## Files to open first (recommended)

- `bimflow/settings.py`
- `bimflow/urls.py`
- `parametric_generator/generators/building.py`
- `compliance_engine/rule_engine.py` and `clash_detector.py`
- `parametric_generator/tasks.py`
- `api/v1/urls.py`

## Example API: Compliance endpoint

This service evaluates an IFC (text) against a rulepack and returns a `ComplianceCheck` result. The REST endpoint lives under `api/v1/` — look for a path like `/api/v1/compliance/` or similar in `api/v1/urls.py`.

Example request (JSON payload):

```http
POST /api/v1/compliance/ HTTP/1.1
Host: localhost:8000
Authorization: Bearer <ACCESS_TOKEN>
Content-Type: application/json

{
  "model_id": "optional-generated-model-id",
  "rule_pack": "default_building",
  "ifc": "<base64-or-raw-ifc-string>",
  "include_clash": true
}
```

Example successful response (HTTP 200/201):

```json
{
  "id": 123,
  "model": 42,
  "rule_pack": "default_building",
  "status": "passed",
  "results": [
    {"rule": "wall_height", "passed": true, "details": []},
    {"rule": "door_clearance", "passed": false, "details": [{"msg": "Door clearance 0.6m < 0.8m"}]}
  ],
  "clash_results": {
    "summary": {"total_clashes": 1, "hard_clashes": 1, "soft_clashes": 0},
    "clashes": [
      {"id_a":"0xA","id_b":"0xB","type":"hard","description":"Overlap between IfcWall and IfcDuctSegment"}
    ]
  },
  "checked_at": "2025-12-07T12:34:56Z"
}
```

Example error response (HTTP 400):

```json
{ "detail": "Missing 'ifc' in request body" }
```

Notes
- The endpoint may accept raw IFC text, a base64-encoded IFC string, or an uploaded file — check the `api/v1` serializer/view implementation.
- Authentication: JWT Bearer tokens.

## Checklist: Running large IFC checks in Celery

When running expensive geometry operations (IFC parsing, shape creation, clash detection) in Celery workers, follow this checklist to reduce failures and resource contention:

1. Use a dedicated worker queue and concurrency limit for geometry tasks:

```bash
# run worker for geometry tasks only
celery -A bimflow worker -Q geometry -c 1 -l info
```

2. Increase worker memory limits or use autoscaling for heavy jobs (Kubernetes HPA or multiple worker replicas).

3. Persist the raw IFC to disk or object storage before processing and stream it into the task to avoid huge message payloads in the broker.

4. Wrap `ifcopenshell.geom` calls with try/except and log full stack traces; capture partial results where possible.

5. Use temporary isolated working directories per task and clean up artifacts on completion to avoid disk buildup.

6. Add timeouts and retries with exponential backoff for flaky geometry conversions.

7. If GPU-accelerated geometry is available, ensure the worker has exclusive access to those devices.

8. Monitor task durations and failures (Celery events, Flower, or Prometheus) and set alerting for unusual error rates.

9. For very large models, consider splitting evaluation into spatial partitions (tile the model) and merge results.

10. Record resource usage in logs (memory/CPU) to help tune concurrency.