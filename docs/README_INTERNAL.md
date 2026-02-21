# 🍕 PizzaMama Market – Documentazione Tecnica Interna (Allineata)

---

# Scopo di questo documento

Questo documento rappresenta la **guida tecnica operativa interna** del progetto PizzaMama Market.

È destinato a:

* sviluppatori che lavorano al backend
* mantenere coerenza architetturale
* guidare evoluzione tecnica controllata
* prevenire debito tecnico
* facilitare onboarding

Il `README.md` principale rimane orientato al prodotto.
Questo documento è orientato all’implementazione tecnica reale.

---

# Visione Tecnica

PizzaMama Market è una piattaforma **API-first** costruita con:

* Python
* Django
* Django REST Framework
* SQLite (sviluppo)
* PostgreSQL (target produzione)

Separazione chiara tra:

* Application Layer (Django)
* Business Logic
* Persistence Layer
* Presentation Layer (frontend indipendente)

Il backend è progettato per essere:

* riutilizzabile
* modulare
* sicuro
* evolvibile

---

# Architettura Concettuale

```id="arch001"
Client (Web / Mobile / External Services)
                ↓
            REST API (v1)
                ↓
        Django Application Layer
                ↓
         Business Logic Layer
                ↓
           Django ORM
                ↓
             Database
```

---

# Principi Architetturali

* API-first
* separazione responsabilità
* dominio modulare
* zero trust mindset
* evoluzione incrementale
* evitare over-engineering
* configurazioni ambiente separate

---

# Struttura Backend (Stato Attuale Reale)

```id="struct001"
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
│   │   └── models.py        # TimeStampedModel (abstract)
│   │
│   └── accounts/
│       ├── models.py        # Custom User
│       ├── admin.py
│       ├── apps.py
│       └── migrations/
│
├── requirements/
└── venv/
```

Nota:
Il virtual environment non è parte dell’architettura logica.

---

# Settings Strategy

Il progetto utilizza settings modulari:

* `base.py` → configurazioni comuni
* `dev.py` → sviluppo
* `prod.py` → produzione

Regole:

* Nessun settings monolitico
* Nessuna credenziale hardcoded
* Separazione ambienti obbligatoria
* Preparazione a Docker / CI/CD

---

# Django REST Framework

Configurazione attuale:

```python
DEFAULT_PERMISSION_CLASSES = [
    IsAuthenticated
]

DEFAULT_AUTHENTICATION_CLASSES = [
    SessionAuthentication
]
```

Stato sicurezza attuale:

* Tutte le API protette di default
* BasicAuthentication rimossa
* Autenticazione via sessione
* JWT previsto come evoluzione futura

---

# Naming Strategy

Regole ufficiali:

| Elemento             | Convenzione         |
| -------------------- | ------------------- |
| URL pubblico         | kebab-case italiano |
| Variabili dominio    | snake_case italiano |
| Classi dominio       | PascalCase italiano |
| Framework Django/DRF | inglese             |

Separazione netta tra dominio e framework.

---

# Modulo `core`

La cartella `apps/core/` contiene componenti infrastrutturali condivisi.

Attualmente include:

* `TimeStampedModel` (abstract)

Non rappresenta un dominio business.

Non deve contenere modelli concreti.

---

# Custom User Model

Il progetto utilizza un Custom User Model fin dall’inizio.

Implementazione:

```python
class User(AbstractUser, TimeStampedModel)
```

Configurazione obbligatoria:

```python
AUTH_USER_MODEL = "accounts.User"
```

Regole:

* Mai importare `User` da `django.contrib.auth.models`
* Usare sempre `settings.AUTH_USER_MODEL`
* Nessuna relazione diretta verso `auth.User`

---

# Ruolo della Cartella `apps/`

Contiene tutto il codice applicativo.

Ogni app include:

* modelli
* admin
* logica di dominio (in futuro services.py)
* API (in futuro api/)
* migrazioni

Regola fondamentale:

