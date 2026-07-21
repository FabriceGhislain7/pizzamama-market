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
**Step completati:** 1 → 35 (BACKEND COMPLETATO)  
**Prossimo step:** Frontend — Step 15 (Catalogo prodotti)

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

## Audit Logging (Step 18)

App `apps/audit/` con:
- `AuditLog` — modello UUID immutabile (`_state.adding` guard), indici su user/action/model/created_at
- `AuditMiddleware` — cattura IP e User-Agent via thread-locals
- `AuditService.log()` — entry point unico per tutti i log
- Hook in `Order.change_status()` — log `status_change` con before/after
- Hook in `CustomTokenObtainPairSerializer` — log `login` ad ogni accesso riuscito
- Hook in `LogoutView` — log `logout`
- Admin read-only (no add/change/delete)
- **20 test verdi** (inclusi 5 specifici per audit)

## Step 19 — Celery (Task Queue)

- `config/celery.py` + `config/__init__.py` (celery_app)
- `apps/orders/tasks.py`: `send_order_confirmation_email` (retry 3x), `notify_kitchen`, `cleanup_abandoned_carts`
- `django_celery_beat` per task schedulati (periodic tasks via DB)
- Docker: servizi `celery_worker` + `celery_beat` nel `docker-compose.yml`
- Redis esposto solo internamente (`expose`, non `ports`)
- CELERY settings in `base.py` (broker/backend da REDIS_URL)

## Step 26 — RequestID Middleware

- `apps/core/middleware/request_id.py`: ogni request riceve `X-Request-ID` header

## Step 27 — Analytics/BI Layer

- `apps/analytics/queries/sales_queries.py`: `today_sales`, `top_selling_products`, `weekly_trend`, `customer_lifetime_value`
- `apps/analytics/services/dashboard_service.py`: `DashboardService.manager_dashboard()`
- `GET /api/v1/analytics/dashboard/` — protetto da IsManager | IsITAdmin

## Step 28 — Principle of Least Privilege

