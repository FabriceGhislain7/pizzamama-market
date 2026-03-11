# PizzaMama Market - Architecture Reference

---

# Document Purpose

This document defines the official architecture of the PizzaMama Market project up to the current implementation baseline.

It exists to:

* keep the project aligned with the real codebase
* prevent architectural drift
* support controlled growth
* reduce technical debt
* provide a stable reference for future steps

The content of this file must reflect the real state of the repository.

---

# Architectural Vision

PizzaMama Market is an API-first e-commerce platform designed for:

* progressive scalability
* domain and framework separation
* backend reuse across web, mobile, and integrations
* security by default
* incremental evolution without invasive rewrites

Django is used as:

> API provider and application orchestrator
> not as a traditional template-driven monolith

---

# Core Principles

1. Clear separation of responsibilities
2. Modular domain structure
3. API as the official system interface
4. Default-deny security model
5. Incremental evolution
6. No premature over-engineering

---

# Security Model

Applied principles:

* default deny
* explicit permissions
* no unnecessary public exposure
* separated environment configurations
* stateless authentication for the API

Current authentication status:

* `IsAuthenticated` is the global DRF default permission
* JWT is the default authentication mechanism
* refresh token rotation is enabled
* refresh token blacklist is enabled
* `SessionAuthentication` is added only in development for local convenience
* `BasicAuthentication` is not used

---

# High-Level Architecture

```text
Client (Web / Mobile / External Services)
                |
            REST API v1
                |
       Application Layer (Django)
                |
         Business Logic Layer
                |
          Persistence Layer (ORM)
                |
              Database
```

---

# Layer Separation

## Presentation Layer

Responsibilities:

* frontend rendering
* client state
* API consumption

Rules:

* no business logic
* no direct database access
* no dependency on Django templates

---

## Application Layer

Location:

```text
backend/config/
backend/apps/*/api/
```

Responsibilities:

* routing
* authentication
* permissions
* serialization
* request validation
* API versioning
* schema generation

Complex business logic is not allowed inside:

* serializers
* admin
* signals

---

## Business Logic Layer

Current implementation:

* domain rules live primarily inside models
* the `Order` model contains workflow and financial consistency rules

Possible future evolution:

* `services.py`
* `selectors.py`

This is a future refinement, not a current requirement for already simple domain rules.

---

## Persistence Layer

Technologies:

* Django ORM
* SQLite in development
* PostgreSQL in production

Rules:

* migrations are mandatory
* no manual database modifications
* no undocumented raw queries

---

# Current Repository Structure

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

The virtual environment is not part of the logical architecture.

---

# Core Infrastructure

`apps/core/` contains reusable infrastructure components.

Current example:

* `TimeStampedModel` as an abstract base model

It is shared infrastructure, not a business domain.

---

# Custom User Model

The project uses a custom user model:

```python
class User(AbstractUser, TimeStampedModel)
```

Mandatory setting:

```python
AUTH_USER_MODEL = "accounts.User"
```

Forbidden:

```python
from django.contrib.auth.models import User
```

Reasons:

* extensibility
* profile and loyalty evolution
* cleaner domain ownership
* safer long-term authentication strategy

---

# API Strategy

Official format:

```text
/api/v1/accounts/
/api/v1/products/
/api/v1/orders/
```

Additional platform endpoints:

```text
/api/v1/auth/login/
/api/v1/auth/refresh/
/api/v1/schema/
/api/v1/docs/
```

Rules:

* versioning is mandatory
* no unversioned APIs
* global default permission is `IsAuthenticated`
* public endpoints must be explicitly declared

---

# Implemented Domains

## Accounts

Implemented:

* custom user model
* registration endpoint
* JWT-compatible authentication flow
* logout with refresh token blacklist
* address management
* profile model

---

## Products

Implemented:

* catalog domain modeling
* API exposure through versioned endpoints
* filtering and list support

---

## Orders

Implemented:

* cart and cart items
* order and order items
* payment and delivery information models
* controlled order status workflow
* financial consistency validation
* dedicated API endpoint for status transitions

The `Order` model contains domain logic such as:

* `VALID_TRANSITIONS`
* `change_status()`
* `clean()`
* `save()` with `full_clean()`

---

# Testing State

The project includes an active pytest-based test suite.

Current test scope:

* JWT login
* order status transition workflow
* invalid workflow protection
* order financial validation
* custom change-status endpoint

Testing stack:

* `pytest`
* `pytest-django`
* `factory-boy`
* `coverage`

---

# Settings Strategy

The project uses modular settings:

* `base.py` for shared configuration
* `dev.py` for development
* `prod.py` for production

Rules:

* no monolithic settings file
* no hardcoded production credentials
* fail-fast on critical missing production variables
* environment separation is mandatory

---

# Production Foundation

Current production-oriented elements:

* `SECRET_KEY` from environment variables
* `ALLOWED_HOSTS` from environment variables
* `DEBUG = False` in production
* HSTS enabled
* secure cookies enabled
* SSL redirect enabled
* proxy SSL header configured
* console logging configured
* Gunicorn included in dependencies

---

# Architectural Rules

## Rule 1 - Single Source of Truth

Every business rule must have one authoritative implementation.

Forbidden:

* duplicated logic
* duplicated domain concepts
* contradictory documentation

---

## Rule 2 - Directional Dependencies

Correct flow:

```text
API / Admin
      |
   Models
      |
 Database
```

Possible future service layer:

```text
API / Admin
      |
  Services
      |
   Models
      |
 Database
```

Forbidden:

* circular imports
* business logic inside serializers
* business logic inside admin

---

## Rule 3 - API First

Every external feature must be exposed through the API layer.

Frontend rules:

* no direct data access
* no business rules duplicated in the UI
* no dependence on server-rendered Django pages

---

# Current Baseline

The repository is aligned up to this baseline:

* modular settings
* DRF with global authenticated default
* JWT stateless authentication
* refresh token blacklist and rotation
* production-oriented settings split
* domain-driven `Order` workflow
* pytest-based regression protection

This corresponds to the project state up to Step 15.

---

# Next Direction

The next logical step is not more domain breadth.

It is operational maturity:

* Dockerization
* environment reproducibility
* CI/CD
* stronger automated quality gates

These belong after the current baseline, not inside it.

---

# Final Note

If this document diverges from the codebase:

* the document must be updated
* or the code must be corrected

Documentation is only valid when it matches the repository.