> Nessun modello Django fuori da `apps/`.

---

# Logica di Dominio

Attualmente minima (fase foundation).

Direzione futura:

* `services.py`
* separazione read/write (se necessario)
* nessuna logica complessa in serializer o admin

---

# API Strategy

Formato ufficiale:

```id="api001"
/api/v1/accounts/
/api/v1/products/
/api/v1/orders/
```

Regole:

* Versioning obbligatorio
* Nessuna API non versionata
* Default permission: IsAuthenticated

---

# Database Strategy

Ambienti:

* Dev → SQLite
* Prod → PostgreSQL

Regole:

* Ogni modifica ai modelli → migrazione obbligatoria
* Nessuna modifica manuale al database
* Workflow standard:

```bash
python manage.py makemigrations
python manage.py migrate
```

---

# Sicurezza

Principi attuali:

* Default deny
* IsAuthenticated globale
* Validazione server-side
* SessionAuthentication attiva
* Preparazione a JWT
* Settings separati per ambiente

Futuro:

* JWT
* RBAC avanzato
* Logging strutturato
* Audit trail

---

# Testing Strategy

Struttura pronta per:

* test modelli
* test servizi
* test API
* test integrazione

Obiettivo:

* regressioni controllate
* refactor sicuri
* affidabilità crescente

---

# Linee Guida di Sviluppo

* mantenere app piccole
* evitare logica nei serializer
* evitare logica negli admin
* evitare import circolari
* refactor incrementali
* ogni modifica deve avere motivazione architetturale

---

# Stato Attuale del Progetto

Foundation completata:

* settings modulari
* DRF configurato
* Custom User attivo
* BASE_DIR corretto
* migrazioni pulite
* admin funzionante
* API versionata `/api/v1/`
* sicurezza default deny

---

# Obiettivo Evolutivo

Prossimi domini:

* Products
* Orders
* Payments
* Delivery
* Reviews

Il sistema è progettato per crescere senza riscritture invasive.

---

# Nota Finale

Questo documento deve riflettere lo stato reale del progetto.

Se codice e documento divergono:

* va aggiornato il documento
* oppure va corretto il codice

La coerenza è obbligatoria.

---

Se vuoi, nel prossimo messaggio posso:

* Allineare anche README pubblico
* Creare checklist automatica di validazione architetturale
* Preparare template ADR (Architecture Decision Record)
* Oppure fare audit completo di tutto il progetto fino a ora
Perfetto.
Ti fornisco la **versione aggiornata, coerente con lo stato reale attuale**, allineata con:

* Custom User già implementato
* Modulo `core` ufficiale
* Settings modulari attivi
* DRF configurato
* SessionAuthentication attiva
* IsAuthenticated default
* Naming dominio italiano
* Zero Trust esplicitato
* Nessuna dichiarazione non ancora implementata

Questa versione è sincronizzata con l’Architecture Reference che abbiamo appena corretto.

---

# 🍕 PizzaMama Market – Documentazione Tecnica Interna (Allineata)

---

# Scopo di questo documento

Questo documento rappresenta la **guida tecnica operativa interna** del progetto PizzaMama Market.

È destinato a:

* sviluppatori che lavorano al backend
* mantenere coerenza architetturale
* guidare evoluzione tecnica controllata
* prevenire debito tecnico
* facilitare onboarding

Il `README.md` principale rimane orientato al prodotto.
Questo documento è orientato all’implementazione tecnica reale.

---

# Visione Tecnica

PizzaMama Market è una piattaforma **API-first** costruita con:

* Python
* Django
* Django REST Framework
* SQLite (sviluppo)
* PostgreSQL (target produzione)

Separazione chiara tra:

* Application Layer (Django)
* Business Logic
* Persistence Layer
* Presentation Layer (frontend indipendente)

Il backend è progettato per essere:

* riutilizzabile
* modulare
* sicuro
* evolvibile

---

# Architettura Concettuale

