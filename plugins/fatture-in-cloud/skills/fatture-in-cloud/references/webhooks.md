# Webhook

Disponibili per tutti (non più closed beta). Basati sullo standard **CloudEvents**. Alternativa raccomandata al polling.

## Endpoint di gestione (tag Subscriptions, `/c/{company_id}/subscriptions`)

- `GET /subscriptions` — lista sottoscrizioni
- `POST /subscriptions` — crea: body `{"data": {"sink": "https://tuo-endpoint", "types": ["it.fattureincloud.webhooks. ..."], "config": {"mapping": "structured"}, "verification_method": "header"}}`
- `GET/PUT/DELETE /subscriptions/{subscription_id}` (id è una STRINGA)
- `POST /subscriptions/{subscription_id}/verify` — avvia/completa la verifica dell'endpoint

Campi WebhooksSubscription: `id, sink (callback URL), verified (RO), types[], config.mapping (binary|structured), verification_method (header|query)`.

- **Verifica obbligatoria**: dopo la creazione la subscription non è `verified`; FIC invia una challenge all'endpoint (in header o query a seconda di `verification_method`) e l'endpoint deve risponderle correttamente; `verify` per ritriggerarla.
- **Le subscription scadono** (pagina "Subscription Expiration"): mantienile attive/rinnovale, e non dare per scontato che restino valide per sempre.
- `mapping`: `structured` = evento CloudEvents come JSON nel body; `binary` = attributi CloudEvents negli header HTTP.
- La notifica contiene gli ID delle risorse toccate, non l'intera risorsa: fai una Get per i dettagli.
- Rispondi 2xx rapidamente; processa in coda (es. Celery) per evitare retry.

## Tipi di evento (EventType)

Prefisso comune `it.fattureincloud.webhooks.`

- Documenti emessi, per tipo: `issued_documents.{invoices|quotes|proformas|receipts|delivery_notes|credit_notes|orders|work_reports|supplier_orders|self_supplier_invoices|self_own_invoices}.{create|update|delete|email_sent}` — oppure aggregato `issued_documents.all.{create|update|delete|email_sent}`
- E-fattura: `issued_documents.e_invoices.status_update` (cambi di `ei_status`), `received_documents.e_invoices.receive` (e-fattura passiva ricevuta)
- Documenti ricevuti: `received_documents.{create|update|delete}`
- Corrispettivi: `receipts.{create|update|delete}`
- F24: `taxes.{create|update|delete}`
- Archivio: `archive_documents.{create|update|delete}`
- Prima nota: `cashbook.{create|update|delete}`
- Prodotti: `products.{create|update|delete|stock_update}`
- Anagrafiche: `entities.clients.{create|update|delete}`, `entities.suppliers.{...}`, aggregato `entities.all.{...}`

## Se non puoi esporre un endpoint

Polling "educato": bassa frequenza, backoff esponenziale, traccia degli id processati, `fields`/`fieldset` sulle List per evitare Get singole (raccomandazioni ufficiali FIC).
