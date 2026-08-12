---
name: fatture-in-cloud
description: "Integrazione con le API v2 di Fatture in Cloud (fattureincloud.it / TeamSystem). Usa SEMPRE questa skill quando si parla di Fatture in Cloud, FIC, api-v2.fattureincloud.it, fatturazione elettronica via API, invio all'SDI, sincronizzazione fatture/clienti/fornitori/prodotti/spese da un gestionale, OAuth Fatture in Cloud, webhook FIC, o quando si scrive codice (Python/Django, JS, PHP...) che crea/legge/modifica documenti emessi o ricevuti su Fatture in Cloud — anche se la richiesta è generica come 'collega il gestionale a Fatture in Cloud', 'scarica le fatture', 'crea la fattura via API' o 'perché la chiamata mi dà errore'. Contiene la spec OpenAPI 2.1.8 completa (endpoint, scope, modelli, enum, query language, e-fattura, rate limit e trappole note)."
---

# Fatture in Cloud API v2

Base URL: `https://api-v2.fattureincloud.it` — REST, JSON, OAuth2 Bearer. Spec di riferimento: OpenAPI **2.1.8** (marzo 2026), repo ufficiale `fattureincloud/openapi-fattureincloud`.

## Mappa mentale dell'API (la visione d'insieme)

1. **Autenticazione** → token Bearer (`a/...`), poi `GET /user/companies` per il `company_id`. Quasi tutto è sotto `/c/{company_id}/...`.
2. **Anagrafiche**: `entities/clients`, `entities/suppliers`, `products` — CRUD completo.
3. **Documenti emessi** (`issued_documents`): UN solo endpoint per 11 tipi (`invoice, quote, proforma, receipt, delivery_note, credit_note, order, work_report, supplier_order, self_own_invoice, self_supplier_invoice`), distinti dal campo/param `type`. Include: totals, attachment, email, transform (es. preventivo→fattura), join, e-invoice (verify/send/xml/error_reason).
4. **Documenti ricevuti** (`received_documents`): spese e fatture passive (`expense, passive_credit_note, passive_delivery_note, self_invoice`) + `received_documents/pending` (fatture passive da SDI/mail da registrare).
5. **Altre risorse**: `receipts` (corrispettivi), `taxes` (F24), `cashbook` (prima nota), `archive`, `price_lists`, `emails`, `bin` (cestino), `subscriptions` (webhook).
6. **Configurazione**: `settings/` (vat_types, payment_methods, payment_accounts, templates, tax_profile) + `info/` (liste di supporto senza scope).

Prima di scrivere codice leggi il file di riferimento pertinente in `references/`:

| File | Quando leggerlo |
|---|---|
| `references/endpoints.md` | Elenco completo dei 123 endpoint con scope richiesti e parametri comuni |
| `references/autenticazione.md` | OAuth flow, token, refresh, scope, trappole redirect_uri |
| `references/query-filtri-paginazione.md` | Parametro `q` (SQL-like), campi filtrabili per metodo, page/per_page/sort/fields/fieldset |
| `references/modelli.md` | Tutti i modelli (IssuedDocument 86 campi, Entity, ReceivedDocument, Product, VatType...) ed enum |
| `references/fattura-elettronica.md` | Flusso SDI: ei_data, dry_run, ei_status, ei_raw, bollo, note di credito |
| `references/webhooks.md` | Eventi disponibili, subscription, verifica, scadenza |
| `references/errori-limiti.md` | Codici errore, rate limit (403 vs 429), plan limits, URL a scadenza 7gg, retry pattern |

## Regole non negoziabili (le trappole che causano il 90% degli errori)

