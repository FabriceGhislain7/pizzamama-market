# 🍕 PizzaMama Market – Architecture Reference (Versione Allineata)

---

# Scopo del Documento

Questo documento definisce l’**architettura ufficiale e vincolante** del progetto PizzaMama Market.

Serve per:

* mantenere coerenza nel tempo
* prevenire derive architetturali
* supportare crescita controllata
* ridurre debito tecnico
* garantire evoluzione sicura

Le regole qui definite **non sono opzionali**.

---

# Visione Architetturale

PizzaMama Market è una piattaforma e-commerce **API-first**, progettata per:

* scalabilità progressiva
* separazione dominio/framework
* riutilizzo backend (web, mobile, integrazioni)
* sicurezza by design
* evoluzione senza riscritture invasive

Django è utilizzato come:

> API provider e orchestratore applicativo
> Non come monolite MVC tradizionale

---

# Principi Fondamentali

1. Separazione netta delle responsabilità
2. Dominio modulare
3. Zero Trust Security
4. API come unica interfaccia ufficiale
5. Evoluzione incrementale
6. Nessun over-engineering prematuro

---

# Filosofia di Sicurezza (Zero Trust)

Principi applicati:

* Default deny
* Permessi espliciti
* Nessuna fiducia implicita tra layer
* Nessuna esposizione non necessaria
* Configurazioni ambiente separate
* Preparazione a JWT (JSON Web Token)

Stato attuale autenticazione:

* SessionAuthentication attiva
* DEFAULT_PERMISSION_CLASSES = IsAuthenticated
* BasicAuthentication rimossa
* JWT previsto in evoluzione futura

---

# Naming Strategy Ufficiale

| Elemento               | Convenzione         |
| ---------------------- | ------------------- |
| URL pubblico           | kebab-case italiano |
| Variabili dominio      | snake_case italiano |
| Classi dominio         | PascalCase italiano |
| Framework Django/DRF   | inglese             |
| Modello autenticazione | `User` (inglese)    |

Separazione netta tra dominio e framework.

---

# Architettura ad Alto Livello

```
Client (Web / Mobile / External Services)
                ↓
            REST API v1
                ↓
       Application Layer (Django)
                ↓
         Business Logic Layer
                ↓
          Persistence Layer (ORM)
                ↓
              Database
```

---

# Separazione dei Layer

## 1️⃣ Presentation Layer (Frontend)

* React (target)
* Stato client
* Chiamate API
* Nessuna logica di business
* Nessun accesso diretto al database

---

## 2️⃣ Application Layer (Django)

Posizione:

```
backend/config/
backend/apps/
```

Responsabilità:

* Routing
* Autenticazione
* Permessi
* Serializzazione
* Validazione input
* Versioning API
* Admin interface

⚠ Vietato inserire business logic complessa in:

* serializer
* admin
* signals

---

## 3️⃣ Business Logic Layer

Vive dentro le app.

Può essere organizzata in:

```
services.py
selectors.py
```

Principi:

* Nessuna logica nei serializer
* Nessuna logica negli admin
* Nessuna logica complessa nei signals
* Nessuna duplicazione

---

## 4️⃣ Persistence Layer

Tecnologie:

* Django ORM
* SQLite (sviluppo)
* PostgreSQL (produzione target)

Regole:

* Migrazioni obbligatorie
* Nessuna modifica manuale al DB
* Nessuna query raw non documentata

---

# Struttura Ufficiale Attuale (Stato Reale)

```
backend/
├── manage.py
├── db.sqlite3
│
├── config/
│   ├── asgi.py
│   ├── wsgi.py
│   ├── urls.py
│   └── settings/
│       ├── base.py
│       ├── dev.py
│       └── prod.py
│
├── apps/
│   ├── core/
│   │   └── models.py      ← TimeStampedModel (abstract)
│   │
│   └── accounts/
│       ├── models.py      ← Custom User
│       ├── admin.py
│       ├── apps.py
│       └── migrations/
│
├── requirements/
└── venv/
```

---

# Modulo Core (Infrastruttura Dominio)

`apps/core/` contiene componenti riutilizzabili.

Esempio:

* TimeStampedModel (abstract)

Non è un dominio business.
Non è registrato in INSTALLED_APPS.

---

# Custom User Model (Regola Obbligatoria)

Il progetto utilizza un Custom User Model:

```python
class User(AbstractUser, TimeStampedModel)
```

È obbligatorio:

```python
AUTH_USER_MODEL = "accounts.User"
```

È vietato:

```python
from django.contrib.auth.models import User
```

Motivazioni:

* estensibilità futura
* compatibilità JWT
* gestione loyalty
* flessibilità RBAC

---

# API Strategy

Formato ufficiale:

```
/api/v1/accounts/
/api/v1/products/
/api/v1/orders/
```

Regole:

* Versioning obbligatorio
* Nessuna API non versionata
* Default permission: IsAuthenticated
* Endpoint pubblici esplicitamente dichiarati

---

# Regole Fondamentali

## Regola 1 — Unica Fonte di Verità

Ogni concetto di business ha una sola definizione.

Vietato:

* duplicare logica
* duplicare modelli
* naming incoerente

---

## Regola 2 — Dipendenze Direzionali

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

Vietato:

* import circolari
* logica nei serializer
* logica negli admin

---

## Regola 3 — API First

Ogni funzionalità deve essere esposta via API.

Frontend:

* non accede al DB
* non contiene regole dominio
* non dipende da template Django

---

# Domini Previsti

## Accounts

* utenti
* profili
* indirizzi
* autenticazione
* ruoli e permessi
* loyalty

## Products

* catalogo
* categorie
* varianti
* pricing

## Orders

* carrello
* ordini
* stati
* storico

---

# Struttura Target Evolutiva (Non Ancora Implementata)

```
apps/
├── accounts/
│   ├── models.py
│   ├── services.py
│   ├── api/
│   └── urls.py
│
├── products/
├── orders/
├── payments/
```

Questa è direzione futura, non stato attuale.

---

# Migrazioni

Regole:

* Ogni modifica ai modelli → makemigrations + migrate
* Migrazioni versionate
* Nessuna manipolazione manuale DB

---

# Database Strategy

Ambienti:

* Dev → SQLite
* Prod → PostgreSQL

Futuro:

* Redis
* Celery
* Docker

---

# Estensioni Future

* JWT Authentication
* RBAC avanzato
* Payments
* Delivery
* Reviews
* Analytics
* Observability

---

# Nota Finale

Se una modifica viola questo documento:

La modifica è da rifiutare.

Questo file rappresenta la **verità architetturale ufficiale** del progetto PizzaMama Market.


