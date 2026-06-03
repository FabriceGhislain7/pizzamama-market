# AVANZAMENTO PROGETTO — PizzaMama Market

> Documento di stato per AI. Leggendo questo file si ha il contesto completo del progetto,
> le decisioni prese, lo stack attivo e il prossimo step da eseguire.

---

## CONTESTO GENERALE

**Progetto:** PizzaMama Market — e-commerce pizzeria  
**Architettura:** Monorepo con backend Django API-first + frontend React  
**Repository:** `C:\Users\ghisl\repositories\pizzamama-market`  
**Branch principale:** `main` (production) / `develop` (staging)  
**Workflow guida:** `C:\Users\ghisl\repositories\dev-workflow\Develop\01-PizzaMama-Django-React\`

Ogni step di sviluppo ha un file `.md` guida nel workflow. Prima di implementare qualsiasi step, leggere il file corrispondente.

---

# I. BACKEND (Django)

**Cartella:** `backend/`  
**Step completati:** 1 → 17  
**Prossimo step:** Step 18 — Audit Logging

## Stack attivo

| Componente | Versione | Stato |
|---|---|---|
| Python | 3.13.7 | ✔ |
| Django | 5.2.x | ✔ |
| Django REST Framework | 3.16.x | ✔ |
| SimpleJWT | 5.5.x | ✔ |
| drf-spectacular (Swagger) | 0.29.x | ✔ |
| django-axes (brute force) | 8.3.x | ✔ |
| django-cors-headers | 4.9.x | ✔ |
| django-redis | 6.0.x | ✔ |
| dj-database-url | 3.1.x | ✔ |
| psycopg2-binary | 2.9.x | ✔ |
| python-json-logger | 4.1.x | ✔ |
| sentry-sdk | 2.58.x | ✔ |
| pytest + pytest-django | 9.0.x | ✔ |
| factory-boy | 3.3.x | ✔ |
| gunicorn | 25.1.x | ✔ |

## Struttura cartelle backend

```
backend/
├── apps/
│   ├── core/
│   │   ├── models.py           (TimeStampedModel base)
│   │   ├── views.py            (health_check endpoint)
│   │   ├── permissions.py      (IsManager, IsKitchen, IsDelivery, IsStaff, IsITAdmin, IsManagerOrITAdmin)
│   │   └── tests/
│   │       ├── test_health.py
│   │       └── test_api_root.py
│   ├── accounts/
│   │   ├── models.py           (User custom, Profile, Address)
│   │   ├── services/
│   │   │   └── role_service.py (RoleService.setup_roles())
│   │   ├── management/
│   │   │   └── commands/
│   │   │       └── setup_roles.py
│   │   └── tests/
│   │       ├── factories.py    (UserFactory)
│   │       ├── test_api.py
│   │       └── test_rbac.py
│   ├── products/
│   │   └── models.py           (Category, Pizza, PizzaSize, Ingredient, Allergen, PizzaIngredient)
│   └── orders/
│       ├── models.py           (Cart, CartItem, Order, OrderItem, Payment, DeliveryInfo)
│       ├── api/
│       │   ├── serializers.py
│       │   ├── views.py        (OrderViewSet con RBAC)
│       │   └── urls.py
│       └── tests/
│           ├── test_api.py
│           └── test_workflow.py
├── config/
│   ├── settings/
│   │   ├── base.py
│   │   ├── dev.py
│   │   └── prod.py
│   ├── urls.py
│   └── api_urls.py             (api_root pubblico, auth JWT, swagger)
├── requirements/
│   └── base.txt
├── Dockerfile                  (python:3.11-slim, gunicorn, healthcheck)
├── docker-compose.yml          (web + db PostgreSQL15 + redis Redis7)
├── .dockerignore
├── .env                        (DATABASE_URL commentata → SQLite locale)
├── .env.example
└── pytest.ini
```

## Autenticazione

- JWT stateless via SimpleJWT
- Access token: 15 minuti
- Refresh token: 7 giorni con rotazione e blacklist
- Logout reale (blacklist token)
- Permission globale DRF: `IsAuthenticated`
- Endpoint: `POST /api/v1/auth/login/`, `POST /api/v1/auth/refresh/`

## RBAC — Ruoli enterprise (Step 17)

Implementato via Django Groups nativi (NON campi booleani).

| Ruolo | Accesso ordini | Accesso prodotti |
|---|---|---|
| Customer | Solo propri ordini | — |
| Manager | Tutti gli ordini | — |
| Kitchen | Solo ordini in `preparing` | — |
| Delivery | Solo ordini `out_for_delivery` assegnati a lui | — |
| Staff | — | CRUD Pizza |
| IT_Admin | Tutti gli ordini | — |

Inizializzazione: `python manage.py setup_roles`

**Regola critica:** `change_status` endpoint richiede `IsManagerOrITAdmin`. Un Customer che tenta ottiene 403.

## Modello Order — dettagli chiave

```python
# State machine
VALID_TRANSITIONS = {
    "pending": ["confirmed", "cancelled"],
    "confirmed": ["preparing", "cancelled"],
    "preparing": ["ready"],
    "ready": ["out_for_delivery"],
    "out_for_delivery": ["delivered"],
}