1. **Body incapsulati**: richieste Create/Modify → `{"data": {...}}`; risposte → `{"data": {...}}`. Le List sono paginate stile Laravel (`data[]`, `next_page_url`, `total`).
2. **`per_page` di default è 50** (verificato 12/08/2026 su `entities/clients`, `issued_documents`, `received_documents`, `products`). Impostalo comunque (max 100) e pagina finché `next_page_url` è null: 50 basta a nascondere il problema in sviluppo e non in produzione.
3. **`fieldset=detailed` per i dettagli**: le List (e alcune Get) di default NON restituiscono `items_list`, `payments_list`, `ei_status`. Se un campo "manca", quasi sempre è un problema di fieldset/fields, non dell'API.
4. **Niente autocompletamento**: passare `entity.id` o `product_id` NON popola nome, indirizzo, prezzi nel documento. Ogni campo che deve comparire va scritto esplicitamente nel body (recuperalo prima con Get Client/Product).
5. **Creare una e-fattura NON la invia all'SDI**: serve `POST .../e_invoice/send` separato; poi si monitora `ei_status` (con fieldset detailed) o il webhook `e_invoices.status_update`. Per i test usa `options.dry_run: true`. Non è possibile inviare XML generati esternamente.
6. **`vat.id` è per-company**: recupera gli id con `GET /c/{id}/info/vat_types` (richiede scope `settings:r`); non dare per scontato che 0 = 22%.
7. **`payments_list`**: la somma delle rate deve coincidere col totale documento; `status: "paid"` esige un `payment_account.id` esistente. In dubbio, calcola prima con `POST /issued_documents/totals`.
8. **PUT sostituisce le liste**: in Modify, `items_list`/`payments_list` inviate rimpiazzano integralmente quelle esistenti — invia sempre la lista completa con gli id delle righe da conservare.
9. **URL dei PDF/allegati scadono dopo 7 giorni** (policy 09/2025): mai persisterli; riscarica l'URL con una nuova Get o salva il file.
10. **Rate limit**: 1.000/ora e 40.000/mese per company-app (→ 403), 300/5min per company condivise tra tutte le app (→ 429). Sempre backoff esponenziale + rispetto di `Retry-After`. Creare più app private NON aumenta le quote.
11. **Scope minimi ma giusti**: gli scope issued_documents sono per singolo tipo (`issued_documents.invoices:a` ≠ `.credit_notes:a`); cambiare scope = nuova autorizzazione OAuth da zero. Il refresh token ruota: salva sempre quello nuovo.
12. **Filtri `q` solo sui campi ammessi** dal metodo specifico (tabella in query-filtri-paginazione.md); campo non autorizzato = errore. Stringhe tra apici singoli, tutto URL-encoded.
13. **Bollo in e-fattura a carico cliente** = riga dedicata (`Bollo in fattura`, 2€, `not_taxable: true`, IVA 0% Escluso Art.15) — il campo `stamp_duty` in e-fattura mette il bollo a carico dell'emittente.
14. **422 = leggi `validation_result`**: contiene campo per campo cosa non va; non tirare a indovinare.

## Workflow tipo: creare e inviare una fattura elettronica

```
1. GET /c/{id}/issued_documents/info?type=invoice   → numerazioni, vat_types, payment_accounts, methods, templates
                                              ⚠️ `type` (o `id`) è OBBLIGATORIO: senza, 422
                                                 "The type field is required when id is not present."
2. GET /c/{id}/entities/clients?q=vat_number = '...'   → id + dati cliente (o POST per crearlo)
3. POST /c/{id}/issued_documents/totals       → verifica importi di items+payments
4. POST /c/{id}/issued_documents              → {"data": {type, entity{...completa...}, date, numeration,
                                                 e_invoice: true, ei_data{vat_kind, payment_method:"MP05",...},
                                                 items_list[{name, net_price, qty, vat:{id}}],
                                                 payments_list[{amount, due_date, status}], payment_method:{id}}}
5. POST /c/{id}/issued_documents/{doc}/e_invoice/send   (prima volta: options.dry_run=true)
6. GET  /c/{id}/issued_documents/{doc}?fieldset=detailed → ei_status  (oppure webhook status_update)
7. se discarded/rejected → GET .../e_invoice/error_reason → correggi → re-send
```

## Workflow tipo: sincronizzare le fatture passive (spese)

```
1. Preferisci i webhook: received_documents.create/update + received_documents.e_invoices.receive
2. Altrimenti polling: GET /c/{id}/received_documents?type=expense
      &q=updated_at >= '<ultimo_sync>'&per_page=100&fieldset=detailed&sort=-updated_at
3. Le fatture SDI non ancora registrate: GET /c/{id}/received_documents/pending?type=agyo
4. Scarica subito gli allegati (attachment_url scade in 7 giorni)
```

## SDK ufficiali

Python `fattureincloud-python-sdk` (PyPI), JS `@fattureincloud/fattureincloud-js-sdk`, TS, PHP, Java, C#, Go, Ruby + connettore Zapier. Gli SDK includono OAuth helper e Filter helper. Per Django/requests va benissimo anche l'HTTP diretto seguendo queste regole.

## Verità sul campo

Se un comportamento sembra contraddire questa skill (l'API evolve), fidati della risposta reale dell'API e della doc ufficiale (https://developers.fattureincloud.it), e proponi a Giacomo di aggiornare la skill.
