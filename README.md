![PizzaMama Enterprise](https://images.openai.com/static-rsc-3/7InvxiSJU5gtaEC6KE8vIb0j_MsLbFGBemTCdZt7KBxG6MkkSdI5HbhHY3SK4a1qopU84K51JamSW3JKj8hDjF-Aau_sS1eKzOegrjC--yo?purpose=fullsize\&v=1)

# PizzaMama Market 🍕

## Professional E-commerce Platform for Modern Pizzerias

**PizzaMama Market** is a modern and scalable e-commerce platform designed for pizzerias and food businesses that require a solid, extensible, and business-oriented system.

The project is developed using **Django (backend API)** and **React (frontend)** and follows principles of **professional architecture**, **maintainability**, and **progressive growth**.

This is not a simple demonstration project, but a **real foundation designed to evolve toward production environments**.

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

The application adopts an **API-first** approach, with a clear separation between:

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
* SQLite (development environment)
* PostgreSQL (production target)
* Redis (planned)
* Celery (planned)
* JWT (planned)

### Frontend (Web App)

* React
* JavaScript / TypeScript
* REST API consumption
* Modular and scalable CSS

### Tooling & DevOps

* Docker (planned)
* Environment variable management
* Git
* Project ready for CI/CD pipelines

---

## General Project Structure 📁

```text
pizzamama-market/
├── backend/
│   ├── manage.py
│   ├── config/                # Django project configuration
│   ├── apps/                  # Django apps (accounts, ...)
│   ├── requirements/
│   └── db.sqlite3 (dev)
│
├── frontend/
│   ├── src/
│   ├── public/
│   └── package.json
│
├── docs/
│
├── docker-compose.yml (planned)
└── README.md
```

Detailed technical documentation and architectural decisions are maintained inside the **docs** folder, separated from the main README.

The virtual environment is not part of the architecture.

---

## Business Domains (Backend)

### Accounts

* custom user management (Custom User Model)
* profiles and preferences
* delivery addresses
* loyalty systems (planned)

### Products (planned)

* pizza catalog
* categories
* ingredients
* allergens
* pricing and variants

### Orders (planned)

* cart
* order management
* status workflow
* historical tracking and traceability

The **Payments**, **Delivery**, **Reviews**, and **Analytics** domains are planned as future extensions.

---

## Security and Quality

* authentication via SessionAuthentication (current)
* DRF permissions with IsAuthenticated by default
* server-side validation
* CSRF and CORS protection
* separated environment configurations
* prepared for JWT and advanced RBAC

---

## Development Setup

### Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements/base.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Backend available at:

```
http://127.0.0.1:8000/
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

* structure prepared for unit testing
* API testing
* code organized for continuous refactoring
* versioned migrations

---

## Project Status

* modular settings active
* Custom User Model implemented
* DRF configured
* versioned API `/api/v1/`
* architectural foundation stabilized
* foundation ready for progressive growth

---

## Architectural Checklist

### Foundations

* [ ] Modular settings active (base/dev/prod)
* [ ] Custom User Model configured
* [ ] AUTH_USER_MODEL properly set
* [ ] No direct use of auth.User
* [ ] Correct BASE_DIR

### API

* [ ] Versioning `/api/v1/`
* [ ] IsAuthenticated as default
* [ ] No unintentionally exposed APIs
* [ ] No domain logic inside serializers

### Database

* [ ] Every model change → makemigrations + migrate
* [ ] No manual database modifications
* [ ] Consistent migrations

### Security

* [ ] No hardcoded credentials
* [ ] DEBUG disabled in production
* [ ] BasicAuthentication removed
* [ ] Proper environment separation

### Architecture

* [ ] No circular imports
* [ ] No duplicated logic
* [ ] Business logic outside admin and serializers
* [ ] Consistency with docs/ARCHITECTURE.md

---

## Final Notes

PizzaMama Market is a project focused on:

* advanced learning
* professional backend architecture
* modern web application development
* real-world business contexts

It is a project foundation designed to evolve over time while maintaining clarity, quality, and sustainability.
