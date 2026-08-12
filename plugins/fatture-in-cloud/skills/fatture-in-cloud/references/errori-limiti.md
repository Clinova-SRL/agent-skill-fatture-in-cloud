# Errori, rate limit, quote e scadenza URL

## Codici errore

| Codice | Significato | Azione |
|---|---|---|
| 401 | Token mancante/invalido/scaduto | Refresh token o ri-autentica |
| 403 | Permessi/scope insufficienti, licenza scaduta, **o quota long-term superata** | Verifica scope; se quota → attendi `Retry-After` |
| 404 | Risorsa inesistente | — |
| 409 | Conflict, operazione non eseguibile | — |
| 422 | Body non valido (validazione) | La risposta include `error.validation_result` con i campi errati e i messaggi — leggilo sempre |
| 429 | **Rate limit short-term superato** | Attendi `Retry-After`, backoff esponenziale |
| 5xx | Errore server FIC (raro) | Retry, poi supporto |

Formato: `{"error": {"message": "...", "code": ..., "validation_result": {...}}}`. I messaggi possono essere in italiano.

## Rate limit (3 tipi)

**Long-term** (finestra fissa, reset a inizio ora/mese; superamento → **403** + Retry-After):
- 1.000 richieste/ora per coppia company-app
- 40.000 richieste/mese per coppia company-app (app pubbliche) o per company (app private — creare più app private NON aumenta la quota)
- Solo i limiti long-term sono incrementabili su richiesta motivata a FIC.

**Short-term** (sliding window; superamento → **429** + Retry-After):
- **300 richieste ogni 5 minuti a livello COMPANY** — condivise tra TUTTE le app e gli utenti che accedono alla stessa company. Se ottieni 429, per FIC "stai usando male le API": implementa backoff, mai richiedere aumento.

**Plan limits** (piano Fatture in Cloud della company): numero massimo di documenti/anno e risorse totali per piano (`trial, standard, premium, premium_plus, complete`). Verifica con `GET /c/{id}/company/plan_usage?category=...` — se `usage >= limit` le Create falliscono. Il limite documenti è annuale, gli altri sono globali.

Header su ogni risposta: `RateLimit-HourlyRemaining`, `RateLimit-HourlyLimit`, `RateLimit-MonthlyRemaining`, `RateLimit-MonthlyLimit`. Monitorali e rallenta preventivamente.

### Pattern di retry raccomandato (Python)

```python
import time, requests

def fic_request(method, url, max_retries=6, **kw):
    for attempt in range(max_retries):
        r = requests.request(method, url, **kw)
        if r.status_code in (429, 403) and 'Retry-After' in r.headers:
            wait = int(r.headers['Retry-After'])
            time.sleep(min(wait, 2 ** attempt * 2))
            continue
        if r.status_code >= 500:
            time.sleep(2 ** attempt)
            continue
        return r
    r.raise_for_status()
```

## ⚠️ Scadenza URL documenti (dal 10/09/2025)

Tutti gli URL restituiti dalle API per PDF/allegati (`url`, `dn_url`, `ai_url`, `attachment_url`, `attachment_preview_url`) **scadono dopo 7 giorni**.
- **NON salvare mai questi URL in database** per uso futuro.
- Per riscaricare: rifai la Get/List del documento (con `fields`/`fieldset` adeguati) e usa l'URL fresco, oppure scarica subito il file e conserva il file.

## Upload allegati (flusso a 2 passi)

1. `POST /c/{id}/{issued_documents|received_documents|taxes|archive}/attachment` — multipart form (`filename`, `attachment` file). Formati tipici: pdf, doc/docx, xls/xlsx, jpg/png, txt, csv, zip.
2. La risposta contiene `attachment_token` → passalo come `attachment_token` nel Create/Modify del documento. Per ArchiveDocument il token è obbligatorio.

## Note operative

- Il `modify` (PUT) aggiorna i campi passati, ma **`items_list` e `payments_list` passate sostituiscono integralmente le liste esistenti**: per modificare una riga, invia la lista completa (con gli `id` delle righe da conservare).
- I DELETE spostano i documenti nel **cestino** (`/bin/...`): recuperabili con `POST .../recover`; il DELETE sul bin è definitivo.
- Prima di creare un documento con importi delicati usa `POST /issued_documents/totals` (o `/{id}/totals`) per farti calcolare i totali dal server e verificare la coerenza di rate e righe.
