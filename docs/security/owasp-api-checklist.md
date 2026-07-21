# OWASP API Security Checklist — PizzaMama Market

## API1 - Broken Object Level Authorization

- [x] Ogni endpoint filtra i dati per utente proprietario (queryset filtrato per `user=request.user`)
- [x] Nessun utente puo leggere ordini di un altro utente (test: `test_user_cannot_read_another_user_order`)
- [x] Gli endpoint admin sono protetti da ruolo (IsManager, IsITAdmin, IsManagerOrITAdmin)

## API2 - Broken Authentication

- [x] Login rate limited (LoginRateThrottle: 5/min)
- [x] Errore login generico ("Invalid credentials", nessuna indicazione username vs password)
- [x] Refresh token gestito in modo sicuro (SimpleJWT rotation + blacklist)
- [x] Account lockout dopo 5 tentativi falliti (django-axes, cooloff 1h)

## API3 - Broken Object Property Level Authorization

- [x] I serializer non espongono la password hash
- [x] I campi read-only sono definiti nei serializer

## API4 - Unrestricted Resource Consumption

- [x] Pagination attiva (PAGE_SIZE=20)
- [x] Rate limit globale attivo (50/h anon, 500/h user)
- [x] Upload size limitato (DATA_UPLOAD_MAX_MEMORY_SIZE = 2MB)

## API5 - Broken Function Level Authorization

- [x] `change-status` protetto da IsManagerOrITAdmin
- [x] `analytics/dashboard/` protetto da IsManager | IsITAdmin
- [x] `me/export/` protetto da IsAuthenticated

## API8 - Security Misconfiguration

- [x] DEBUG=False in produzione
- [x] ALLOWED_HOSTS configurato con fail-fast
- [x] CORS ristretto agli origini consentiti
- [x] Security headers HSTS, XFrame, CSP in prod.py
- [x] HTTPS forzato in produzione

## API10 - Unsafe Consumption of APIs

- [x] Nessuna chiamata API esterna senza timeout gestito
- [x] Sentry per tracking errori in produzione
