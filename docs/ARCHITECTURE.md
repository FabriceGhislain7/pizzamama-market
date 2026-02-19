# PizzaMama Market – Architecture Reference

## Scopo del Documento

Questo documento descrive l’**architettura ufficiale** del progetto **PizzaMama Market**.

È il riferimento tecnico principale per:

* comprendere la struttura del sistema
* prendere decisioni coerenti nel tempo
* mantenere qualità architetturale
* supportare onboarding, crescita ed estensioni
* evitare debito tecnico e derive strutturali

Le regole definite in questo documento **non sono opzionali**.

---

## Visione Architetturale

PizzaMama Market è progettato come una **piattaforma e-commerce API-first**, orientata al business e pronta alla scalabilità.

Principi fondamentali:

* separazione netta delle responsabilità
* domini di business chiari e modulari
* backend riutilizzabile (web, mobile, integrazioni)
* frontend completamente indipendente
* crescita progressiva senza riscritture

---

## Architettura ad Alto Livello

```text
[ Client Web / Mobile / External ]
|
REST API
|
Django Application Layer
|
Business Logic
|
Database
```

Il backend **non renderizza HTML come responsabilità primaria**.
Django viene utilizzato come **API provider e orchestratore**, non come monolite MVC tradizionale.

---

## Separazione dei Livelli

### 1. Presentation Layer

**Responsabilità**

* interfaccia utente (React)
* UX e gestione stato client
* chiamate API
* integrazioni esterne

**Caratteristiche**

* completamente indipendente dal backend
* nessuna logica di business
* comunicazione esclusivamente via API REST

---

### 2. Application Layer (Django)

**Posizione**

```text
backend/apps/
```

**Responsabilità**

* esposizione API REST
* autenticazione e autorizzazione
* validazione input
* serializzazione dati
* admin interface
* routing e permessi

⚠️ Questo layer **non contiene logica di business complessa**.

---

### 3. Business Logic Layer

La logica di business è mantenuta:

* all’interno delle app Django
* oppure in moduli dedicati (`services.py`, `selectors.py`)

In questa fase del progetto:

* si privilegia **chiarezza e semplicità**
* si evita una separazione eccessiva prematura
* il dominio evolve insieme all’applicazione

---

### 4. Persistence Layer

**Tecnologie**

* Django ORM
* SQLite (sviluppo)
* PostgreSQL (produzione)

**Responsabilità**

* persistenza dei dati
* migrazioni
* integrità referenziale

---

## Struttura del Progetto (Target)

```text
backend/
├── manage.py
│
├── pizzamama/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── apps/
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
│   ├── orders/
│   │   ├── models.py
│   │   ├── admin.py
│   │   ├── api/
│   │   ├── urls.py
│   │   └── migrations/
│   │
│   └── shared/
│       ├── permissions.py
│       ├── mixins.py
│       └── utils.py
│
└── db.sqlite3
```

---

## Regole Fondamentali (Non Negoziabili)

### Regola 1 – Unica Fonte di Verità

Ogni concetto di business deve avere **una sola definizione**.

È vietato:

* duplicare modelli
* duplicare logica
* duplicare naming

---

### Regola 2 – Dipendenze Chiare

```text
API / Views / Admin
        ↓
      Models
        ↓
     Database
```

È vietato:

* import circolari
* logica di business negli admin o serializer
* accoppiamento stretto tra frontend e backend

---

### Regola 3 – Modelli Django

* tutti i `models.Model` vivono **esclusivamente in `apps/*/models.py`**
* nessun modello Django fuori dalle app registrate
* naming coerente e leggibile

---

### Regola 4 – API First

Ogni funzionalità deve essere accessibile via API.

Il frontend:

* non accede direttamente al database
* non dipende da template Django
* non contiene logica di business

---

## Gestione dei Domini

### Accounts

Responsabilità:

* utenti
* profili
* indirizzi
* autenticazione
* ruoli e permessi

---

### Products

Responsabilità:

* catalogo pizze
* categorie
* ingredienti
* allergeni
* pricing e varianti

---

### Orders

Responsabilità:

* carrello
* ordini
* stati ordine
* storico e tracciabilità

---

## Migrazioni e Database

* ogni modifica ai modelli → migrazione obbligatoria
* nessuna modifica manuale al database
* versionamento coerente

Ambienti:

* sviluppo → SQLite
* produzione → PostgreSQL

---

## Sicurezza

* autenticazione token-based
* permessi granulari
* validazione server-side
* logging eventi critici
* struttura pronta per audit

---

## Estensioni Future Previste

* Payments
* Delivery
* Reviews
* Analytics
* Machine Learning

L’architettura è progettata per integrare nuovi domini **senza rompere quelli esistenti**.

---

## Documenti Correlati

* `README.md` → presentazione pubblica
* `docs/README_INTERNAL.md` → guida tecnica operativa
* `docs/ARCHITECTURE.md` → **riferimento architetturale ufficiale**

---

## Nota Finale

Se una modifica **viola questo documento**,
la modifica è **da rifiutare**, non da adattare.

Questo file rappresenta la **verità architetturale** del progetto **PizzaMama Market**.

