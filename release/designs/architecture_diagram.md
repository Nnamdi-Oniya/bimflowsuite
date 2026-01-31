# BIMFlow Suite Architecture - Visual Overview

## System Architecture Diagram

```
┌────────────────────────────────────────────────────────────────────────────┐
│                       FRONTEND (React + Vite + TypeScript)                 │
│  ┌──────────────────┐  ┌──────────────┐  ┌────────────────────────────┐  │
│  │  Upload IFC Page │  │ Generate Form│  │  Compliance Check Page     │  │
│  │ (File upload)    │  │ (30+ fields) │  │  + Results visualization   │  │
│  └────────┬─────────┘  └───────┬──────┘  └──────────┬─────────────────┘  │
│           │                    │                     │                    │
│  ┌──────────────────┐  ┌──────────────────┐  ┌────────────────────────┐ │
│  │  Account/Auth    │  │  Project List    │  │  Dashboard + Analytics │ │
│  │  (Login/Register)│  │  (View & Filter) │  │  (Project Metrics)     │ │
│  └────────┬─────────┘  └───────┬──────────┘  └──────────┬─────────────┘ │
│           │                    │                        │                 │
└───────────┼────────────────────┼────────────────────────┼─────────────────┘
            │ HTTP (JWT Token)   │                        │
            ├────────────────────────────────────────────┤
            ▼
┌────────────────────────────────────────────────────────────────────────────┐
│                       DJANGO REST API (DRF)                                │
│  ┌──────────────────────────────────────────────────────────────────────┐ │
│  │ /api/v1/auth/          ← Users App (Login, Register, Accounts)      │ │
│  │ /api/v1/                ← Multiple app routes:                       │ │
│  │   ├─ generate/          ← Parametric Generator (IFC creation)       │ │
│  │   ├─ compliance/        ← Compliance Engine (Rule checks, clashes)  │ │
│  │   ├─ analytics/         ← Analytics (Upload analysis, metrics)      │ │
│  │   └─ organizations/     ← Users App (Multi-tenant management)       │ │
│  └──────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
│  ┌─────────────────────────────────┐  ┌──────────────────────────────┐    │
│  │ Serializers & ViewSets          │  │ Middleware Layer             │    │
│  │ - ProjectSerializer             │  │ - JWT Authentication         │    │
│  │ - GeneratedIFCSerializer        │  │ - CORS Support               │    │
│  │ - ComplianceCheckSerializer     │  │ - Permission Checks          │    │
│  │ - User/Organization/RulePackSerial
│  └─────────────────────────────────┘  └──────────────────────────────┘    │
└────────────────────────┬─────────────────────────────────────────────────┘
                         │
         ┌───────────────┼───────────────┐
         │               │               │
         ▼               ▼               ▼
┌─────────────────┐ ┌─────────────────┐ ┌──────────────────┐
│ Parametric      │ │  Compliance     │ │   Analytics      │
│ Generator App   │ │ Engine App      │ │  App             │
│                 │ │                 │ │                  │
│ - Project model │ │ - RuleEngine    │ │ - ProjectMetrics │
│ - GeneratedIFC  │ │ - AdvancedClash │ │ - UploadedIFC    │
│ - Generator     │ │   Detector      │ │ - Analysis Tools │
│   functions     │ │ - Compliance    │ │                  │
│ - Celery tasks  │ │   Check model   │ │                  │
└────────┬────────┘ └────────┬────────┘ └────────┬─────────┘
         │                   │                    │
         └───────────────────┼────────────────────┘
                             │
                             ▼
┌────────────────────────────────────────────────────────────────────────────┐
│                        DJANGO ORM LAYER                                    │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────────┐    │
│  │  Project Model   │  │ GeneratedIFC     │  │ ComplianceCheck      │    │
│  │  (30+ fields)    │  │ Model            │  │ Model                │    │
│  │                  │  │                  │  │                      │    │
│  │ - Basic info     │  │ - asset_type     │  │ - generated_ifc (FK) │    │
│  │ - Client info    │  │ - status         │  │ - rule_pack          │    │
│  │ - Location data  │  │ - specifications │  │ - results (JSON)     │    │
│  │ - Materials      │  │ - ifc_file       │  │ - clash_results      │    │
│  │ - Organization   │  │ - error_message  │  │ - status             │    │
│  └────────┬─────────┘  └────────┬─────────┘  └──────────┬──────────┘    │
│           │                     │                       │                 │
└───────────┼─────────────────────┼───────────────────────┼─────────────────┘
            │                     │                       │
            └─────────────────────┼───────────────────────┘
                                  │
                                  ▼
                    ┌──────────────────────┐
                    │ PostgreSQL (Local &  │
                    │ Production)          │
                    │ (S3 for IFC storage) │
                    └──────────────────────┘
```

