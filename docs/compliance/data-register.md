# Registro Dati Trattati — PizzaMama Market

## Accounts - Custom User

| Campo | Categoria | Finalita | Accesso | Retention |
|---|---|---|---|---|
| email | personale / identificativo | login e comunicazioni | user, admin | finche account attivo |
| username | personale / identificativo | login / display | user, admin | finche account attivo |
| password | credenziale hashata | autenticazione | sistema | finche account attivo |
| is_staff | tecnico / autorizzazione | controllo accessi | admin | finche account attivo |

## Accounts - Profile

| Campo | Categoria | Finalita | Accesso | Retention |
|---|---|---|---|---|
| phone | personale / contatto | consegna ordine | user, staff autorizzato | finche necessario |
| avatar | personale / media opzionale | profilo utente | user, admin | finche account attivo |

## Accounts - Address

| Campo | Categoria | Finalita | Accesso | Retention |
|---|---|---|---|---|
| street | personale / indirizzo | consegna ordine | user, staff autorizzato | finche necessario |
| city | personale / indirizzo | consegna ordine | user, staff autorizzato | finche necessario |
| zip_code | personale / indirizzo | consegna ordine | user, staff autorizzato | finche necessario |

## Orders

| Campo | Categoria | Finalita | Accesso | Retention |
|---|---|---|---|---|
| user | personale / relazione cliente | gestione ordine | user, staff autorizzato | obblighi fiscali/business |
| delivery_address | personale / indirizzo | consegna ordine | user, staff autorizzato | finche necessario |
| total_amount | commerciale | pagamento / reporting | user, staff autorizzato | obblighi fiscali/business |
| status | operativo / workflow | gestione ordine | staff autorizzato | storico ordine |

## Audit Log

| Campo | Categoria | Finalita | Accesso | Retention |
|---|---|---|---|---|
| user | relazione | tracciabilita azioni | solo IT_Admin | periodo definito dal progetto |
| ip_address | tecnico | sicurezza / analisi incidenti | solo IT_Admin | periodo definito dal progetto |
| action_type | operativo | compliance | solo IT_Admin | periodo definito dal progetto |