- `IsFinance` permission class in `core/permissions.py`
- Ruolo `Finance` aggiunto al `RoleService`
- `DATA_UPLOAD_MAX_MEMORY_SIZE = 2MB` in `base.py`
- Redis: `expose` invece di `ports` nel docker-compose (non accessibile dall'esterno)

## Step 30 — GDPR / Privacy

- `apps/accounts/services/privacy_service.py`: `PrivacyService.export_user_data()`
- `GET /api/v1/accounts/me/export/` — export dati utente autenticato (no password, no token)
- `docs/compliance/data-register.md`
- `docs/compliance/data-retention-policy.md`

## Step 32 — OWASP SDLC

- `apps/orders/tests/test_security.py`: 5 test ownership (BOLA, auth, GDPR)
- `docs/security/owasp-api-checklist.md`
- `docs/security/security-code-review-checklist.md`
- **25 test verdi** (inclusi 5 security)

## Debito tecnico backend residuo

1. Step 33-35: documentazione consegna cliente (README, changelog, runbook)
2. `setup_roles` da eseguire manualmente al primo deploy

---

# II. FRONTEND (React)

**Cartella:** `frontend/`  
**Step completati:** 1-34 (FRONTEND COMPLETATO)  
**Prossimo step:** — Nessuno. Progetto completo. Avviare backend + frontend e testare end-to-end.

## Stack attivo

| Componente | Versione | Stato |
|---|---|---|
| Node.js | 22.20.0 | ✔ |
| npm | 11.6.1 | ✔ |
| React | 19.2.x | ✔ |
| react-router-dom | 7.16.x | ✔ |
| TypeScript | 6.0.x | ✔ |
| Vite | 8.0.x | ✔ |
| ESLint | 10.3.x | ✔ |
| Prettier | 3.8.x | ✔ |

## Struttura cartelle frontend

```
frontend/src/
├── app/
│   ├── router.tsx       (createBrowserRouter, routes con AppLayout)
│   └── settings.ts      (apiBaseUrl centralizzato, fail-fast)
├── pages/
│   ├── HomePage.tsx
│   ├── MenuPage.tsx     (placeholder — attende API prodotti)
│   ├── CartPage.tsx
│   └── NotFoundPage.tsx
├── components/
│   ├── layout/
│   │   ├── AppLayout.tsx        (shell: header + outlet + footer)
│   │   ├── Header.tsx           (NavLink attivi)
│   │   └── Footer.tsx
│   ├── ui/
│   │   └── Button.tsx           (varianti: primary/secondary/danger/ghost, size, loading)
│   └── state/
│       ├── LoadingState.tsx
│       ├── ErrorState.tsx       (con pulsante retry)
│       └── EmptyState.tsx
├── features/
│   └── cart/
│       ├── cartContext.ts       (CartContext + CartContextValue interface)
│       ├── CartProvider.tsx     (useReducer, persistenza automatica)
│       ├── useCart.ts           (hook)
│       ├── cartStorage.ts       (localStorage: load/save/clear)
│       └── index.ts
├── services/
│   └── api/
│       ├── httpClient.ts        (get/post/patch/delete, Bearer token automatico)
│       └── apiErrors.ts        (ApiError class, toUserMessage(), messaggi IT)
├── types/
│   ├── product.ts               (Pizza, Category, Ingredient, PizzaSize)
│   ├── order.ts                 (Order, OrderItem, CartItem, OrderStatus)
│   ├── user.ts                  (User, Address, AuthTokens)
│   └── index.ts                 (re-export + PaginatedResponse<T>)
└── styles/
    ├── tokens.css               (CSS custom properties: colori, spacing, tipografia, radius)
    └── global.css               (reset + stili base importa tokens.css)
```

## Routing

```
/          → HomePage
/menu      → MenuPage (placeholder API)
/cart      → CartPage
*          → NotFoundPage
```

Tutte le route dentro `AppLayout` (header + footer). NotFound fuori dal layout.

## Design tokens (tokens.css)

Variabili CSS per: `--color-primary` (#e63946), `--color-text`, `--color-border`,  
`--space-1..8`, `--font-size-sm..3xl`, `--radius-sm/md/lg`, `--shadow-sm/md`.

## httpClient — regole

- Mai chiamare `fetch` direttamente nei componenti — sempre `httpClient.get/post/...`
- Token JWT letto da `localStorage.access_token` e iniettato automaticamente
- Risposta 204 → ritorna `undefined`
- Errore HTTP → lancia `ApiError(status, message, detail)`
- `toUserMessage(error)` converte errori tecnici in messaggi italiani per l'utente

## Carrello (CartProvider)

- Stato gestito con `useReducer` (ADD/REMOVE/UPDATE_QTY/CLEAR)
- Persistenza automatica su `localStorage` (chiave: `pizzamama_cart`)
- Calcolo `totalItems` e `totalPrice` derivati dallo stato
- Inizializzato da `loadCart()` al primo render
- Accesso via `useCart()` hook — lancia errore se usato fuori da `CartProvider`

## Decisioni architetturali frontend

1. CSS Modules per stili componente — nessun framework CSS esterno
2. Design tokens in `tokens.css` — nessun valore hardcoded nei componenti
3. `httpClient` unico punto di accesso alle API — mai `fetch` diretto
4. `settings.ts` unico punto per variabili ambiente — mai `import.meta.env.*` nei componenti
5. `declare` per class fields TypeScript 6 (`erasableSyntaxOnly`)
6. Contesti separati in file `.ts` puri — Provider in `.tsx` separato (react-refresh)

## Cosa manca

- Step 15: catalogo prodotti da API Django (`/api/v1/products/`)
- Step 18: login/register con JWT
- Step 19: AuthContext e gestione token
- Step 20: protected routes, logout, sessione scaduta
- Step 21: CORS/CSRF configurazione backend
- Step 22-26: checkout, ordini, profilo, staff, dashboard

**CORS sbloccato (2026-06-04):** `django-cors-headers` ora include `http://localhost:5173` in `dev.py`.  
**Prossimo step frontend:** Step 15 — catalogo prodotti (il backend è pronto, CORS ok).

---

# RIEPILOGO RAPIDO

| Area | Ultimo step | Prossimo |
|---|---|---|
| Backend Django | Step 32 — OWASP SDLC | Step 33-35 (documentazione consegna) |
| Frontend React | Step 17 — Cart + API client | Step 15 — Catalogo prodotti (CORS ok) |

**Backend completato** (2026-06-04): tutti gli step fino al 32 sono implementati e testati (25/25 test verdi).

**Per continuare il frontend:** leggere  
`dev-workflow\...\Frontend-React\FASE-04-API-State-e-Dati\15-catalogo-prodotti-da-api-django.md`