```id="arch001"
Client (Web / Mobile / External Services)
                ↓
            REST API (v1)
                ↓
        Django Application Layer
                ↓
         Business Logic Layer
                ↓
           Django ORM
                ↓
             Database
```

---

# Principi Architetturali

* API-first
* separazione responsabilità
* dominio modulare
* zero trust mindset
* evoluzione incrementale
* evitare over-engineering
* configurazioni ambiente separate

---

# Struttura Backend (Stato Attuale Reale)

```id="struct001"
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
│   │   └── models.py        # TimeStampedModel (abstract)
│   │
│   └── accounts/
│       ├── models.py        # Custom User
│       ├── admin.py
│       ├── apps.py
│       └── migrations/
│
├── requirements/
└── venv/
```

Nota:
Il virtual environment non è parte dell’architettura logica.

---

# Settings Strategy

Il progetto utilizza settings modulari:

* `base.py` → configurazioni comuni
* `dev.py` → sviluppo
* `prod.py` → produzione

Regole:

* Nessun settings monolitico
* Nessuna credenziale hardcoded
* Separazione ambienti obbligatoria
* Preparazione a Docker / CI/CD

---

# Django REST Framework

Configurazione attuale:

```python
DEFAULT_PERMISSION_CLASSES = [
    IsAuthenticated
]

DEFAULT_AUTHENTICATION_CLASSES = [
    SessionAuthentication
]
```

Stato sicurezza attuale:

* Tutte le API protette di default
* BasicAuthentication rimossa
* Autenticazione via sessione
* JWT previsto come evoluzione futura

---

# Naming Strategy

Regole ufficiali:

| Elemento             | Convenzione         |
| -------------------- | ------------------- |
| URL pubblico         | kebab-case italiano |
| Variabili dominio    | snake_case italiano |
| Classi dominio       | PascalCase italiano |
| Framework Django/DRF | inglese             |

Separazione netta tra dominio e framework.

---

# Modulo `core`

La cartella `apps/core/` contiene componenti infrastrutturali condivisi.

Attualmente include:

* `TimeStampedModel` (abstract)

Non rappresenta un dominio business.

Non deve contenere modelli concreti.

---

# Custom User Model

Il progetto utilizza un Custom User Model fin dall’inizio.

Implementazione:

```python
class User(AbstractUser, TimeStampedModel)
```

Configurazione obbligatoria:

```python
AUTH_USER_MODEL = "accounts.User"
```

Regole:

* Mai importare `User` da `django.contrib.auth.models`
* Usare sempre `settings.AUTH_USER_MODEL`
* Nessuna relazione diretta verso `auth.User`

---

# Ruolo della Cartella `apps/`

Contiene tutto il codice applicativo.

Ogni app include:

* modelli
* admin
* logica di dominio (in futuro services.py)
* API (in futuro api/)
* migrazioni

Regola fondamentale:

> Nessun modello Django fuori da `apps/`.

---

# Logica di Dominio

Attualmente minima (fase foundation).

Direzione futura:

* `services.py`
* separazione read/write (se necessario)
* nessuna logica complessa in serializer o admin

---

# API Strategy

Formato ufficiale:

```id="api001"
/api/v1/accounts/
/api/v1/products/
/api/v1/orders/
```

Regole:

* Versioning obbligatorio
* Nessuna API non versionata
* Default permission: IsAuthenticated

---

# Database Strategy

Ambienti:

* Dev → SQLite
* Prod → PostgreSQL

Regole:

* Ogni modifica ai modelli → migrazione obbligatoria
* Nessuna modifica manuale al database
* Workflow standard:

```bash
python manage.py makemigrations
python manage.py migrate
```

---

# Sicurezza

Principi attuali:

* Default deny
* IsAuthenticated globale
* Validazione server-side
* SessionAuthentication attiva
* Preparazione a JWT
* Settings separati per ambiente

Futuro:

* JWT
* RBAC avanzato
* Logging strutturato
* Audit trail