## Data Flow: Three Main Workflows

### Workflow 1: Upload & Analyze Existing IFC

```
┌─────────────────────┐
│ User selects IFC    │
│ file to upload      │
└────────┬────────────┘
         │ POST /api/v1/analytics/upload_ifc/
         ▼
┌──────────────────────────────────────┐
│ Analytics App ViewSet                │
│ - Validate file format (IFC)         │
│ - Store upload metadata              │
│ - Create UploadedIFC record          │
└────────┬─────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────┐
│ Celery Worker                        │
│ - Parse IFC using ifcopenshell       │
│ - Extract geometry metrics           │
│ - Calculate project statistics       │
│ - Store analysis results             │
└────────┬─────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────┐
│ Frontend receives analysis           │
│ - Displays extracted metrics         │
│ - Shows component breakdown          │
│ - Visualizes geometry (3D viewer)    │
└──────────────────────────────────────┘
```

### Workflow 2: Generate New IFC from Project Form

```
┌──────────────────────┐
│ User fills form      │
│ (30+ project fields) │
└────────┬─────────────┘
         │ POST /api/v1/generate/projects/
         ▼
┌────────────────────────────────────────┐
│ Parametric Generator App               │
│ - Validate project data                │
│ - Create Project record                │
│ - Associate with user/org              │
└────────┬───────────────────────────────┘
         │ POST /api/v1/generate/ifcs/create_for_project/
         ▼
┌────────────────────────────────────────┐
│ GeneratedIFC ViewSet                   │
│ - Create GeneratedIFC (status: pending)│
│ - Store specifications from form       │
│ - Return IFC ID to frontend            │
└────────┬───────────────────────────────┘
         │ Trigger Celery Task
         ▼
┌────────────────────────────────────────┐
│ Celery Worker (Async Generation)       │
│ 1. Load project specifications         │
│ 2. Select appropriate generator        │
│    (building.py, road.py, bridge.py)   │
│ 3. Generate IFC using ifcopenshell     │
│ 4. Save to S3 or local storage         │
│ 5. Update GeneratedIFC status:         │
│    "completed" + file path             │
└────────┬───────────────────────────────┘
         │
         ▼
┌────────────────────────────────────────┐
│ Frontend (WebSocket/Polling)           │
│ - Poll for status updates              │
│ - Show generation progress             │
│ - Enable download when complete        │
└──────────────────────────────────────┘
```

### Workflow 3: Compliance Check & Clash Detection

```
┌──────────────────────────────┐
│ User initiates compliance    │
│ check on existing IFC        │
│ (uploaded or generated)      │
└────────┬─────────────────────┘
         │ POST /api/v1/compliance/checks/
         ▼
┌──────────────────────────────────────┐
│ Compliance Engine ViewSet             │
│ - Validate IFC reference              │
│ - Load appropriate YAML rulepack      │
│   (default_building.yaml, etc.)       │
│ - Create ComplianceCheck (pending)    │
└────────┬─────────────────────────────┘
         │ Trigger Celery Task
         ▼
┌──────────────────────────────────────┐
│ Celery Worker (Rule Evaluation)       │
│ 1. Parse IFC file                     │
│ 2. Extract building elements          │
│    (walls, columns, slabs, etc.)      │
│ 3. Evaluate YAML conditions:          │
│    - wall_count > 5                   │
│    - avg_height < 30 meters           │
│    - material compliance              │
│ 4. Run AdvancedClashDetector:         │
│    - Hard clashes (tolerance: 0.01m)  │
│    - Soft clashes (tolerance: 0.05m)  │
│ 5. Store results in ComplianceCheck   │
└────────┬─────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────┐
│ Frontend displays results             │
│ - Passed/failed rules breakdown       │
│ - Clash locations (3D highlighting)   │
│ - Remediation suggestions             │
│ - Export compliance report (PDF)      │
└──────────────────────────────────────┘
```

