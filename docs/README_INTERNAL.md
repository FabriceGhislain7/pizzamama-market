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
