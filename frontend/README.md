# PizzaMama Market — Frontend React

Frontend React per l'e-commerce pizzeria PizzaMama Market.

## Stack

- React 19 + TypeScript 6
- Vite 8
- React Router 7
- CSS Modules + Design Tokens
- Vitest + React Testing Library

## Installazione locale

```powershell
cd frontend
npm install
copy .env.example .env.local
# Editare .env.local: VITE_API_BASE_URL=http://127.0.0.1:8000/api/v1
npm run dev
```

App disponibile su: `http://localhost:5173/`

## Comandi disponibili

| Comando | Descrizione |
|---|---|
| `npm run dev` | Avvia server di sviluppo |
| `npm run build` | Build production in `dist/` |
| `npm run preview` | Anteprima della build production |
| `npm run lint` | Controllo ESLint |
| `npm run format` | Formattazione Prettier |
| `npm run format:check` | Verifica formattazione |
| `npm run test:run` | Esegue i test una volta |
| `npm run test` | Test in watch mode |
| `npm run check` | Quality gate completo (format + lint + test + build) |

## Quality gate — prima di ogni merge

```powershell
npm run check
```

Deve essere verde su tutti i punti.

## Struttura cartelle

```
src/
├── app/           # Router, ProtectedRoute, StaffRoute, settings
├── components/    # UI riutilizzabili (Button, states, layout)
├── features/      # Logica per dominio (auth, cart, products, orders...)
├── hooks/         # Hook condivisi (useAsync)
├── pages/         # Pagine entry-point
├── services/api/  # httpClient + ApiError
├── styles/        # tokens.css + global.css
├── test/          # Setup Vitest
└── types/         # TypeScript interfaces
```

## Route disponibili

| Route | Accesso | Descrizione |
|---|---|---|
| `/` | Pubblico | Home |
| `/menu` | Pubblico | Catalogo pizze da API |
| `/login` | Pubblico | Login JWT |
| `/register` | Pubblico | Registrazione |
| `/cart` | Autenticato | Carrello |
| `/checkout` | Autenticato | Checkout → crea ordine |
| `/orders` | Autenticato | Storico ordini |
| `/profile` | Autenticato | Profilo + indirizzi |
| `/staff` | Autenticato | Gestione ordini staff |
| `/dashboard` | Autenticato | Dashboard KPI manager |

## Deploy su Render (Static Site)

1. Build command: `npm install && npm run build`
2. Publish directory: `dist`
3. Env var: `VITE_API_BASE_URL=https://pizzamama-market-backend.onrender.com/api/v1`

## Deploy su Netlify / Vercel

Stessa configurazione — build command `npm run build`, publish `dist`.
Aggiungere redirect per SPA: `/* → /index.html 200`.
