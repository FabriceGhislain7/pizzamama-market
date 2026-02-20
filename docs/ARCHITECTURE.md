# PizzaMama Market – Architecture Reference

---

## Scopo del Documento

Questo documento descrive l’**architettura ufficiale** del progetto PizzaMama Market.

È il riferimento tecnico principale per:

* comprendere la struttura del sistema
* prendere decisioni coerenti nel tempo
* mantenere qualità architetturale
* supportare onboarding e crescita
* prevenire debito tecnico e derive strutturali

Le regole definite in questo documento **non sono opzionali**.

---

# Visione Architetturale

PizzaMama Market è una piattaforma e-commerce **API-first**, orientata al business e progettata per crescere in modo controllato.

Principi fondamentali:

* separazione netta delle responsabilità
* domini di business modulari
* backend riutilizzabile (web, mobile, integrazioni)
* frontend completamente indipendente
* evoluzione progressiva senza riscritture invasive

Il backend non è un monolite MVC tradizionale.
Django è utilizzato come **API provider e orchestratore applicativo**.

---

# Architettura ad Alto Livello

```
[ Client Web / Mobile / External Services ]
                  |
               REST API (v1)
                  |
        Application Layer (Django)
                  |
            Business Logic
                  |
              Persistence Layer
                  |
                Database
```

---

# Separazione dei Livelli

## 1️⃣ Presentation Layer

Responsabilità:

* interfaccia utente (React)
* gestione stato client
* chiamate API
* integrazioni esterne

Caratteristiche:

* completamente indipendente dal backend
* nessuna logica di business
* comunicazione esclusivamente via REST

---

## 2️⃣ Application Layer (Django)

Posizione:

```
backend/apps/
```

Responsabilità:

* esposizione API REST
* autenticazione e autorizzazione
* validazione input
* serializzazione
* routing
* permessi
* admin interface

⚠️ Questo layer non contiene logica di business complessa.

Views e serializer non devono contenere regole di dominio articolate.

---

## 3️⃣ Business Logic Layer

La logica di dominio è mantenuta:

* all’interno delle app
* oppure in moduli dedicati (`services.py`, `selectors.py`)

In questa fase:

* privilegiamo semplicità e chiarezza
* evitiamo separazioni premature
* evitiamo pattern complessi non necessari

La business logic:

* non vive nei serializer
* non vive negli admin
* non vive nei signals (salvo casi motivati)

---

## 4️⃣ Persistence Layer

Tecnologie:

* Django ORM
* PostgreSQL (target produzione)
* SQLite (solo sviluppo locale)

Responsabilità:

* persistenza dati
* migrazioni versionate
* integrità referenziale

Nessuna query SQL raw senza motivazione documentata.

---

# Struttura del Progetto (Target Ufficiale)

```
backend/
├── manage.py
│
├── config/                     # Configurazione Django
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
├── apps/
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
│   ├── orders/
│   │   ├── models.py
│   │   ├── admin.py
│   │   ├── services.py
│   │   ├── api/
│   │   ├── urls.py
│   │   └── migrations/
│   │
│   └── shared/
│       ├── permissions.py
│       ├── mixins.py
│       └── utils.py
│
├── tests/
└── requirements/
```

Il virtual environment non fa parte dell’architettura.

---

# Settings Strategy (Regola Ufficiale)

Il progetto utilizza settings modulari:

* `base.py` → configurazioni comuni
* `dev.py` → sviluppo locale
* `prod.py` → produzione

Non è ammesso utilizzare un unico `settings.py` monolitico.

---

# Custom User Model (Regola Obbligatoria)

Il progetto utilizza un **Custom User Model** estendendo `AbstractUser`.

Motivazioni:

* flessibilità futura
* estensione campi
* gestione loyalty
* compatibilità evolutiva

È obbligatorio:

```python
settings.AUTH_USER_MODEL
```

È vietato:

```python
from django.contrib.auth.models import User
```

---

# API Design Strategy

Le API sono:

* RESTful
* versionate

Formato:

```
/api/v1/accounts/
/api/v1/products/
/api/v1/orders/
```

Il versioning è obbligatorio per prevenire breaking changes futuri.

---

# Regole Fondamentali (Non Negoziabili)

## Regola 1 – Unica Fonte di Verità

Ogni concetto di business ha una sola definizione.

È vietato:

* duplicare modelli
* duplicare logica
* duplicare naming incoerente

---

## Regola 2 – Dipendenze Direzionali

Flusso corretto:

```
API / Admin
      ↓
  Services
      ↓
    Models
      ↓
   Database
```

È vietato:

* import circolari
* logica complessa nei serializer
* logica di dominio negli admin
* accoppiamento frontend-backend

---

## Regola 3 – Modelli Django

* tutti i `models.Model` vivono in `apps/*/models.py`
* nessun modello fuori da app registrate
* naming leggibile e coerente

---

## Regola 4 – API First

Ogni funzionalità deve essere esposta via API.

Il frontend:

* non accede al database
* non dipende da template Django
* non contiene regole di dominio

---

# Domini di Business

## Accounts

* utenti
* profili
* indirizzi
* autenticazione
* ruoli e permessi
* loyalty

---

## Products

* catalogo pizze
* categorie
* ingredienti
* allergeni
* pricing e varianti

---

## Orders

* carrello
* ordini
* stati ordine
* storico e tracciabilità

---

# Migrazioni e Database

Regole:

* ogni modifica ai modelli → migrazione obbligatoria
* nessuna modifica manuale al database
* nessuna manipolazione fuori ORM senza documentazione

Ambienti:

* sviluppo → SQLite
* produzione → PostgreSQL

---

# Sicurezza

* autenticazione token-based (DRF)
* permessi granulari
* validazione server-side
* logging eventi critici
* separazione configurazioni ambiente

---

# Estensioni Future Previste

* Payments
* Delivery
* Reviews
* Analytics
* Machine Learning

L’architettura è progettata per integrare nuovi domini senza rompere quelli esistenti.

---

# Documenti Correlati

* `README.md` → presentazione pubblica
* `docs/README_INTERNAL.md` → guida tecnica operativa
* `docs/ARCHITECTURE.md` → riferimento architetturale ufficiale

---

# Nota Finale

Se una modifica viola questo documento:

la modifica è da rifiutare.

Questo file rappresenta la **verità architetturale ufficiale** del progetto PizzaMama Market.
