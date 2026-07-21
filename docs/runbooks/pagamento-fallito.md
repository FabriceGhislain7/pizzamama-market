# Runbook — Pagamento Fallito

## Sintomi

- Ordine creato ma pagamento non confermato
- Webhook Stripe non ricevuto o non processato
- Stato ordine rimasto `pending` dopo tentativo pagamento

## Controlli

1. Verificare evento in Stripe Dashboard → Webhooks
2. Verificare log applicativi per errori webhook
3. Verificare audit log pagamento (`action_type=payment`)
4. Verificare stato ordine nel database

## Regola

Non marcare manualmente un ordine come pagato senza traccia audit.
Ogni modifica manuale deve passare da `AuditService.log()`.

## Rimborso

Il rimborso va gestito da Stripe Dashboard o via API Stripe.
Dopo rimborso: aggiornare stato ordine a `refunded` tramite API autenticata.
