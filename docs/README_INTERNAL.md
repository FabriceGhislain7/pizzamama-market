# PizzaMama Market – Documentazione Tecnica Interna

## Scopo di questo documento

Questo documento fornisce una **guida tecnica interna** al progetto **PizzaMama Market**.

Non è destinato alla presentazione pubblica del repository, ma è pensato per:

* sviluppatori che lavorano al progetto
* comprendere la struttura tecnica del backend
* mantenere coerenza architetturale nel tempo
* guidare l’evoluzione del codice
* facilitare onboarding e manutenzione

Il README principale rimane orientato alla **visione di prodotto**; questo documento è orientato alla **realizzazione tecnica**.

---

## Visione Tecnica del Progetto

PizzaMama Market è progettato come una **piattaforma API-first**, con una chiara separazione tra:

* logica di business
* livello applicativo
* interfacce di comunicazione (API)

L’obiettivo è costruire una base:

* semplice da comprendere
* solida dal punto di vista architetturale
* facilmente estendibile
* sostenibile nel lungo periodo

---

## Architettura Concettuale

```text
[ Client (Web / Mobile / External) ]
|
REST API
|
Django Applications
|
Business Domain Logic
|
Database
```

### Principi Architetturali

* separazione netta delle responsabilità
* backend indipendente dal frontend
* domini di business modulari
* API riutilizzabili
* codice orientato all’evoluzione

---

## Struttura Backend

```text
backend/
├── manage.py
├── pizzamama/              # Configurazione progetto Django
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── apps/                   # App Django (domini applicativi)
│   ├── accounts/
│   │   ├── models.py
│   │   ├── admin.py
│   │   ├── api/
│   │   ├── urls.py
│   │   └── migrations/
│   │
│   ├── products/
│   │   ├── models.py
│   │   ├── admin.py
│   │   ├── api/
│   │   ├── urls.py
│   │   └── migrations/
│   │
│   └── orders/
│       ├── models.py
│       ├── admin.py
│       ├── api/
│       ├── urls.py
│       └── migrations/
│
└── db.sqlite3
```

---

## Ruolo delle Cartelle

### `apps/`

Contiene **tutto il codice Django applicativo**:

* modelli (`models.py`)
* admin
* API (serializers, views, routers)
* URL routing
* migrazioni

Regola fondamentale:

> **Ogni modello Django (`models.Model`) vive esclusivamente in `apps/`.**

Questa scelta garantisce:

* compatibilità nativa con Django
* migrazioni chiare
* import semplici e coerenti
* riduzione della complessità

---

### Logica di Dominio

La logica di dominio (regole di business, calcoli, orchestrazioni) è mantenuta:

* **all’interno delle app**
* oppure in moduli dedicati (es. `services.py`)

In questa fase iniziale del progetto:

* si privilegia la **chiarezza** rispetto all’astrazione
* si evita una separazione eccessiva prematura

---

## Domini di Business Implementati

### Accounts

* utenti personalizzati
* profili
* indirizzi
* preferenze
* sistemi di fidelizzazione

### Products

* catalogo pizze
* categorie
* ingredienti
* allergeni
* pricing e varianti

### Orders

* carrello
* gestione ordini
* workflow di stato
* storicizzazione

Domini futuri previsti:

* Payments
* Delivery
* Reviews
* Analytics

---

## Regole di Import

Import **sempre espliciti e coerenti**.

### Esempio corretto

```python
from apps.products.models import Pizza
```

### Regole

* nessun import circolare
* nessuna duplicazione dei modelli
* modelli importati solo dalle rispettive app

---

## Database e Migrazioni

* SQLite utilizzato in sviluppo
* PostgreSQL previsto per produzione
* ogni modifica ai modelli richiede una migrazione

Workflow standard:

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## Sicurezza

Il progetto è predisposto per:

* autenticazione e autorizzazioni robuste
* validazione degli input
* protezione CSRF e CORS
* logging applicativo
* audit e best practice di sicurezza

---

## Testing

Struttura pronta per:

* test unitari sui modelli
* test delle API
* test di integrazione

L’obiettivo è mantenere:

* codice affidabile
* regressioni controllate
* facilità di refactoring

---

## Linee Guida di Sviluppo

* mantenere le app piccole e leggibili
* privilegiare la chiarezza rispetto all’over-engineering
* refactor incrementali
* documentare le decisioni architetturali rilevanti

---

## Obiettivo di Lungo Periodo

PizzaMama Market è pensato come:

* base professionale di backend Django
* progetto evolutivo
* riferimento architetturale per applicazioni reali
* piattaforma pronta per integrazioni future

---

## Nota Finale

Questo documento è **ad uso interno**.

Serve a garantire che il progetto rimanga:

* coerente
* leggibile
* sostenibile
* professionale

Il README principale resta orientato alla **presentazione del progetto**, non ai dettagli implementativi.

