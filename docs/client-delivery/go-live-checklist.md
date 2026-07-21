# Go Live Checklist — PizzaMama Market

## Backend

- [x] `DEBUG=False` in produzione
- [x] `ALLOWED_HOSTS` configurato con fail-fast
- [x] `DATABASE_URL` production configurato su Render
- [x] Migrazioni applicate (`python manage.py migrate`)
- [x] Static files raccolti (`collectstatic` nel docker-compose)
- [x] `setup_roles` eseguito al primo deploy

## Security

- [x] HTTPS attivo (Render gestisce SSL automaticamente)
- [x] Segreti non presenti nel repository (`.env` in `.gitignore`)
- [x] CORS ristretto (solo origini autorizzate in `prod.py`)
- [x] Rate limiting attivo (50/h anon, 500/h user, 5/min login)
- [x] Account lockout dopo 5 tentativi falliti (django-axes)
- [x] JWT rotation + blacklist attivi
- [ ] Backup PostgreSQL verificato su Render

## Test

- [x] Suite pytest verde (25/25 test)
- [x] CI/CD pipeline attiva su GitHub Actions
- [ ] Login testato in ambiente production
- [ ] Ordine testato end-to-end
- [ ] Restore database testato su staging

## Monitoring

- [x] Health check attivo (`GET /health/`)
- [x] Sentry configurato (se SENTRY_DSN impostato)
- [x] Logging JSON strutturato attivo
- [x] Audit log attivo (login, logout, cambio status)
