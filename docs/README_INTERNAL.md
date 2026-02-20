
# PizzaMama Market – Documentazione Tecnica Interna

---

## Scopo di questo documento

Questo documento fornisce una **guida tecnica interna** al progetto PizzaMama Market.

Non è destinato alla presentazione pubblica del repository, ma è pensato per:

* sviluppatori che lavorano al progetto
* mantenere coerenza architetturale
* guidare l’evoluzione tecnica
* facilitare onboarding e manutenzione
* evitare deriva architetturale nel tempo

Il README principale rimane orientato alla **visione di prodotto**.
Questo documento è orientato alla **realizzazione tecnica**.

---

# Visione Tecnica del Progetto

PizzaMama Market è progettato come una piattaforma **API-first**.

Separazione chiara tra:

* logica di business
* livello applicativo
* interfacce di comunicazione (REST API)

L’obiettivo è costruire una base:

* semplice da comprendere
* solida architetturalmente
* facilmente estendibile
* sostenibile nel lungo periodo

---

# Architettura Concettuale

```
[ Client (Web / Mobile / External Services) ]
              |
           REST API
              |
        Django Applications
              |
        Domain Business Logic
              |
            Database
```

---

# Principi Architetturali

* separazione netta delle responsabilità
* backend indipendente dal frontend
* domini modulari e isolati
* API riutilizzabili
* evoluzione incrementale
* evitare over-engineering prematuro

---

# Struttura Backend

Struttura prevista:

```
backend/
├── manage.py
├── config/                   # Configurazione progetto Django
│   ├── __init__.py
│   ├── asgi.py
│   ├── wsgi.py
│   ├── urls.py
│   └── settings/
│       ├── __init__.py
│       ├── base.py
│       ├── dev.py
│       └── prod.py
│
├── apps/                     # Domini applicativi
│   ├── accounts/
│   │   ├── models.py
│   │   ├── admin.py
│   │   ├── services.py
│   │   ├── api/
│   │   ├── urls.py
│   │   └── migrations/
│   │
│   ├── products/
│   │   ├── models.py
│   │   ├── admin.py
│   │   ├── services.py
│   │   ├── api/
│   │   ├── urls.py
│   │   └── migrations/
│   │
│   └── orders/
│       ├── models.py
│       ├── admin.py
│       ├── services.py
│       ├── api/
│       ├── urls.py
│       └── migrations/
│
├── tests/
└── requirements/
```

Nota:
Il virtual environment non è parte dell’architettura e non viene documentato nella struttura.

---

# Settings Strategy

Il progetto utilizza una struttura settings modulare:

* `base.py` → configurazioni comuni
* `dev.py` → ambiente sviluppo
* `prod.py` → ambiente produzione

Questo consente:

* separazione ambienti
* configurazioni sicure in produzione
* integrazione semplice con Docker e CI/CD

---

# Custom User Model (Decisione Architetturale Fondamentale)

Il progetto utilizza **un Custom User Model fin dall’inizio**, estendendo `AbstractUser`.

Motivazione:

* flessibilità futura
* estensione campi utente
* integrazione sistemi loyalty
* evitare refactor critici in fase avanzata

Tutti i riferimenti all’utente devono utilizzare:

```python
settings.AUTH_USER_MODEL
```

Mai importare direttamente `User` da `django.contrib.auth`.

---

# Ruolo della Cartella `apps/`

Contiene tutto il codice applicativo Django:

* modelli (`models.Model`)
* logica di dominio (`services.py`)
* admin
* API (serializers, views, routers)
* URL routing
* migrazioni

Regola fondamentale:

> Ogni modello Django vive esclusivamente in `apps/`.

---

# Logica di Dominio

La logica di business è mantenuta:

* all’interno delle app
* oppure in moduli dedicati (`services.py`)

In questa fase:

* si privilegia la chiarezza
* si evita separazione eccessiva
* si mantiene coerenza per dominio

---

# API Design Strategy

Le API seguono un approccio:

* RESTful
* versionabile

Struttura prevista:

```
/api/v1/accounts/
/api/v1/products/
/api/v1/orders/
```

Motivazione:

* evoluzione futura senza breaking changes
* supporto multi-client

---

# Domini di Business

## Accounts

* utenti personalizzati
* profili
* indirizzi
* preferenze
* loyalty system

## Products

* catalogo pizze
* categorie
* ingredienti
* allergeni
* varianti
* pricing

## Orders

* carrello
* gestione ordini
* workflow stati
* storicizzazione

Domini previsti:

* Payments
* Delivery
* Reviews
* Analytics

---

# Database Strategy

* SQLite per sviluppo
* PostgreSQL per produzione
* migrazioni obbligatorie per ogni modifica ai modelli

Workflow:

```bash
python manage.py makemigrations
python manage.py migrate
```

---

# Regole di Import

Esempio corretto:

```python
from apps.products.models import Pizza
```

Regole:

* nessun import circolare
* nessuna duplicazione modelli
* import sempre espliciti
* modelli referenziati tramite `settings.AUTH_USER_MODEL`

---

# Sicurezza

Il progetto è predisposto per:

* autenticazione robusta
* sistema permessi DRF
* validazione input
* CSRF e CORS
* logging strutturato
* configurazione differenziata per ambiente

---

# Testing Strategy

Struttura pronta per:

* test unitari modelli
* test servizi
* test API
* test integrazione

Obiettivo:

* codice affidabile
* regressioni controllate
* refactoring sicuro

---

# Linee Guida di Sviluppo

* mantenere le app piccole e leggibili
* evitare complessità prematura
* refactor incrementali
* documentare decisioni architetturali
* privilegiare coerenza rispetto a soluzioni creative isolate

---

# Obiettivo di Lungo Periodo

PizzaMama Market è pensato come:

* base professionale backend Django
* progetto evolutivo
* riferimento architetturale reale
* piattaforma pronta per integrazioni future

---

# Nota Finale

Questo documento è ad uso interno.

Serve a garantire che il progetto rimanga:

* coerente
* leggibile
* sostenibile
* professionale
* scalabile

