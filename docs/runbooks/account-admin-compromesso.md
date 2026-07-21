# Runbook — Account Admin Compromesso

## Azioni immediate

1. Disabilitare l'account sospetto (`is_active = False`)
2. Ruotare la password dell'account admin
3. Verificare audit log per azioni recenti dell'account
4. Verificare modifiche a utenti, ordini, pagamenti e permessi nelle ultime 24-48h
5. Revocare tutti i token attivi (cancellare dalla blacklist è sufficiente se access token è scaduto)

## Comandi Django shell

```powershell
cd backend
.\venv\Scripts\Activate.ps1
python manage.py shell
```

```python
from django.contrib.auth import get_user_model
from apps.audit.models import AuditLog

User = get_user_model()

# Disabilitare account
user = User.objects.get(username="username_sospetto")
user.is_active = False
user.save()

# Controllare audit log
AuditLog.objects.filter(user=user).order_by("-created_at")[:50]
```

## Post incident

- Documentare timeline dell'incidente
- Documentare impatto (dati modificati, accessi non autorizzati)
- Documentare azioni correttive adottate
- Notificare le persone coinvolte se dati personali sono stati esposti (GDPR)