---

# Testing Strategy

Struttura pronta per:

* test modelli
* test servizi
* test API
* test integrazione

Obiettivo:

* regressioni controllate
* refactor sicuri
* affidabilità crescente

---

# Linee Guida di Sviluppo

* mantenere app piccole
* evitare logica nei serializer
* evitare logica negli admin
* evitare import circolari
* refactor incrementali
* ogni modifica deve avere motivazione architetturale

---

# Stato Attuale del Progetto

Foundation completata:

* settings modulari
* DRF configurato
* Custom User attivo
* BASE_DIR corretto
* migrazioni pulite
* admin funzionante
* API versionata `/api/v1/`
* sicurezza default deny

---

# Obiettivo Evolutivo

Prossimi domini:

* Products
* Orders
* Payments
* Delivery
* Reviews

Il sistema è progettato per crescere senza riscritture invasive.

---

# Nota Finale

Questo documento deve riflettere lo stato reale del progetto.

Se codice e documento divergono:

* va aggiornato il documento
* oppure va corretto il codice

La coerenza è obbligatoria.

---

Se vuoi, nel prossimo messaggio posso:

* Allineare anche README pubblico
* Creare checklist automatica di validazione architetturale
* Preparare template ADR (Architecture Decision Record)
* Oppure fare audit completo di tutto il progetto fino a ora
Perfetto.
Ti fornisco la **versione aggiornata, coerente con lo stato reale attuale**, allineata con:

* Custom User già implementato
* Modulo `core` ufficiale
* Settings modulari attivi
* DRF configurato
* SessionAuthentication attiva
* IsAuthenticated default
* Naming dominio italiano
* Zero Trust esplicitato
* Nessuna dichiarazione non ancora implementata

Questa versione è sincronizzata con l’Architecture Reference che abbiamo appena corretto.

---

# 🍕 PizzaMama Market – Documentazione Tecnica Interna (Allineata)

---

# Scopo di questo documento

Questo documento rappresenta la **guida tecnica operativa interna** del progetto PizzaMama Market.

È destinato a:

* sviluppatori che lavorano al backend
* mantenere coerenza architetturale
* guidare evoluzione tecnica controllata
* prevenire debito tecnico
* facilitare onboarding

Il `README.md` principale rimane orientato al prodotto.
Questo documento è orientato all’implementazione tecnica reale.

---

# Visione Tecnica

PizzaMama Market è una piattaforma **API-first** costruita con:

* Python
* Django
* Django REST Framework
* SQLite (sviluppo)
* PostgreSQL (target produzione)

Separazione chiara tra:

* Application Layer (Django)
* Business Logic
* Persistence Layer
* Presentation Layer (frontend indipendente)

Il backend è progettato per essere:

* riutilizzabile
* modulare
* sicuro
* evolvibile

---

# Architettura Concettuale

```id="arch001"
Client (Web / Mobile / External Services)
                ↓
            REST API (v1)
                ↓
        Django Application Layer
                ↓
         Business Logic Layer
                ↓
           Django ORM
                ↓
             Database
```

---

# Principi Architetturali

* API-first
* separazione responsabilità
* dominio modulare
* zero trust mindset
* evoluzione incrementale
* evitare over-engineering
* configurazioni ambiente separate

---

# Struttura Backend (Stato Attuale Reale)

```id="struct001"
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
│   │   └── models.py        # TimeStampedModel (abstract)
│   │
│   └── accounts/
│       ├── models.py        # Custom User
│       ├── admin.py
│       ├── apps.py
│       └── migrations/
│
├── requirements/
└── venv/
```

Nota:
Il virtual environment non è parte dell’architettura logica.

---

# Settings Strategy

Il progetto utilizza settings modulari:

* `base.py` → configurazioni comuni
* `dev.py` → sviluppo
* `prod.py` → produzione

Regole:

* Nessun settings monolitico
* Nessuna credenziale hardcoded
* Separazione ambienti obbligatoria
* Preparazione a Docker / CI/CD

