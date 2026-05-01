# PizzaMama Market - Internal Technical Documentation

---

# Purpose of This Document

This document is the internal technical guide for the PizzaMama Market repository.

It is intended for:

* backend developers working on the project
* maintaining technical consistency
* guiding controlled evolution
* preventing technical debt
* supporting onboarding

The public `README.md` remains product-oriented.
This document describes the real technical implementation baseline.

---

# Technical Vision

PizzaMama Market is an API-first platform built with:

* Python
* Django
* Django REST Framework
* SQLite as local fallback
* PostgreSQL in production

The backend is designed to be:

* reusable
* modular
* secure
* evolvable

---

# Conceptual Architecture

```text
Client (Web / Mobile / External Services)
                |
            REST API (v1)
                |
        Django Application Layer
                |
         Business Logic Layer
                |
           Django ORM
                |
             Database
```

---

# Architectural Principles

* API-first
* separation of responsibilities
* modular domain structure
* default-deny security mindset
* incremental evolution
* avoid premature over-engineering
* separated environment configurations

---

# Backend Structure

```text
backend/
|-- manage.py
|-- db.sqlite3
|-- pytest.ini
|
|-- config/
|   |-- asgi.py
|   |-- wsgi.py
|   |-- urls.py
|   |-- api_urls.py
|   `-- settings/
|       |-- base.py
|       |-- dev.py
|       `-- prod.py
|
|-- apps/
|   |-- core/
|   |   `-- models.py
|   |
|   |-- accounts/
|   |   |-- models.py
|   |   |-- admin.py
|   |   |-- signals.py
|   |   |-- api/
|   |   |-- migrations/
|   |   `-- tests/
|   |
|   |-- products/
|   |   |-- models.py
|   |   |-- admin.py
|   |   |-- api/
|   |   |-- migrations/
|   |   `-- tests/
|   |
|   `-- orders/
|       |-- models.py
|       |-- admin.py
|       |-- api/
|       |-- migrations/
|       `-- tests/
|
`-- requirements/
```

The virtual environment is not part of the logical project architecture.

---

# Settings Strategy

The project uses modular settings:

* `base.py` for shared configuration
* `dev.py` for development
* `prod.py` for production

Rules:

* no monolithic settings file
* no hardcoded production credentials
* fail-fast on critical production variables
* mandatory environment separation
* prepared for Docker and CI/CD, but not yet containerized in-repo

---

# Django REST Framework

Current DRF baseline:

```python
DEFAULT_PERMISSION_CLASSES = [
    IsAuthenticated
]

DEFAULT_AUTHENTICATION_CLASSES = [
    JWTAuthentication
]
```

Development adds:

```python
SessionAuthentication
```

only in `dev.py` for local convenience.

Current security status:

* all APIs are protected by default
* JWT is active by default
* refresh token rotation is active
* refresh token blacklist is active
* `BasicAuthentication` is not used

---

# Authentication and Accounts

Implemented:

* custom `User` model
* registration endpoint
* JWT login endpoint
* refresh endpoint
* logout with refresh token blacklist
* address CRUD
* profile model

Relevant endpoint groups:

```text
/api/v1/auth/login/
/api/v1/auth/refresh/
/api/v1/accounts/register/
/api/v1/accounts/logout/
/api/v1/accounts/addresses/
```

---

# Products Domain

The products app models the catalog domain and exposes versioned API endpoints.

Current scope includes:

* categories
* ingredients
* pizzas
* pizza size support
* list and detail API exposure
* filtering support

---

# Orders Domain

The orders app already contains business-critical domain behavior.

Current implemented scope:

* cart
* cart items
* order
* order items
* payment
* delivery information
* order workflow endpoint

Important domain rules currently live in the `Order` model:

* controlled `VALID_TRANSITIONS`
* `change_status()` for workflow progression
* `clean()` for amount consistency
* `save()` enforcing `full_clean()`

This means workflow logic is protected at model level, not only at API level.

---

# API Strategy

Official API namespace:

```text
/api/v1/
```

Primary domain groups:

```text
/api/v1/accounts/
/api/v1/products/
/api/v1/orders/
```

Platform endpoints:

```text
/api/v1/schema/
/api/v1/docs/
/api/v1/auth/login/
/api/v1/auth/refresh/
```

Rules:

* versioning is mandatory
* no unversioned APIs
* public endpoints must be explicit
* business logic must not live in serializers

---

# Core Infrastructure

`apps/core/` contains reusable shared infrastructure.

Current example:

* `TimeStampedModel`

It is not a business domain and should remain thin.

---

# Database Strategy

Environments:

* development uses SQLite fallback
* production uses PostgreSQL

Rules:

* every model change requires migrations
* no manual database manipulation
* standard workflow remains:

```bash
python manage.py makemigrations
python manage.py migrate
```

---

# Production Foundation

The project already includes a production-oriented baseline:

* environment-based `SECRET_KEY`
* environment-based `ALLOWED_HOSTS`
* `DEBUG=False` in production
* HSTS enabled
* secure cookies enabled
* SSL redirect enabled
* proxy SSL header configured
* logging configured
* Gunicorn included

This corresponds to the hardening work completed before Dockerization.

---

# Testing Strategy

Current testing stack:

* `pytest`
* `pytest-django`
* `factory-boy`
* `coverage`

Current implemented coverage areas:

