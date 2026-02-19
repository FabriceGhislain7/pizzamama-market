![PizzaMama Enterprise](https://images.openai.com/static-rsc-3/7InvxiSJU5gtaEC6KE8vIb0j_MsLbFGBemTCdZt7KBxG6MkkSdI5HbhHY3SK4a1qopU84K51JamSW3JKj8hDjF-Aau_sS1eKzOegrjC--yo?purpose=fullsize&v=1)

# PizzaMama Market 🍕

## Piattaforma E-commerce Professionale per Pizzerie Moderne

**PizzaMama Market** è una piattaforma e-commerce moderna e scalabile, progettata per pizzerie e attività di ristorazione che desiderano un sistema solido, estendibile e orientato al business.

Il progetto è sviluppato con **Django (backend API)** e **React (frontend)** e segue principi di **architettura professionale**, **manutenibilità** e **crescita progressiva**.

Non si tratta di un semplice progetto dimostrativo, ma di una **base reale pronta per evolvere verso ambienti di produzione**.

---

## Obiettivi del Progetto

PizzaMama Market nasce con l’obiettivo di:

- modellare correttamente domini di business reali
- separare in modo chiaro frontend, backend e logica di dominio
- ridurre il debito tecnico nel tempo
- supportare nuove funzionalità senza riscritture invasive
- fungere da base per applicazioni web, mobile e integrazioni esterne

---

## Visione Architetturale

L’applicazione adotta un approccio **API-first**, con una netta separazione tra:

- logica di business
- livello applicativo
- interfacce (API e UI)

Principi architetturali adottati:

- separazione completa frontend / backend
- backend indipendente dal rendering
- domini modulari e ben isolati
- progettazione orientata alla scalabilità
- codice pensato per evoluzione continua

---

## Stack Tecnologico

### Backend (API)

- Python 3.10+
- Django 5.x
- Django REST Framework
- SQLite (ambiente di sviluppo)
- PostgreSQL (ambiente di produzione)
- Redis (cache e sessioni – previsto)
- Celery (task asincroni – previsto)

### Frontend (Web App)

- React
- JavaScript / TypeScript
- Consumo API REST
- CSS modulare e scalabile

### Tooling & DevOps

- Docker e Docker Compose
- Gestione variabili d’ambiente
- Git
- Progetto pronto per pipeline CI/CD

---

## Struttura Generale del Progetto 📁

```text
pizzamama-market/
├── backend/                  # Backend Django (API)
│   ├── pizzamama/            # Configurazione progetto
│   ├── apps/                 # App Django (accounts, products, orders, ...)
│   ├── manage.py
│   └── db.sqlite3
│
├── frontend/                 # Frontend React (in sviluppo)
│   ├── src/
│   ├── public/
│   └── package.json
│
├── docs/                     # Documentazione tecnica
│
├── docker-compose.yml
├── .env.example
└── README.md
````

La documentazione tecnica dettagliata e le decisioni architetturali sono mantenute nella cartella **docs**, separata dal README principale.

---

## Domini di Business (Backend)

### Accounts

* gestione utenti personalizzati
* profili e preferenze
* indirizzi di consegna
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
* storicizzazione e tracciabilità

I domini **Payments**, **Delivery**, **Reviews** e **Analytics** sono previsti in architettura come estensioni future.

---

## Sicurezza e Qualità

* autenticazione e autorizzazioni robuste
* validazione degli input
* protezione CSRF e CORS
* logging applicativo
* struttura pronta per audit e best practice di sicurezza

---

## Setup di Sviluppo

### Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements.txt
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

## Analytics e Business Intelligence (Roadmap)

Il progetto è progettato per supportare:

* analisi del comportamento utenti
* metriche su ordini e fatturato
* performance dei prodotti
* customer retention e insight operativi

---

## Machine Learning – Customer Satisfaction (Roadmap)

Sono previste integrazioni future per:

* analisi del sentiment delle recensioni
* customer satisfaction score
* previsione del churn
* supporto alle decisioni di marketing e operations

---

## Testing e Manutenibilità

* struttura pronta per test unitari
* test delle API
* codice organizzato per refactoring continuo
* orientamento alla manutenzione di lungo periodo

---

## Stato del Progetto

* architettura definita
* domini di business chiari e modulari
* backend API solido
* frontend in sviluppo
* base pronta per crescita progressiva

---

## Note Finali

PizzaMama Market è un progetto orientato a:

* apprendimento avanzato
* architettura backend professionale
* sviluppo moderno di applicazioni web
* contesti reali di business

È una base progettuale pensata per evolvere nel tempo, mantenendo chiarezza, qualità e sostenibilità.