### Workflow 4: User Authentication & Account Management

```
┌────────────────────┐
│ User registers or  │
│ submits demo req   │
└────────┬───────────┘
         │ POST /api/v1/auth/register/
         │ or /api/v1/auth/request-submission/
         ▼
┌──────────────────────────────────────┐
│ Users App ViewSet                     │
│ - Validate email/credentials          │
│ - Create User + Organization          │
│ - Send welcome/verification email     │
│ - Create RequestSubmission record     │
└────────┬─────────────────────────────┘
         │ POST /api/v1/auth/login/
         ▼
┌──────────────────────────────────────┐
│ TokenObtainPairView (JWT)             │
│ - Verify credentials                  │
│ - Generate access token (60 min)      │
│ - Generate refresh token (7 days)     │
│ - Return tokens to frontend           │
└────────┬─────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────┐
│ Frontend stores JWT in localStorage   │
│ - Send with each API request          │
│ - Authorization: Bearer <token>       │
│ - Redirect to dashboard on success    │
└──────────────────────────────────────┘
```
   │ Frontend Download Btn  │
   │ (IFC id: 1)            │
   └────────┬───────────────┘
            │ GET /api/v1/bim-projects/ifcs/1/download/
            ▼
   ┌────────────────────────────────────┐
   │ GeneratedIFCViewSet.download()     │
   │ - Verify ownership                 │
   │ - Generate S3 signed URL (15 min)  │
   │ - Log download                     │
   └────────┬─────────────────────────────┘
            │ Return download_url, filename, file_size
            ▼
   ┌────────────────────────────────┐
   │ Frontend Redirects to S3        │
   │ (or streams if local storage)   │
   └────────┬───────────────────────┘
            │ Browser downloads IFC file
            ▼
   ┌────────────────────────────────┐
   │ User has IFC file locally       │
   │ Ready for use in Revit/Navisw.. │
   └────────────────────────────────┘
```

## AWS S3 & File Storage Integration

```
LOCAL DEVELOPMENT (USE_S3=false):
┌────────────────────────┐
│ Django Local Storage   │
│ (FileSystemStorage)    │
└────────┬───────────────┘
         │
         ▼
   /media/ifc_files/2024/01/01/project_building_1.ifc
   (Served by Django static file handler)


PRODUCTION (USE_S3=true):
┌──────────────────────────────────────────────┐
│ django-storages + boto3                      │
│ AWS_ACCESS_KEY_ID                            │
│ AWS_SECRET_ACCESS_KEY                        │
│ AWS_STORAGE_BUCKET_NAME                      │
│ AWS_S3_REGION_NAME                           │
└────────┬─────────────────────────────────────┘
         │
         ▼
   ┌──────────────────────────────────────┐
   │ AWS S3 Bucket                        │
   │ ├─ ifc_files/                        │
   │ │  └─ 2024/01/01/                    │
   │ │     ├─ project_building_1.ifc ◄──┐
   │ │     ├─ analysis_bridge_2.ifc   │  │
   │ │     └─ compliance_road_3.ifc   │  │
   │ │                                 │  │
   │ ├─ Private bucket (IAM policy)     │  │
   │ ├─ Versioning enabled              │  │
   │ └─ Object encryption (optional)    │  │
   └──────────────────────────────────────┘
         ▲
         │ S3 API calls (boto3)
         │
   ┌─────────────────────────────────┐
   │ GeneratedIFC.ifc_file.save()    │
   │ UploadedIFC.file.save()         │
   │ (Automatically handles uploads) │
   └─────────────────────────────────┘
```
   │ Frontend Download Btn  │
   │ (IFC id: 1)            │
   └────────┬───────────────┘
            │ GET /api/v1/bim-projects/ifcs/1/download/
            ▼
   ┌────────────────────────────────────┐
   │ GeneratedIFCViewSet.download()     │
   │ - Verify ownership                 │
   │ - Generate S3 signed URL (15 min)  │
   │ - Log download                     │
   └────────┬─────────────────────────────┘
            │ Return download_url, filename, file_size
            ▼
   ┌────────────────────────────────┐
   │ Frontend Redirects to S3        │
   │ (or streams if local storage)   │
   └────────┬───────────────────────┘
            │ Browser downloads IFC file
            ▼
   ┌────────────────────────────────┐
   │ User has IFC file locally       │
   │ Ready for use in Revit/Navisw.. │
   └────────────────────────────────┘
```