* JWT login
* order workflow transitions
* invalid transition protection
* order amount validation
* custom change-status endpoint

Current goal:

* block regressions on critical flows
* allow safer refactors
* expand coverage incrementally

---

# Development Guidelines

* keep apps focused and modular
* avoid business logic inside serializers
* avoid business logic inside admin
* avoid circular imports
* prefer incremental refactors
* update documentation when the baseline changes

---

# Current Project State

The repository is aligned up to Step 15:

* modular settings
* JWT stateless authentication
* refresh token blacklist and rotation
* custom user model
* products domain modeled
* orders domain modeled
* order workflow formalized
* production hardening baseline
* pytest suite active
* versioned API `/api/v1/`
* centralized API routing
* default-deny security model

---

# Project Evolution Checklist

This checklist tracks the backend evolution against:

```text
C:\Users\ghisl\repositories\learning-lab\Develop_Documentation\Django\README_STEPS_SENIOR
```

Before continuing, read the guide in this order:

```text
00-ROADMAP-E-ISTRUZIONI/00-readme-roadmap.md
00-ROADMAP-E-ISTRUZIONI/01-standard-documentazione-step.md
00-ROADMAP-E-ISTRUZIONI/02-checklist-qualita-documentazione.md
00-ROADMAP-E-ISTRUZIONI/03-debug-flusso-funzionale-frontend-api-backend-database.md
FASE-04-Industrializzazione-Produzione-e-Deployment/
```

This preserves the learning path and avoids continuing from assumptions.

## Phase 01 - Fondamenta Progetto

* [x] Step 1 - Monorepo API-first structure created
* [x] Step 2 - Django backend environment installed
* [x] Step 3 - Django project created with `config/` architecture
* [x] Step 4 - Backend installation tested
* [x] Step 5 - Database setup and modular settings completed

## Phase 02 - Backend API e Dominio

* [x] Step 6 - Django REST Framework foundation configured
* [x] Step 7 - Accounts app and custom user model configured
* [x] Step 8 - Profile, address, media and account domain modeled
* [x] Step 9 - Products catalog domain modeled
* [x] Step 10 - Orders domain modeled
* [x] Step 11 - Enterprise API layer implemented

## Phase 03 - Autenticazione, Sicurezza Base e Test

* [x] Step 12 - JWT authentication flow implemented
* [x] Step 13 - Production hardening foundation implemented
* [x] Step 14 - Order workflow and state transitions implemented
* [x] Step 15 - Professional pytest suite implemented and passing

## Phase 04 - Industrializzazione, Produzione e Deployment

* [x] Step 16 - Dockerization with backend and PostgreSQL implemented
  Verification pending: Docker CLI is not available in the current shell.
* [x] Step 17 - CI/CD pipeline implemented
  Verification pending: workflow must run on GitHub after push.
* [x] Step 18 - Monitoring and observability implemented
* [x] Step 19 - Performance and scalability implemented
* [x] Step 20 - Security hardening and abuse protection implemented

Current verified checkpoint:

```text
Steps 1-15 completed and verified.
Steps 16-20 implemented.
Local backend checks pass.
Docker build/up verification is pending because Docker is not available in the current shell.
Remote CI/CD verification is pending until the workflow runs on GitHub.
```

Verification commands:

```powershell
cd backend
.\venv\Scripts\python.exe manage.py check
.\venv\Scripts\python.exe manage.py makemigrations --check --dry-run
.\venv\Scripts\python.exe -m pytest
.\venv\Scripts\python.exe -m black --check apps config manage.py
.\venv\Scripts\python.exe -m flake8 apps config manage.py --jobs=1
```

Expected verification result:

```text
System check identified no issues.
No changes detected.
7 passed.
Black check passes.
Flake8 passes.
```

Docker verification, when Docker is installed:

```powershell
cd backend
docker compose build
docker compose up
```

Expected Docker endpoints:

```text
http://localhost:8000/admin/
http://localhost:8000/api/v1/docs/
```

CI/CD verification, when pushed to GitHub:

```text
.github/workflows/ci.yml
```

Required repository secrets for Docker image publishing:

```text
DOCKER_USERNAME
DOCKER_PASSWORD
```

## Resume Notes

When work resumes, do not restart from Step 1.

Resume by checking:

```powershell
git status --short
cd backend
.\venv\Scripts\python.exe manage.py check
.\venv\Scripts\python.exe manage.py makemigrations --check --dry-run
.\venv\Scripts\python.exe -m pytest
```

Then continue from the first unresolved external verification:

```powershell
cd backend
docker compose build
docker compose up
```

If Docker works, verify:

```text
http://localhost:8000/health/
http://localhost:8000/api/v1/docs/
```

After Docker verification, push to GitHub and verify the workflow:

```text
.github/workflows/ci.yml
```

The next guide file after Fase 04 is:

```text
FASE-05-Funzionalita-Business-Reali/21-payment-integration-enterprise.md
```

Only start Step 21 after Docker and GitHub Actions are verified or explicitly accepted as pending.

---

# Next Logical Evolutions

The next steps after the current baseline are:

* Dockerization
* local environment reproducibility
* CI/CD
* broader automated coverage
* observability

These are not yet completed in the repository.

---

# Final Note

This document must always match the real state of the project.

If code and documentation diverge:

* update the document
* or correct the code

Consistency is mandatory.
