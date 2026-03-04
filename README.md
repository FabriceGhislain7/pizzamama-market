![PizzaMama Enterprise](https://images.openai.com/static-rsc-3/7InvxiSJU5gtaEC6KE8vIb0j_MsLbFGBemTCdZt7KBxG6MkkSdI5HbhHY3SK4a1qopU84K51JamSW3JKj8hDjF-Aau_sS1eKzOegrjC--yo?purpose=fullsize\&v=1)

# PizzaMama Market 🍕

## Professional E-commerce Platform for Modern Pizzerias

## Live Demo

### Production API Documentation

[https://pizzamama-market-backend.onrender.com/api/v1/docs/](https://pizzamama-market-backend.onrender.com/api/v1/docs/)

The interactive Swagger interface allows full exploration of all endpoints, authentication via JWT, and complete schema inspection.

---

**PizzaMama Market** is a modern and scalable e-commerce platform designed for pizzerias and food businesses that require a solid, extensible, and business-oriented system.

The project is developed using **Django (backend API)** and **React (frontend)** and follows principles of **professional architecture**, **maintainability**, and **progressive growth**.

This is not a simple demonstration project, but a real foundation designed to evolve toward production environments.

---

## Project Goals

PizzaMama Market was created with the goal of:

* correctly modeling real business domains
* clearly separating frontend, backend, and domain logic
* reducing technical debt over time
* supporting new features without invasive rewrites
* serving as a foundation for web, mobile, and external integrations

---

## Architectural Vision

The application adopts an API-first approach, with a clear separation between:

* business logic
* application layer
* interfaces (API and UI)

Architectural principles adopted:

* complete frontend / backend separation
* backend independent from rendering
* modular and well-isolated domains
* scalability-oriented design
* code structured for continuous evolution

---

## Technology Stack

### Backend (API)

* Python 3.10+
* Django 5.x
* Django REST Framework
* PostgreSQL (production)
* SQLite (development fallback)
* JWT Authentication (stateless)
* Refresh token rotation and blacklist
* Modular settings (base / dev / prod)

### Frontend (Web App)

* React
* JavaScript / TypeScript
* REST API consumption
* Modular and scalable CSS

### Tooling & DevOps

* Gunicorn (WSGI server)
* Render deployment
* Environment variable management
* Git branching strategy (main / develop)
* Project prepared for CI/CD
* Docker (planned)
* Redis (planned)
* Celery (planned)

---

## General Project Structure 📁

```text
pizzamama-market/
├── backend/
│   ├── manage.py
│   ├── config/
│   │   ├── settings/
│   │   │   ├── base.py
│   │   │   ├── dev.py
│   │   │   └── prod.py
│   ├── apps/
│   │   ├── accounts/
│   │   ├── products/
│   │   └── orders/
│   ├── requirements/
│   └── db.sqlite3 (development only)
│
├── frontend/
│   ├── src/
│   ├── public/
│   └── package.json
│
├── docs/
└── README.md
```

The virtual environment is not part of the architecture.

---

## API Overview

The backend exposes a versioned API under `/api/v1/`.

Available domains:

### Accounts

* User registration
* JWT login
* Token refresh
* Logout with refresh token blacklist
* Address management (CRUD)

### Authentication

* `/api/v1/auth/login/`
* `/api/v1/auth/refresh/`

JWT-based stateless authentication is enforced by default.

### Products

* Categories listing
* Pizza catalog listing
* Detail endpoints
* Filtering and pagination support

### Orders

* Order creation
* Order listing
* Order detail
* Update and deletion
* Controlled status transition endpoint
* Domain-driven state machine

### Schema

* `/api/v1/schema/`
* Fully documented OpenAPI 3.0 schema

All endpoints are documented in Swagger.

---

## Security and Production Hardening

* JWT authentication (stateless)
* Refresh token rotation
* Blacklist after rotation
* DRF `IsAuthenticated` as default permission
* No hardcoded credentials
* Environment-based configuration
* DEBUG disabled in production
* Secure cookies in production
* HSTS enabled
* Proxy SSL header configuration
* Structured logging

---

## Development Setup

### Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements/base.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Backend available at:

```
http://127.0.0.1:8000/api/v1/docs/
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend available at:

```
http://localhost:5173/
```

---

## Frontend ↔ Backend Communication

* communication exclusively through REST APIs
* reusable backend for web, mobile, and external services
* complete separation between presentation and business logic

---

## Testing and Maintainability

* domain logic centralized inside models
* serializers free from business logic
* versioned API `/api/v1/`
* structured migrations
* architecture ready for professional test suite expansion

---

## Deployment Strategy

* Production branch: `main`
* Staging branch: `develop`
* Separate Render services per environment
* Environment variables isolated per service
* Production-grade settings active on both environments

### Staging API Documentation

[https://pizzamama-market-backend-develop.onrender.com/api/v1/docs/](https://pizzamama-market-backend-develop.onrender.com/api/v1/docs/)

---

## Architectural Checklist

### Foundations

* [x] Modular settings active (base/dev/prod)
* [x] Custom User Model configured
* [x] AUTH_USER_MODEL properly set
* [x] No direct use of auth.User
* [x] Correct BASE_DIR

### API

* [x] Versioning `/api/v1/`
* [x] IsAuthenticated as default
* [x] No unintentionally exposed APIs
* [x] No domain logic inside serializers

### Database

* [x] Every model change → makemigrations + migrate
* [x] No manual database modifications
* [x] Consistent migrations

### Security

* [x] No hardcoded credentials
* [x] DEBUG disabled in production
* [x] BasicAuthentication removed
* [x] Proper environment separation

### Architecture

* [x] No circular imports
* [x] No duplicated logic
* [x] Business logic inside domain models
* [x] API-first structure

---

## Final Notes

PizzaMama Market is a project focused on:

* advanced learning
* professional backend architecture
* modern web application development
* real-world business contexts

It is a project foundation designed to evolve over time while maintaining clarity, quality, and sustainability.
