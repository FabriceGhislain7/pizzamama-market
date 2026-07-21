# Database Operations — PizzaMama Market

## Ambienti

| Ambiente | Database | Scopo |
|---|---|---|
| local | SQLite (fallback automatico) | sviluppo senza Docker |
| local Docker | PostgreSQL 15 (container) | sviluppo con Docker |
| staging | PostgreSQL su Render (develop branch) | test pre-produzione |
| production | PostgreSQL su Render (main branch) | dati reali cliente |

## Regola principale

Non usare mai il database production per test locali.

## Avvio locale senza Docker (SQLite)

```powershell
cd backend
.\venv\Scripts\Activate.ps1
python manage.py migrate
python manage.py runserver
```

## Avvio locale con Docker (PostgreSQL)

```powershell
cd backend
docker compose up
```

## Migrazioni

```powershell
python manage.py makemigrations
python manage.py migrate
python manage.py showmigrations
python manage.py makemigrations --check --dry-run  # verifica migrazioni pendenti
```

## Verifica pre-deploy

```powershell
python manage.py check --deploy --settings=config.settings.prod
python manage.py migrate --plan
```
