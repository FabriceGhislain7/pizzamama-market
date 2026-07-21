# Data Retention Policy — PizzaMama Market

## Obiettivo

Definire per quanto tempo il sistema conserva i dati e le azioni da intraprendere alla scadenza.

## Regole

| Dato | Retention | Azione finale |
|---|---|---|
| Account utente | Finche account attivo | Cancellazione o anonimizzazione su richiesta |
| Indirizzi consegna | Finche necessari al servizio | Cancellazione su richiesta utente |
| Ordini | Secondo necessita fiscali / business (7 anni) | Anonimizzazione dati personali se possibile |
| Audit log | Minimo 1 anno | Conservazione protetta, non cancellabile |
| Log applicativi | 30 giorni operativi | Rotazione automatica / eliminazione |
| Token JWT | Access: 15 min, Refresh: 7 giorni | Scadenza automatica + blacklist logout |

## Export dati utente

L'utente puo richiedere l'export dei propri dati tramite:

```
GET /api/v1/accounts/me/export/
Authorization: Bearer <token>
```

## Note

Le durate precise devono essere validate con il cliente e, se necessario, con un consulente legale.
Le regole variano in base alla giurisdizione e al tipo di dato.