## AWS S3 Integration Flow

```
LOCAL DEVELOPMENT:
┌─────────────────┐
│ Django Storage  │  USE_S3=false
│   (Local Disk)  │
└────────┬────────┘
         │
         ▼
   /media/ifc_files/2024/01/01/project_building_1.ifc
   (served by Django static file handler)


PRODUCTION (AWS S3):
┌──────────────────────────┐
│ django-storages          │  USE_S3=true
│ + boto3 client           │
└────────┬─────────────────┘
         │
         ▼
   ┌─────────────────────────────────────────────┐
   │ AWS S3 Bucket                               │
   │ ├─ ifc_files/                               │
   │ │  ├─ 2024/                                 │
   │ │  │  ├─ 01/                                │
   │ │  │  │  ├─ 01/                             │
   │ │  │  │  │  └─ project_building_1.ifc ◄──┐
   │ │  │  │  │  └─ project_road_2.ifc    │    │
   │ │  │  │  │  └─ project_bridge_3.ifc  │    │
   │ ├─ IAM Policy (Private)                     │
   │ └─ Versioning enabled (optional)            │
   └─────────────────────────────────────────────┘
         ▲
         │ boto3 client
         │ (AWS_ACCESS_KEY_ID,
         │  AWS_SECRET_ACCESS_KEY)
         │
   ┌─────────────────────────────┐
   │ GeneratedIFC.ifc_file.save()│
   │ - Upload to S3              │
   │ - Generate S3 URL           │
   │ - Return signed URL         │
   └─────────────────────────────┘
```

## Permission & Ownership Model

```
┌─────────────────────────────────────────────────────────────────┐
│                         AUTHENTICATION LAYER                     │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ JWT Token (60 min expiry)                                │  │
│  │ Contains: user_id, exp, token_type                       │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────┬──────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    PERMISSION CHECKING                          │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ Request comes in with Authorization header              │  │
│  │ 1. JWT validated (signature, expiry)                     │  │
│  │ 2. User extracted from token                            │  │
│  │ 3. View checks IsAuthenticated                          │  │
│  └──────────────────────────────────────────────────────────┘  │
│                         ▼                                       │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ IsProjectOwner Permission Check                         │  │
│  │ if obj.user != request.user:                            │  │
│  │     return 403 Forbidden                                │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘

EXAMPLE:
User A's Token          User B's Token
    │                       │
    ▼                       ▼
GET /projects/1/         GET /projects/1/
│                        │
├─ user_id: A           ├─ user_id: B
├─ Project 1.user: A    └─ Project 1.user: A
│                       
├─ Check: A == A ✓        Check: B == A ✗
└─ 200 OK                 403 Forbidden
```

## Database Schema - Core Models

