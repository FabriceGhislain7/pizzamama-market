# 🍕 PizzaMama Market – Internal Technical Documentation (Aligned)

---

# Purpose of This Document

This document represents the **internal operational technical guide** of the PizzaMama Market project.

It is intended for:

* backend developers working on the project
* maintaining architectural consistency
* guiding controlled technical evolution
* preventing technical debt
* facilitating onboarding

The main `README.md` remains product-oriented.
This document is focused on real technical implementation.

---

# Technical Vision

PizzaMama Market is an **API-first** platform built with:

* Python
* Django
* Django REST Framework
* SQLite (development)
* PostgreSQL (production target)

Clear separation between:

* Application Layer (Django)
* Business Logic Layer
* Persistence Layer
* Presentation Layer (independent frontend)

The backend is designed to be:

* reusable
* modular
* secure
* evolvable

---

# Conceptual Architecture

```id="arch001"
Client (Web / Mobile / External Services)
                ↓
            REST API (v1)
                ↓
        Django Application Layer
                ↓
         Business Logic Layer
                ↓
           Django ORM
                ↓
             Database
```

---

# Architectural Principles

* API-first
* separation of responsibilities
* modular domain structure
* zero trust mindset
* incremental evolution
* avoid premature over-engineering
* separated environment configurations

---

# Backend Structure (Current Real State)

```id="struct001"
backend/
├── manage.py
├── db.sqlite3
│
├── config/
│   ├── asgi.py
│   ├── wsgi.py
│   ├── urls.py
│   ├── api_urls.py
│   └── settings/
│       ├── base.py
│       ├── dev.py
│       └── prod.py
│
├── apps/
│   ├── core/
│   │   └── models.py              # TimeStampedModel (abstract)
│   │
│   ├── accounts/
│   │   ├── models.py              # Custom User + Profile + Address
│   │   ├── admin.py
│   │   ├── api/
│   │   └── migrations/
│   │
│   ├── products/
│   │   ├── models.py              # Category, Ingredient, Pizza, etc.
│   │   ├── admin.py
│   │   ├── api/
│   │   └── migrations/
│   │
│   └── orders/
│       ├── models.py              # Cart, Order, OrderItem, Payment
│       ├── admin.py
│       ├── api/
│       └── migrations/
│
├── requirements/
└── venv/
```

Note:
The virtual environment is not part of the logical architecture.

---

# Settings Strategy

The project uses modular settings:

* `base.py` → shared configuration
* `dev.py` → development
* `prod.py` → production

Rules:

* No monolithic settings file
* No hardcoded production credentials
* Mandatory environment separation
* Prepared for Docker / CI/CD

---

# Django REST Framework

Current configuration:

```python
DEFAULT_PERMISSION_CLASSES = [
    IsAuthenticated
]

DEFAULT_AUTHENTICATION_CLASSES = [
    SessionAuthentication,
    TokenAuthentication
]
```

Current security status:

* All APIs protected by default
* BasicAuthentication removed
* Session and Token authentication active
* JWT planned as future evolution

---

# Naming Strategy

Official rules:

| Element              | Convention         |
| -------------------- | ------------------ |
| Public URL           | Italian kebab-case |
| Domain variables     | Italian snake_case |
| Domain classes       | Italian PascalCase |
| Django/DRF framework | English            |

Clear separation between domain and framework.

---

# `core` Module

The `apps/core/` folder contains shared infrastructure components.

Currently includes:

* `TimeStampedModel` (abstract)

It does not represent a business domain.
It must not contain concrete models.

---

# Custom User Model

The project uses a Custom User Model from the beginning.

Implementation:

```python
class User(AbstractUser, TimeStampedModel)
```

Mandatory configuration:

```python
AUTH_USER_MODEL = "accounts.User"
```

Rules:

* Never import `User` from `django.contrib.auth.models`
* Always use `settings.AUTH_USER_MODEL`
* No direct relation to `auth.User`

---

# Role of the `apps/` Folder

Contains all application code.

Each app includes:

* models
* admin
* domain logic (future `services.py`)
* API layer (`api/`)
* migrations

Fundamental rule:

> No Django model outside `apps/`.

---

# Domain Logic

Currently implemented inside models with controlled scope.

Future direction:

* `services.py` per domain
* optional read/write separation
* no complex logic inside serializers or admin

---

# API Strategy

Official format:

```id="api001"
/api/v1/accounts/
/api/v1/products/
/api/v1/orders/
```

Rules:

* Versioning mandatory
* No unversioned APIs
* Default permission: IsAuthenticated
* Public endpoints explicitly declared

API routing is centralized in:

```text
backend/config/api_urls.py
```

---

# Database Strategy

Environments:

* Dev → SQLite
* Prod → PostgreSQL

Rules:

* Every model change → mandatory migration
* No manual database modification
* Standard workflow:

```bash
python manage.py makemigrations
python manage.py migrate
```

---

# Security

Current principles:

* Default deny
* Global IsAuthenticated
* Server-side validation
* SessionAuthentication active
* TokenAuthentication active
* Prepared for JWT
* Separated environment settings

Future:

* JWT
* Advanced RBAC
* Structured logging
* Audit trail

---

# Testing Strategy

Structure prepared for:

* model tests
* service tests
* API tests
* integration tests

Objective:

* controlled regressions
* safe refactors
* increasing reliability

---

# Development Guidelines

* keep apps focused and modular
* avoid logic inside serializers
* avoid logic inside admin
* avoid circular imports
* perform incremental refactors
* every modification must have architectural justification

---

# Current Project State

Foundation and core domains completed:

* modular settings
* DRF configured
* Token authentication active
* Custom User implemented
* Products domain modeled
* Orders domain modeled
* Clean migrations
* Working admin
* Versioned API `/api/v1/`
* Centralized API routing
* Default deny security model

---

# Evolutionary Objective

Next logical evolutions:

* Service layer formalization
* Production hardening
* JWT authentication
* Payments domain expansion
* Delivery integration
* Reviews
* Observability

The system is designed to grow without invasive rewrites.

---

# Final Note

This document must always reflect the real state of the project.

If code and document diverge:

* either the document must be updated
* or the code must be corrected

Consistency is mandatory.
