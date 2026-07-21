# Installazione Locale — PizzaMama Market

## Prerequisiti

- Python 3.11+
- Node.js 22+ e npm 11+
- Git
- Docker Desktop (opzionale, per avvio con PostgreSQL)

## Backend (senza Docker — SQLite)

```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements/base.txt
copy .env.example .env
# Editare .env con DJANGO_SECRET_KEY
python manage.py migrate
python manage.py setup_roles
python manage.py runserver
```

API disponibile su: `http://127.0.0.1:8000/`  
Swagger UI: `http://127.0.0.1:8000/api/v1/docs/`

## Backend (con Docker — PostgreSQL)

```powershell
cd backend
copy .env.example .env
# Editare .env con DJANGO_SECRET_KEY e credenziali DB
docker compose up
```

## Frontend

```powershell
cd frontend
npm install
copy .env.example .env
# Editare .env con VITE_API_BASE_URL=http://127.0.0.1:8000
npm run dev
```

Frontend disponibile su: `http://localhost:5173/`
