# Database Environment Variables — PizzaMama Market

## DATABASE_URL

Formato PostgreSQL:

```
postgres://USER:PASSWORD@HOST:PORT/DB_NAME
```

Esempi:

```
# Locale con Docker
DATABASE_URL=postgres://pizzamama:pizzamama@localhost:5432/pizzamama

# Render (staging/production)
DATABASE_URL=postgres://user:pass@host.render.com:5432/dbname
```

## Regole

- Non committare mai DATABASE_URL reale nel repository
- Usare database diversi per local, staging e production
- Ruotare le credenziali se esposte accidentalmente
- Limitare accesso diretto al database production (solo da app o VPN)
- Il fallback SQLite (`sqlite:///db.sqlite3`) è attivo solo se DATABASE_URL non è impostato
