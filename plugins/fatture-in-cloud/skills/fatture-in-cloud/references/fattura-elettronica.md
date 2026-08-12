# Fattura elettronica (SDI) — flusso completo

## Il flusso in 4 fasi (creare ≠ inviare!)

1. **Crea** il documento con `POST /c/{id}/issued_documents` impostando `e_invoice: true` e `ei_data`. Questo NON invia nulla all'SDI.
2. **(Opzionale) Verifica** con `GET .../issued_documents/{document_id}/e_invoice/xml_verify` — controlla campi obbligatori e formato.
3. **Invia** con `POST .../issued_documents/{document_id}/e_invoice/send`. Body opzionale `{"data": {...}, "options": {"dry_run": true}}` — con `dry_run: true` esegue tutti i controlli SENZA inviare all'SDI (per test; richiede comunque fatturazione elettronica attiva sull'account).
4. **Monitora** lo stato: `GET .../issued_documents/{document_id}` con **`fieldset=detailed`** e leggi `ei_status` (senza detailed il campo non compare!). In caso di scarto: `GET .../e_invoice/error_reason` per il motivo. XML scaricabile con `GET .../e_invoice/xml` (risposta text/xml; param `include_attachment`).

In alternativa al polling: webhook `it.fattureincloud.webhooks.issued_documents.e_invoices.status_update`.

## Stati `ei_status`

| Stato | Significato |
|---|---|
| `attempt` | invio in corso (attendere fino a 2h) |
| `missing` | fattura mancante |
| `not_sent` | ancora da inviare |
| `sent` | inviata |
| `pending` | controlli firma/invio in corso |
| `processing` | SDI sta consegnando al destinatario |
| `error` | errore in gestione → reinviare o contattare supporto |
| `discarded` | **scartata dall'SDI** → correggere e reinviare |
| `not_delivered` | SDI non è riuscito a consegnare (mancato recapito) |
| `accepted` / `manual_accepted` | accettata dal cliente (PA) |
| `rejected` / `manual_rejected` | rifiutata dal cliente → correggere |
| `no_response` | nessuna risposta entro i termini → verificare col cliente |

## `ei_data` (obbligatorio con e_invoice=true)

- `vat_kind`: `I` immediata / `D` differita / `S` split payment
- `payment_method`: codice **ModalitaPagamento FatturaPA** (MP01 contanti, MP05 bonifico, MP08 carta, MP12 RIBA, ... — tabella ufficiale fatturapa.gov.it). Richiesto per le e-fatture.
- `bank_iban`, `bank_name`, `bank_beneficiary` (se diverso dalla ragione sociale)
- `cig`, `cup` (appalti PA), `original_document_type` (`ordine|contratto|convenzione`) + `od_number`, `od_date`
- `invoice_number`, `invoice_date`: **per le note di credito** = riferimenti alla fattura da stornare

E sul cliente (`entity`): `e_invoice: true`, `ei_code` (codice destinatario SDI, 7 caratteri; `0000000` + PEC per privati), `certified_email` (PEC opzionale). Per PA: `type: "pa"` e codice univoco ufficio a 6 caratteri.

## `ei_raw` — campi XML avanzati

I campi FatturaPA non coperti dal modello si impostano con `ei_raw` a 3 livelli: documento (`data.ei_raw`), riga (`items_list[].ei_raw`), pagamento (`payments_list[].ei_raw`, es. `{"DettaglioPagamento": {"CAB": "..."}}`).
⚠️ In `ei_raw` **tutti i valori sono stringhe**, anche i numeri (`"NumItem": "5"`).

## Bollo (imposta di bollo 2€)

- **E-fattura, bollo a carico del cliente**: aggiungi una riga con `name: "Bollo in fattura"`, `net_price: 2`, `not_taxable: true`, `vat.id: 21` (0% Escluso Art.15).
- **E-fattura col campo `stamp_duty`**: il bollo risulta a carico TUO, non del cliente.
- **Fattura non elettronica**: basta `stamp_duty: 2`.

## Limiti importanti

- **Non si può inviare all'SDI un XML generato esternamente**: FIC invia solo documenti creati tramite le sue funzionalità (guida "Externally generated XML"). L'unico percorso è Create Issued Document → Send E-Invoice.
- Le fatture ricevute via SDI arrivano come **Pending Received Documents** (`type=agyo`) o direttamente tra i received documents; webhook dedicato `received_documents.e_invoices.receive`.
- L'IVA di ogni riga deve avere `vat_type.e_invoice: true` e, per aliquote 0%, la **Natura** corretta (`ei_type` N1–N7).
- Autofatture: tipi documento `self_own_invoice` / `self_supplier_invoice` (TD16–TD19 gestiti via ei_raw/numerazione dedicata a seconda del caso).
