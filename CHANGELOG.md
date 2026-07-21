# Changelog — PizzaMama Market

## [Unreleased]

### Added — Backend completo (2026-06-04)

- Audit Logging (Step 18): AuditLog immutabile, AuditMiddleware, AuditService, hook login/logout/status
- Celery Task Queue (Step 19): worker, beat, task email/kitchen/cleanup, django-celery-beat
- RequestID Middleware (Step 26): header `X-Request-ID` su ogni risposta
- Analytics/BI Layer (Step 27): SalesQueries, DashboardService, endpoint `/api/v1/analytics/dashboard/`
- Principle of Least Privilege (Step 28): IsFinance permission, ruolo Finance, upload limit 2MB
- GDPR/Privacy (Step 30): PrivacyService, endpoint `/api/v1/accounts/me/export/`
- OWASP SDLC (Step 32): test security ownership, OWASP checklist, code review checklist
- Database scripts (Step 31): backup_postgres.ps1, restore_postgres.ps1
- Frontend security docs (Step 33): strategia token, regole CORS
- Incident Response Runbooks (Step 34): downtime, database, pagamento, admin compromesso
- Documentazione consegna (Step 35): installazione locale, variabili ambiente, go-live checklist, manuale admin

### Changed

- docker-compose: Redis esposto solo internamente (`expose` non `ports`)
- docker-compose: aggiunto servizio `celery_worker` e `celery_beat`
- CORS: aggiunto `localhost:5173` per sviluppo frontend Vite

### Infrastructure

- 25 test pytest verdi
- CI/CD GitHub Actions attivo (test + coverage + lint + Docker build)
- Deploy su Render: production (main) + staging (develop)

## [0.17.0] — RBAC Enterprise

- Role-Based Access Control via Django Groups nativi
- Ruoli: Manager, Kitchen, Delivery, Staff, IT_Admin
- State machine ordini con transizioni validate

## [0.1.0] — Fondamenta

- Django 5.2 + DRF + JWT stateless (SimpleJWT)
- Modelli: User, Profile, Address, Category, Pizza, Order, Payment
- Docker + PostgreSQL + Redis
- pytest + factory-boy