---

# Django REST Framework

Configurazione attuale:

```python
DEFAULT_PERMISSION_CLASSES = [
    IsAuthenticated
]

DEFAULT_AUTHENTICATION_CLASSES = [
    SessionAuthentication
]
```

Stato sicurezza attuale:

* Tutte le API protette di default
* BasicAuthentication rimossa
* Autenticazione via sessione
* JWT previsto come evoluzione futura

---

# Naming Strategy

Regole ufficiali:

| Elemento             | Convenzione         |
| -------------------- | ------------------- |
| URL pubblico         | kebab-case italiano |
| Variabili dominio    | snake_case italiano |
| Classi dominio       | PascalCase italiano |
| Framework Django/DRF | inglese             |

Separazione netta tra dominio e framework.

---

# Modulo `core`

La cartella `apps/core/` contiene componenti infrastrutturali condivisi.

Attualmente include:

* `TimeStampedModel` (abstract)

Non rappresenta un dominio business.

Non deve contenere modelli concreti.

---

# Custom User Model

Il progetto utilizza un Custom User Model fin dall’inizio.

Implementazione:

```python
class User(AbstractUser, TimeStampedModel)
```

Configurazione obbligatoria:

```python
AUTH_USER_MODEL = "accounts.User"
```

Regole:

* Mai importare `User` da `django.contrib.auth.models`
* Usare sempre `settings.AUTH_USER_MODEL`
* Nessuna relazione diretta verso `auth.User`

---

# Ruolo della Cartella `apps/`

Contiene tutto il codice applicativo.

Ogni app include:

* modelli
* admin
* logica di dominio (in futuro services.py)
* API (in futuro api/)
* migrazioni

Regola fondamentale:

> Nessun modello Django fuori da `apps/`.

---

# Logica di Dominio

Attualmente minima (fase foundation).

Direzione futura:

* `services.py`
* separazione read/write (se necessario)
* nessuna logica complessa in serializer o admin

---

# API Strategy

Formato ufficiale:

```id="api001"
/api/v1/accounts/
/api/v1/products/
/api/v1/orders/
```

Regole:

* Versioning obbligatorio
* Nessuna API non versionata
* Default permission: IsAuthenticated

---

# Database Strategy

Ambienti:

* Dev → SQLite
* Prod → PostgreSQL

Regole:

* Ogni modifica ai modelli → migrazione obbligatoria
* Nessuna modifica manuale al database
* Workflow standard:

```bash
python manage.py makemigrations
python manage.py migrate
```

---

# Sicurezza

Principi attuali:

* Default deny
* IsAuthenticated globale
* Validazione server-side
* SessionAuthentication attiva
* Preparazione a JWT
* Settings separati per ambiente

Futuro:

* JWT
* RBAC avanzato
* Logging strutturato
* Audit trail

---

# Testing Strategy

Struttura pronta per:

* test modelli
* test servizi
* test API
* test integrazione

Obiettivo:

* regressioni controllate
* refactor sicuri
* affidabilità crescente

---

# Linee Guida di Sviluppo

* mantenere app piccole
* evitare logica nei serializer
* evitare logica negli admin
* evitare import circolari
* refactor incrementali
* ogni modifica deve avere motivazione architetturale

---

# Stato Attuale del Progetto

Foundation completata:

* settings modulari
* DRF configurato
* Custom User attivo
* BASE_DIR corretto
* migrazioni pulite
* admin funzionante
* API versionata `/api/v1/`
* sicurezza default deny

---

# Obiettivo Evolutivo

Prossimi domini:

* Products
* Orders
* Payments
* Delivery
* Reviews

Il sistema è progettato per crescere senza riscritture invasive.

---

# Nota Finale

Questo documento deve riflettere lo stato reale del progetto.

Se codice e documento divergono:

* va aggiornato il documento
* oppure va corretto il codice

La coerenza è obbligatoria.

