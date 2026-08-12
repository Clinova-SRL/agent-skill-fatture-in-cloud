# Filtri (q), paginazione, ordinamento, customizzazione risposta

## Parametro `q` — query language SQL-like

Sottinsieme della clausola WHERE SQL. Struttura a triplette `campo op valore`, combinabili con `and`/`or` e parentesi. **Sempre URL-encoded**.

Operatori di confronto: `=`, `>`, `>=`, `<`, `<=`, `<>`, `!=`
Operatori su stringhe (solo su campi stringa): `like` (con `%`), `not like`, `contains`, `not contains`, `starts with`, `ends with`
Null-check: `is null`, `is not null`, `= null`, `!= null`
Valori: stringhe tra apici singoli `'valore'`, boolean `true/false`, int, double. Le date come stringhe ISO: `date >= '2026-01-01'`.

Esempi validi:
```
vat_number = '11553420156'
amount_gross >= 122.50
entity.name contains 'Rossi'
type = 'invoice' and date >= '2026-01-01' and date <= '2026-01-31'
entity.id = 5 and (amount_net > 100 or number is not null)
```

### Campi filtrabili per metodo (SOLO questi — altri campi → errore)

| Metodo | Campi ammessi in `q` |
|---|---|
| listClients / listSuppliers | id, code, name, type, vat_number, tax_code, address_street, address_postal_code, address_city, address_province, country, email, certified_email, phone, fax, notes, imported, atoka_show, e_invoice, ei_code, created_at, updated_at |
| listProducts | id, name, code, net_price, gross_price, net_cost, description, category, notes, in_stock, created_at, updated_at |
| listIssuedDocuments | type, entity.id, entity.name, entity.vat_number, entity.tax_code, entity.city, entity.province, entity.country, date, number, numeration, any_subject, amount_net, amount_vat, amount_gross, next_due_date, created_at, updated_at |
| listReceivedDocuments | id, type, category, description, entity.id, entity.name, date, next_due_date, amount_gross, amount_net, amount_vat, invoice_number, created_at, updated_at |
| listReceipts | date, type, description, rc_center, created_at, updated_at |
| listF24 | due_date, status, amount, description |
| listArchiveDocuments | date, category, description |

Nota: `any_subject` su listIssuedDocuments cerca sia in `subject` sia in `visible_subject`.

## Paginazione

- `page` (default 1) e `per_page` (**default 5**, max 100). Impostare sempre `per_page=100` per sincronizzazioni.
- Risposta stile Laravel: `current_page, data[], first_page_url, from, last_page, last_page_url, next_page_url, path, per_page, prev_page_url, to, total`.
- Loop: continua finché `next_page_url != null` (o `current_page < last_page`).

## Ordinamento

`sort=campo1,-campo2` — `-` per discendente. Es. `sort=-date` per i documenti più recenti prima.

## Customizzazione risposta: `fields` e `fieldset`

- `fields=type,description,amount_gross` → solo quei campi.
- `fieldset=basic|detailed|fic_view`:
  - `basic` è il default sulle List → NON include `items_list`, `payments_list`, `ei_status` e molti altri campi.
  - `detailed` → risorsa completa. **Necessario per leggere `ei_status`** dopo l'invio SDI.
  - `fic_view` → campi extra come `ei_reception_date` e `is_from_pending_expenses` sui documenti ricevuti.
- `fields` e `fieldset` sono mutuamente alternativi; non tutti i metodi li supportano (le Get/List di risorse sì, `getUserInfo` no).
- Suggerito da FIC per ridurre chiamate in polling: usa `fields`/`fieldset` sulle List per evitare Get singole.

## Sincronizzazione via polling (se non usi i webhook)

- Filtra su `updated_at > '<ultimo sync>'` (aggiornamenti) e tieni traccia degli id già processati.
- Frequenza bassa e backoff esponenziale sugli errori: le quote sono condivise a livello company (vedi errori-limiti.md).
- Preferisci comunque i **webhook** (references/webhooks.md).
