# 🍕 PizzaMama Market – Architecture Reference (Aligned Version)

---

# Document Purpose

This document defines the **official and binding architecture** of the PizzaMama Market project.

It exists to:

* maintain long-term consistency
* prevent architectural drift
* support controlled growth
* reduce technical debt
* guarantee safe evolution

The rules defined here are **not optional**.

---

# Architectural Vision

PizzaMama Market is an **API-first** e-commerce platform designed for:

* progressive scalability
* domain/framework separation
* backend reuse (web, mobile, integrations)
* security by design
* evolution without invasive rewrites

Django is used as:

> API provider and application orchestrator
> Not as a traditional MVC monolith

---

# Core Principles

1. Clear separation of responsibilities
2. Modular domain structure
3. Zero Trust Security
4. API as the only official interface
5. Incremental evolution
6. No premature over-engineering

---

# Security Philosophy (Zero Trust)

Applied principles:

* Default deny
* Explicit permissions
* No implicit trust between layers
* No unnecessary exposure
* Separated environment configurations
* Prepared for JWT (JSON Web Token)

Current authentication status:

* SessionAuthentication active
* DEFAULT_PERMISSION_CLASSES = IsAuthenticated
* BasicAuthentication removed
* JWT planned for future evolution

---

# Official Naming Strategy

| Element              | Convention         |
| -------------------- | ------------------ |
| Public URL           | Italian kebab-case |
| Domain variables     | Italian snake_case |
| Domain classes       | Italian PascalCase |
| Django/DRF framework | English            |
| Authentication model | `User` (English)   |

Clear separation between domain and framework.

---

# High-Level Architecture

```
Client (Web / Mobile / External Services)
                ↓
            REST API v1
                ↓
       Application Layer (Django)
                ↓
         Business Logic Layer
                ↓
          Persistence Layer (ORM)
                ↓
              Database
```

---

# Layer Separation

## 1️⃣ Presentation Layer (Frontend)

* React (target)
* Client state
* API calls
* No business logic
* No direct database access

---

## 2️⃣ Application Layer (Django)

Location:

```
backend/config/
backend/apps/
```

Responsibilities:

* Routing
* Authentication
* Permissions
* Serialization
* Input validation
* API versioning
* Admin interface

⚠ Complex business logic is forbidden inside:

* serializers
* admin
* signals

---

## 3️⃣ Business Logic Layer

Lives inside the apps.

Can be organized into:

```
services.py
selectors.py
```

Principles:

* No logic inside serializers
* No logic inside admin
* No complex logic inside signals
* No duplication

---

## 4️⃣ Persistence Layer

Technologies:

* Django ORM
* SQLite (development)
* PostgreSQL (production target)

Rules:

* Migrations mandatory
* No manual database modifications
* No undocumented raw queries

---

# Official Current Structure (Real State)

```
backend/
├── manage.py
├── db.sqlite3
│
├── config/
│   ├── asgi.py
│   ├── wsgi.py
│   ├── urls.py
│   └── settings/
│       ├── base.py
│       ├── dev.py
│       └── prod.py
│
├── apps/
│   ├── core/
│   │   └── models.py      ← TimeStampedModel (abstract)
│   │
│   └── accounts/
│       ├── models.py      ← Custom User
│       ├── admin.py
│       ├── apps.py
│       └── migrations/
│
├── requirements/
└── venv/
```

---

# Core Module (Domain Infrastructure)

`apps/core/` contains reusable components.

Example:

* TimeStampedModel (abstract)

It is not a business domain.
It is not registered in INSTALLED_APPS.

---

# Custom User Model (Mandatory Rule)

The project uses a Custom User Model:

```python
class User(AbstractUser, TimeStampedModel)
```

It is mandatory:

```python
AUTH_USER_MODEL = "accounts.User"
```

It is forbidden:

```python
from django.contrib.auth.models import User
```

Reasons:

* future extensibility
* JWT compatibility
* loyalty management
* RBAC flexibility

---

# API Strategy

Official format:

```
/api/v1/accounts/
/api/v1/products/
/api/v1/orders/
```

Rules:

* Versioning mandatory
* No unversioned APIs
* Default permission: IsAuthenticated
* Public endpoints explicitly declared

---

# Fundamental Rules

## Rule 1 — Single Source of Truth

Every business concept must have only one definition.

Forbidden:

* duplicating logic
* duplicating models
* inconsistent naming

---

## Rule 2 — Directional Dependencies

Correct flow:

```
API / Admin
      ↓
  Services
      ↓
    Models
      ↓
   Database
```

Forbidden:

* circular imports
* logic inside serializers
* logic inside admin

---

## Rule 3 — API First

Every feature must be exposed via API.

Frontend:

* does not access the database
* does not contain domain rules
* does not depend on Django templates

---

# Planned Domains

## Accounts

* users
* profiles
* addresses
* authentication
* roles and permissions
* loyalty

## Products

* catalog
* categories
* variants
* pricing

## Orders

* cart
* orders
* status workflow
* history

---

# Target Evolution Structure (Not Yet Implemented)

```
apps/
├── accounts/
│   ├── models.py
│   ├── services.py
│   ├── api/
│   └── urls.py
│
├── products/
├── orders/
├── payments/
```

This represents the future direction, not the current state.

---

# Migrations

Rules:

* Every model change → makemigrations + migrate
* Versioned migrations
* No manual database manipulation

---

# Database Strategy

Environments:

* Dev → SQLite
* Prod → PostgreSQL

Future:

* Redis
* Celery
* Docker

---

# Future Extensions

* JWT Authentication
* Advanced RBAC
* Payments
* Delivery
* Reviews
* Analytics
* Observability

---

# Final Note

If a modification violates this document:

The modification must be rejected.

This file represents the **official architectural truth** of the PizzaMama Market project.
