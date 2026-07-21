# Frontend Token Strategy — PizzaMama Market

## Access token

- Durata: 15 minuti
- Usato per chiamare le API (header `Authorization: Bearer <token>`)
- Salvato in `localStorage` (lato frontend)

## Refresh token

- Durata: 7 giorni
- Usato per ottenere un nuovo access token scaduto
- Salvato in `localStorage` — valutare `HttpOnly cookie` per produzione ad alto rischio

## Regole

- Non loggare mai token in console (`console.log`)
- Non inviare token a servizi terzi o analytics
- Implementare logout completo (blacklist del refresh token sul backend)
- Gestire scadenza: se il refresh token scade, redirect al login
- Controllare la risposta 401 in ogni chiamata API — se access token scaduto, provare refresh automatico

## Logout

Il logout corretto richiede:

1. Chiamare `POST /api/v1/accounts/logout/` con il refresh token (blacklist backend)
2. Cancellare access token e refresh token dal localStorage
3. Redirect al login

## CORS in produzione

```python
# config/settings/prod.py
CORS_ALLOWED_ORIGINS = [
    "https://pizzamama-market.onrender.com",  # frontend production
]
```

Mai usare `CORS_ALLOW_ALL_ORIGINS = True` in produzione.