```
┌─────────────────────────────────────────────────────────────┐
│                    auth_user (Django)                       │
│ ┌────────────────────────────────────────────────────────┐ │
│ │ id (PK)  | username | email | password | is_staff    │ │
│ │ 1        | alice    | a@... | ***...   | False       │ │
│ │ 2        | bob      | b@... | ***...   | False       │ │
│ └────────────────────────────────────────────────────────┘ │
└────┬───────────────────────────────────────────────────────┘
     │ 1:N
     ▼
┌──────────────────────────────────────────────────────────────────┐
│         parametric_generator_project (Project Model)            │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │id│user│org│name      │number     │status│building_type│...│ │
│ │1 │ 1  │1  │Downtown  │DOC-2024   │det   │office    │...    │ │
│ │2 │ 1  │1  │Highway   │HW-2024    │con   │road      │...    │ │
│ │3 │ 2  │2  │Hospital  │H-2024     │sch   │hospital  │...    │ │
│ │                                                          │ │
│ │ 30+ fields: client, location, climate, materials(JSON)│ │
│ │ Indexes: (user, created_at), (project_number)         │ │
│ └─────────────────────────────────────────────────────────────┘ │
└────┬──────────────────────────────┬────────────────────────┬───┘
     │ 1:N (FK: project_id)         │ 1:N (FK: project_id)   │
     ▼                              ▼                        ▼
┌──────────────────────────────┐  ┌─────────────────────┐ ┌───────┐
│ GeneratedIFC Model           │  │ UploadedIFC Model   │ │Project│
│ (IFC Generation)             │  │ (Analysis)          │ │Metrics│
│ ┌────────────────────────────┐│ │ ┌─────────────────┐│ └───────┘
│ │id│project│asset_type│status││ │id│file│size│...││
│ │1 │  1    │building  │done  ││ │1 │s3..│2MB │...││
│ │2 │  1    │road      │pend  ││ │2 │s3..│5MB │...││
│ │3 │  2    │bridge    │gen   ││ │3 │s3..│3MB │...││
│ │                          ││ │                     ││
│ │Indexes: (project,status)││ │Indexes: (user_id) ││
│ └────────────────────────────┘│ └─────────────────┘│
└──────────────────────────────┘  └─────────────────┘
         │ 1:N
         ▼
┌──────────────────────────────────────────────────┐
│ ComplianceCheck Model                            │
│ ┌──────────────────────────────────────────────┐ │
│ │id│ifc_id│rule_pack│status │results│clashes│ │
│ │1 │  1   │building │passed │[...]  │[...]  │ │
│ │2 │  2   │road     │failed │[...]  │[...]  │ │
│ │3 │  3   │bridge   │pend   │[]     │[]     │ │
│ │                                            │ │
│ │Indexes: (ifc_id), (status), (checked_at) │ │
│ └──────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────┘
```

## Request/Response Flow Example

```
FRONTEND                          API                      DATABASE
    │                              │                          │
    │ POST /projects/              │                          │
    │ {name: "Test", ...}          │                          │
    ├─────────────────────────────►│                          │
    │                              │ Validate serializer      │
    │                              ├─┐                        │
    │                              │◄┘                        │
    │                              │                          │
    │                              │ Insert into DB           │
    │                              ├─────────────────────────►│
    │                              │                          │ saved
    │                              │◄─────────────────────────┤
    │                              │                          │
    │                              │ Serialize to JSON        │
    │                              ├─┐                        │
    │◄─────────────────────────────┤◄┘                        │
    │ 201 Created                  │                          │
    │ {id: 1, name: "Test", ...}   │                          │
    │                              │                          │
```

## Admin Interface Layout

```
┌──────────────────────────────────────────────────────────────┐
│ Django Admin - Projects                                      │
├──────────────────────────────────────────────────────────────┤
│ Search | Filter (Status | Building Type | Created)           │
├────────┬──────────────┬────────┬─────────┬────────────────┤
│ Number │ Name         │ Status │ Building│ IFCs Generated │
├────────┼──────────────┼────────┼─────────┼────────────────┤
│ DOC-01 │ Downtown ... │ Deta   │ Office  │ 3              │
│ HW-001 │ Highway  ... │ Schem  │ Road    │ 1              │
│ H-2024 │ Hospital ... │ Concept│ Hospital│ 0              │
└────────┴──────────────┴────────┴─────────┴────────────────┘

┌──────────────────────────────────────────────────────────────┐
│ Project Detail View                                          │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  Basic Information            │  Location                    │
│  ├─ Name                      │  ├─ Country                 │
│  ├─ Description               │  ├─ City/Address            │
│  ├─ Project Number            │  ├─ Coordinates             │
│  ├─ Status: [dropdown]        │  ├─ Elevation               │
│  │                            │  └─ North Angles            │
│  Building Info                │  Materials (JSON)            │
│  ├─ Building Type             │  ├─ Walls                   │
│  ├─ Climate Zone              │  ├─ Slabs                   │
│  ├─ Design Temp               │  └─ Properties               │
│  │                            │                             │
│  IFC Generation Summary        │                             │
│  ├─ Total: 3                  │                             │
│  ├─ ✓ Completed: 2            │                             │
│  ├─ ⏳ Generating: 0           │                             │
│  ├─ ⏰ Pending: 1              │                             │
│  └─ ✗ Failed: 0               │                             │
│                                                              │
│  [Save Changes]  [Delete]  [History]                        │
└──────────────────────────────────────────────────────────────┘
```

---