# Campo aggiunto in step 17
assigned_to = ForeignKey(User, null=True, blank=True, related_name="assigned_orders")

# Validazione economica in clean()
# subtotal + delivery_fee + tax_amount - discount_amount == total_amount

# full_clean() forzato in save() → nessun ordine incoerente salvabile
```

## API endpoints attivi

```
GET  /api/v1/              → API root (pubblico, AllowAny)
GET  /health/              → health check DB
GET  /api/v1/docs/         → Swagger UI
POST /api/v1/auth/login/   → JWT login
POST /api/v1/auth/refresh/ → JWT refresh
GET/POST /api/v1/orders/   → ordini (queryset filtrato per ruolo)
POST /api/v1/orders/{id}/change-status/ → solo Manager/IT_Admin
GET/POST /api/v1/accounts/ → profili utente
GET/POST /api/v1/products/ → prodotti
```

## Docker (Step 16)

```yaml
# docker-compose.yml
services:
  db:    postgres:15  (healthcheck pg_isready)
  redis: redis:7      (healthcheck redis-cli ping)
  web:   Django+Gunicorn :8000
         DATABASE_URL: postgres://pizzamama:pizzamama@db:5432/pizzamama
         depends_on: db e redis con condition: service_healthy
```

Avvio locale con Docker: `docker compose up`  
Avvio locale senza Docker: `.\venv\Scripts\Activate.ps1` → SQLite fallback automatico

## Settings

- `base.py`: configurazione condivisa, SQLite fallback, JWT, DRF, logging JSON
- `dev.py`: DEBUG=True
- `prod.py`: SECURE_SSL_REDIRECT (via env), HSTS, cookie secure, fail-fast su SECRET_KEY e ALLOWED_HOSTS
- `DJANGO_SETTINGS_MODULE=config.settings.prod` nel docker-compose

## Test suite

**15 test passanti** (`pytest`):

| Test | Area |
|---|---|
| test_login_returns_tokens | JWT |
| test_login_failure_returns_generic_error | JWT |
| test_change_status_endpoint | Order API (Manager) |
| test_valid_status_transition | Order domain |
| test_invalid_status_transition | Order domain |
| test_total_amount_validation | Order validation |
| test_health_check_returns_ok | Health endpoint |
| test_health_check_db_down | Health endpoint degradato |
| test_api_root_is_public | API root |
| test_manager_can_access_change_status | RBAC |
| test_customer_cannot_change_status | RBAC → 403 |
| test_manager_sees_all_orders | RBAC queryset |
| test_customer_sees_only_own_orders | RBAC queryset |
| test_role_service_creates_all_groups | RoleService |
| test_it_admin_can_access_change_status | RBAC IT_Admin |

## Deploy

| Ambiente | Branch | URL |
|---|---|---|
| Production | main | pizzamama-market-backend.onrender.com |
| Staging | develop | pizzamama-market-backend-develop.onrender.com |

PostgreSQL su Render, HTTPS attivo, DEBUG=False, JWT attivo.

## Decisioni architetturali consolidate

1. API-first obbligatorio — nessuna pagina server-side
2. Business logic nei model, serializer senza logica dominio
3. JWT unico sistema auth — nessuna session/cookie auth
4. `IsAuthenticated` globale + permission class per ruolo
5. Settings modulari base/dev/prod — fail-fast su variabili critiche mancanti
6. Separazione ambienti staging/production
7. Test automatici con pytest — nessun commit senza test verdi
8. Docker per ambiente replicabile — DATABASE_URL nel docker-compose, non nel .env
9. RBAC via Django Groups nativi — mai campi booleani `is_manager`, `is_kitchen`
10. Queryset sempre filtrato per ruolo — mai accesso globale per default
11. `full_clean()` in `save()` — nessun dato incoerente nel DB
12. Logging JSON strutturato su stdout

## Debito tecnico backend

1. Nessuna pipeline CI/CD
2. Nessun audit log eventi (prossimo: Step 18)
3. Nessun monitoring strutturato (Step 22)
4. `setup_roles` da eseguire manualmente al primo deploy

---

# II. FRONTEND (React)

**Cartella:** `frontend/`  
**Step completati:** FASE-01 (step 1-5) + FASE-02 (step 6-8)  
**Prossimo step:** FASE-03 — Routing, Layout e Design System

## Stack attivo

| Componente | Versione | Stato |
|---|---|---|
| Node.js | 22.20.0 | ✔ |
| npm | 11.6.1 | ✔ |
| React | 19.2.x | ✔ |
| TypeScript | 6.0.x | ✔ |
| Vite | 8.0.x | ✔ |
| ESLint | 10.3.x | ✔ |
| Prettier | 3.8.x | ✔ |

## Struttura cartelle frontend

```
frontend/
├── src/
│   ├── app/
│   │   └── settings.ts     (apiBaseUrl centralizzato, fail-fast se mancante)
│   ├── pages/              (pagine dell'app)
│   ├── components/         (componenti riutilizzabili)
│   ├── features/           (logica per dominio: auth, orders, products)
│   ├── services/           (chiamate API al backend)
│   ├── types/              (TypeScript types/interfaces)
│   ├── hooks/              (custom React hooks)
│   ├── utils/              (funzioni di utilità)
│   ├── styles/             (CSS globali e variabili)
│   ├── App.tsx             (componente root)
│   ├── main.tsx            (entry point React 19 + StrictMode)
│   └── index.css           (CSS reset minimale)
├── public/
├── .env.example            (VITE_API_BASE_URL=http://127.0.0.1:8000/api/v1)
├── .env.local              (non committato)
├── .gitignore
├── .prettierrc             (semi, singleQuote:false, trailingComma:all, printWidth:100)
├── vite.config.ts          (alias @/ → src/)
├── tsconfig.app.json       (paths @/* → src/*, ignoreDeprecations:6.0)
└── package.json
```

## Alias @/ configurato

```ts
// vite.config.ts
resolve: { alias: { "@": path.resolve(__dirname, "./src") } }

// tsconfig.app.json
"paths": { "@/*": ["src/*"] }
```

Import esempio: `import { settings } from "@/app/settings"`

## settings.ts — configurazione centralizzata

```ts
export const settings = {
  apiBaseUrl: import.meta.env.VITE_API_BASE_URL,  // fail-fast se mancante
} as const;
```

Mai usare `import.meta.env.VITE_*` direttamente nei componenti — sempre passare per `settings`.

## Script disponibili

```bash
npm run dev          # dev server su http://localhost:5173
npm run build        # build production (tsc + vite build)
npm run lint         # ESLint
npm run format       # Prettier write
npm run format:check # Prettier check
```

## Connessione al backend

`VITE_API_BASE_URL` in `.env.local` → `http://127.0.0.1:8000/api/v1`  
In produzione: URL Render del backend.

## Cosa manca ancora (FASE-03+)

- Routing (React Router)
- Layout shell (header, footer, sidebar)
- Design system / CSS framework
- Gestione stato (Zustand o React Query)
- Autenticazione JWT lato frontend
- Pagine: login, menu, carrello, ordini

---

# RIEPILOGO RAPIDO

| Area | Ultimo step | Prossimo |
|---|---|---|
| Backend Django | Step 17 — RBAC | Step 18 — Audit Logging |
| Frontend React | FASE-02 — Architettura | FASE-03 — Routing e Layout |

**Per continuare il backend:** leggere  
`dev-workflow\...\Backend-Django\FASE-04-Funzionalita-Business-Reali\18-audit-logging-enterprise.md`

**Per continuare il frontend:** leggere  
`dev-workflow\...\Frontend-React\FASE-02-Architettura-Frontend\`
