# Manuale Admin — PizzaMama Market

## Accesso

URL admin Django:

```
https://pizzamama-market-backend.onrender.com/admin/
```

Credenziali: fornite separatamente.

## Operazioni comuni

### Gestire prodotti (Ruolo: Staff)

1. Admin → Products → Pizzas
2. Cliccare "Add pizza" o selezionare una esistente
3. Compilare: nome, categoria, prezzo base, ingredienti, immagine
4. Salvare
5. Verificare nel frontend su `/menu`

### Gestire ordini (Ruolo: Manager / IT_Admin)

1. Admin → Orders → Orders
2. Filtrare per stato: `pending`, `confirmed`, `preparing`, ecc.
3. Per cambiare stato: usare API `POST /api/v1/orders/{id}/change-status/` con token JWT (non da admin direttamente)

### Gestire utenti e ruoli (Ruolo: IT_Admin)

1. Admin → Auth → Users → seleziona utente
2. Sezione "Groups": aggiungere il gruppo corretto
   - `Manager`, `Kitchen`, `Delivery`, `Staff`, `IT_Admin`, `Finance`
3. Salvare

### Audit log (Ruolo: IT_Admin)

1. Admin → Audit → Audit logs
2. Filtrare per utente, tipo azione, data
3. I log sono in sola lettura — non modificabili

## Regole

- Non condividere account admin
- Usare password robuste (min 16 caratteri)
- Segnalare accessi sospetti all'IT Admin
- Non usare il database production per test
