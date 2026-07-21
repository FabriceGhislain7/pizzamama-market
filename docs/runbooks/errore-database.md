# Runbook — Errore Database

## Sintomi

- Errori 500 su endpoint che leggono/scrivono dati
- Timeout query
- Migrazioni fallite al deploy
- Health check `/health/` restituisce `"database": "error"`

## Controlli

```powershell
cd backend
.\venv\Scripts\Activate.ps1
python manage.py migrate --plan
python manage.py showmigrations
python manage.py dbshell
```

## Azioni

1. Non eseguire migrazioni manuali non compresi
2. Verificare ultimo backup disponibile su Render
3. Se migrazione fallita: verificare il migration plan, fare rollback se necessario
4. Bloccare deploy automatici se CI/CD è attivo

## Escalation

Contattare Render Support se il servizio database managed non risponde.

## Query utili in Django shell

```python
from django.db import connection
connection.ensure_connection()
```
