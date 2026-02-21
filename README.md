![PizzaMama Enterprise](https://images.openai.com/static-rsc-3/7InvxiSJU5gtaEC6KE8vIb0j_MsLbFGBemTCdZt7KBxG6MkkSdI5HbhHY3SK4a1qopU84K51JamSW3JKj8hDjF-Aau_sS1eKzOegrjC--yo?purpose=fullsize\&v=1)

# PizzaMama Market 🍕

## Piattaforma E-commerce Professionale per Pizzerie Moderne

**PizzaMama Market** è una piattaforma e-commerce moderna e scalabile, progettata per pizzerie e attività di ristorazione che desiderano un sistema solido, estendibile e orientato al business.

Il progetto è sviluppato con **Django (backend API)** e **React (frontend)** e segue principi di **architettura professionale**, **manutenibilità** e **crescita progressiva**.

Non si tratta di un semplice progetto dimostrativo, ma di una **base reale pronta per evolvere verso ambienti di produzione**.

---

## Obiettivi del Progetto

PizzaMama Market nasce con l’obiettivo di:

* modellare correttamente domini di business reali
* separare in modo chiaro frontend, backend e logica di dominio
* ridurre il debito tecnico nel tempo
* supportare nuove funzionalità senza riscritture invasive
* fungere da base per applicazioni web, mobile e integrazioni esterne

---

## Visione Architetturale

L’applicazione adotta un approccio **API-first**, con una netta separazione tra:

* logica di business
* livello applicativo
* interfacce (API e UI)

Principi architetturali adottati:

* separazione completa frontend / backend
* backend indipendente dal rendering
* domini modulari e ben isolati
* progettazione orientata alla scalabilità
* codice pensato per evoluzione continua

---

## Stack Tecnologico

### Backend (API)

* Python 3.10+
* Django 5.x
* Django REST Framework
* SQLite (ambiente di sviluppo)
* PostgreSQL (ambiente di produzione – target)
* Redis (previsto)
* Celery (previsto)
* JWT (previsto)

### Frontend (Web App)

* React
* JavaScript / TypeScript
* Consumo API REST
* CSS modulare e scalabile

### Tooling & DevOps

* Docker (previsto)
* Gestione variabili d’ambiente
* Git
* Progetto pronto per pipeline CI/CD

---

## Struttura Generale del Progetto 📁

```text
pizzamama-market/
├── backend/
│   ├── manage.py
│   ├── config/                # Configurazione progetto Django
│   ├── apps/                  # App Django (accounts, ...)
│   ├── requirements/
│   └── db.sqlite3 (dev)
│
├── frontend/
│   ├── src/
│   ├── public/
│   └── package.json
│
├── docs/
│
├── docker-compose.yml (previsto)
└── README.md
```

La documentazione tecnica dettagliata e le decisioni architetturali sono mantenute nella cartella **docs**, separata dal README principale.

Il virtual environment non fa parte dell’architettura.

---

## Domini di Business (Backend)

### Accounts

* gestione utenti personalizzati (Custom User Model)
* profili e preferenze
* indirizzi di consegna
* sistemi di fidelizzazione (previsto)

### Products (previsto)

* catalogo pizze
* categorie
* ingredienti
* allergeni
* pricing e varianti

### Orders (previsto)

* carrello
* gestione ordini
* workflow di stato
* storicizzazione e tracciabilità

I domini **Payments**, **Delivery**, **Reviews** e **Analytics** sono previsti come estensioni future.

---

## Sicurezza e Qualità

* autenticazione via SessionAuthentication (attuale)
* permessi DRF con IsAuthenticated di default
* validazione server-side
* protezione CSRF e CORS
* configurazioni ambiente separate
* predisposizione per JWT e RBAC avanzato

---

## Setup di Sviluppo

### Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements/base.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Backend disponibile su:

```
http://127.0.0.1:8000/
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend disponibile su:

```
http://localhost:5173/
```

---

## Comunicazione Frontend ↔ Backend

* comunicazione esclusivamente tramite API REST
* backend riutilizzabile per web, mobile e servizi esterni
* separazione completa tra presentazione e logica di business

---

## Testing e Manutenibilità

* struttura pronta per test unitari
* test delle API
* codice organizzato per refactoring continuo
* migrazioni versionate

---

## Stato del Progetto

* settings modulari attivi
* Custom User Model implementato
* DRF configurato
* API versionata `/api/v1/`
* base architetturale stabilizzata
* foundation pronta per crescita progressiva

---

## Checklist Architetturale

### Fondamenta

* [ ] Settings modulari attivi (base/dev/prod)
* [ ] Custom User Model configurato
* [ ] AUTH_USER_MODEL impostato correttamente
* [ ] Nessun uso diretto di auth.User
* [ ] BASE_DIR corretto

### API

* [ ] Versioning `/api/v1/`
* [ ] IsAuthenticated come default
* [ ] Nessuna API esposta involontariamente
* [ ] Nessuna logica di dominio nei serializer

### Database

* [ ] Ogni modifica ai modelli → makemigrations + migrate
* [ ] Nessuna modifica manuale al database
* [ ] Migrazioni coerenti

### Sicurezza

* [ ] Nessuna credenziale hardcoded
* [ ] DEBUG disattivabile in produzione
* [ ] BasicAuthentication rimossa
* [ ] Separazione ambienti corretta

### Architettura

* [ ] Nessun import circolare
* [ ] Nessuna duplicazione logica
* [ ] Logica di business fuori da admin e serializer
* [ ] Coerenza con docs/ARCHITECTURE.md

---

## Note Finali

PizzaMama Market è un progetto orientato a:

* apprendimento avanzato
* architettura backend professionale
* sviluppo moderno di applicazioni web
* contesti reali di business

È una base progettuale pensata per evolvere nel tempo, mantenendo chiarezza, qualità e sostenibilità.


