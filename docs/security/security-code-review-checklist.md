# Security Code Review Checklist — PizzaMama Market

Prima di ogni merge verificare:

## Segreti e configurazione

- [ ] Nessun segreto hardcoded nel codice (SECRET_KEY, DATABASE_URL, TOKEN)
- [ ] Nessun dato personale nei log (email, password, IP in chiaro)
- [ ] `.env` non committato (verificare `.gitignore`)

## Autenticazione e autorizzazione

- [ ] Endpoint protetti dalla permission class corretta
- [ ] Queryset filtrati per utente o ruolo (mai `.all()` senza filtro)
- [ ] Serializer senza campi sensibili esposti (password_hash, token)
- [ ] Test autorizzazioni presenti per ogni nuovo endpoint

## Qualita codice

- [ ] Migrazioni controllate (nessuna migrazione non tracciata)
- [ ] `python manage.py check --deploy` eseguito senza errori
- [ ] Tutti i test passanti (`pytest`)
- [ ] Coverage sopra la soglia minima (80%)

## Audit e tracciabilita

- [ ] Azioni sensibili loggate via AuditService
- [ ] Nessuna azione critica senza log (cambio status, login, logout)
