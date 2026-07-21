# Environment Variables — PizzaMama Market

## Backend

| Variabile | Ambiente | Obbligatoria | Descrizione |
|---|---|---|---|
| DJANGO_SECRET_KEY | tutti | si | chiave segreta Django (min 50 char) |
| DJANGO_SETTINGS_MODULE | production | si | `config.settings.prod` |
| ALLOWED_HOSTS | production | si | domini separati da virgola |
| DATABASE_URL | production | si | stringa connessione PostgreSQL |
| REDIS_URL | production | no | stringa connessione Redis |
| SENTRY_DSN | production | no | DSN Sentry per error tracking |
| DEFAULT_FROM_EMAIL | production | no | email mittente per notifiche |

## Frontend

| Variabile | Ambiente | Obbligatoria | Descrizione |
|---|---|---|---|
| VITE_API_BASE_URL | tutti | si | URL base API Django |

## Regole

- Mai committare valori reali nel repository
- Usare `.env.example` con valori fittizi come documentazione
- Ruotare `DJANGO_SECRET_KEY` se esposta
- `DATABASE_URL` production solo su Render (env vars del servizio)
