# Runbook — Downtime Applicativo

## Sintomi

- API non risponde (timeout o 503)
- Frontend mostra errore generico
- Health check `GET /health/` non risponde

## Controlli immediati

1. Verificare dashboard Render (staging e production)
2. Verificare ultimi deploy e log del deploy
3. Verificare log applicativi in Render → Logs
4. Verificare stato database PostgreSQL su Render

## Comandi locali

```powershell
cd backend
.\venv\Scripts\Activate.ps1
python manage.py check
python manage.py showmigrations
```

## Azione di rollback

1. Andare su Render → Settings → Deploy → Manual Deploy
2. Selezionare commit precedente stabile
3. Fare deploy del commit precedente

## Comunicazione cliente

```
Ora inizio incidente: [HH:MM]
Impatto: [API non disponibile / rallentamenti]
Azione in corso: [investigazione / rollback]
Prossimo aggiornamento: [HH:MM]
```
