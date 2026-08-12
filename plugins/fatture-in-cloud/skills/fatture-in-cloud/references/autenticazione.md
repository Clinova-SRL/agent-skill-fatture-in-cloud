# Autenticazione — OAuth 2.0 e token

## I tre metodi supportati

1. **OAuth 2.0 Authorization Code Flow** — metodo raccomandato per app con backend (es. Django). Richiede redirect URL registrata.
2. **OAuth 2.0 Device Code Flow** — NON generalmente disponibile: va richiesto a Fatture in Cloud e viene abilitato solo per casi specifici senza backend. Endpoint `POST /oauth/device`.
3. **Manual Token** — token generato a mano dalla pagina Fatture in Cloud (Applicazioni). Perfetto per script personali e sviluppo; usato come Bearer identico agli altri.

## Token e durate (fondamentale)

| Token | Prefisso | Durata |
|---|---|---|
| Authorization Code | `c/` | 60 secondi, monouso |
| Access Token | `a/` | **24 ore** dall'emissione |
| Refresh Token | `r/` | **1 anno dall'ultimo refresh** (sliding: se lo usi ogni giorno non scade mai) |

⚠️ Il refresh restituisce **anche un nuovo refresh_token**: va sempre salvato al posto del vecchio.

## Authorization Code Flow — passi

1. **Redirect utente** a `https://api-v2.fattureincloud.it/oauth/authorize` con query: `response_type=code`, `client_id`, `redirect_uri`, `scope` (lista separata da SPAZI, es. `entity.clients:r issued_documents.invoices:a`), `state` (anti-CSRF, da verificare al ritorno).
2. **Callback**: la redirect URI riceve `?state=...&code=...`. Verifica lo `state`, poi usa il `code` entro 60s.
3. **Scambio token**: `POST https://api-v2.fattureincloud.it/oauth/token` con JSON body:
   ```json
   {"grant_type":"authorization_code","client_id":"...","client_secret":"...","redirect_uri":"...","code":"c/..."}
   ```
   Risposta: `{"token_type":"bearer","access_token":"a/...","refresh_token":"r/...","expires_in":86400}`.
4. **Refresh**: stesso endpoint con `{"grant_type":"refresh_token","client_id","client_secret","refresh_token"}`.

## Trappole note

- **redirect_uri confrontata con String Equals**: deve essere IDENTICA carattere per carattere a quella registrata nell'app (uno `/` finale in più = errore). Ambienti diversi (DEV/PROD) = app o redirect diverse, non mischiarle. `http://localhost:8080` è ammessa per sviluppo locale.
- **Client Secret solo lato backend**: mai nel frontend, mai in repo. Se esposto → eliminare l'app e ricrearla.
- **Cambiare gli scope richiede una nuova autorizzazione**: non si può ampliare un token esistente; si butta il vecchio e si rifà il flow dal punto 1 con i nuovi scope.
- Un token è per-utente: app multi-tenant deve associare i token al singolo utente/company.
- Header richieste: `Authorization: Bearer a/...` (il prefisso "Bearer " va aggiunto).

## Scope (elenco completo)

Formato `risorsa:r` (lettura) / `risorsa:a` (scrittura, include lettura). Gli scope Issued Documents sono PER TIPO documento:

- `entity.clients:r|a`, `entity.suppliers:r|a`
- `products:r|a`, `stock:r|a`
- `issued_documents.invoices:r|a`, `.credit_notes:r|a`, `.receipts:r|a`, `.orders:r|a`, `.quotes:r|a`, `.proformas:r|a`, `.delivery_notes:r|a`, `.work_reports:r|a`, `.supplier_orders:r|a`, `.self_invoices:r|a`
- `received_documents:r|a`
- `receipts:r|a` (corrispettivi)
- `taxes:r|a` (F24), `calendar:r|a`, `archive:r|a`, `emails:r`, `cashbook:r|a` (prima nota)
- `settings:r|a` (⚠️ serve `settings:r` anche solo per **listVatTypes**), `situation:r`

Richiedi il minimo indispensabile: scope mancanti → 403 sulle chiamate; troppi → l'utente può rifiutare l'autorizzazione.

## Company ID

Dopo il token, ricava il `company_id` con `GET /user/companies` (le company accessibili all'utente, con ruolo e permessi). Serve per tutti i metodi `/c/{company_id}/...`. `GET /user/info` restituisce l'utente. `GET /c/{id}/company/info` i dettagli e le funzioni attive della company.

⚠️ **La partita IVA dell'azienda sta in `/user/companies`, non in `/company/info`.** È il punto dove si perde più tempo di tutta l'autenticazione, perché l'endpoint che sembra quello giusto è l'altro. Per ogni azienda `/user/companies` restituisce anche `vat_number` e `tax_code`:

```json
{"id": 1619878, "name": "Gateway Prova SRL", "vat_number": "01234567897", "tax_code": "01234567897"}
```

`GET /c/{id}/company/info` dà nome, email, piano, licenza e permessi — `vat_number` **non c'è proprio**. Chi cerca lì i dati fiscali dell'emittente conclude che l'API non li esponga affatto, e finisce per ricopiarli a mano in configurazione: due verità che poi divergono, e un documento che dice una cosa diversa dal registro.

Quello che invece FIC **non espone da nessun endpoint** è la **sede** dell'azienda — indirizzo, CAP, comune, provincia. Provati `/company/info`, `/user/companies`, `/settings/tax_profile`: non c'è. Quella va scritta a mano. *(Verificato contro l'API il 12/08/2026, azienda 1619878.)*

## Errori OAuth

- Authorization phase: errori come query param nella redirect (o mostrati sulla pagina FIC se la redirect è invalida).
- Token endpoint: `400` con `{"error":"invalid_request","error_description":"..."}`.
- Device flow polling: gestire `slow_down`, `authorization_pending`, `access_denied`, `expired_token`.
