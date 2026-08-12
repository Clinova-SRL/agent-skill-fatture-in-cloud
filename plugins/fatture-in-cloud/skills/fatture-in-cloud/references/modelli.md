# Modelli dati ed enum (spec 2.1.8)

## Enum principali

- **IssuedDocumentType**: `invoice, quote, proforma, receipt, delivery_note, credit_note, order, work_report, supplier_order, self_own_invoice, self_supplier_invoice`
- **ReceivedDocumentType**: `expense, passive_credit_note, passive_delivery_note, self_invoice`
- **PendingReceivedDocumentType** (fatture passive in arrivo da smistare): `agyo, mail, browser`
- **IssuedDocumentStatus** (stato pagamento rata): `not_paid, paid, reversed`
- **EntityType / ClientType / SupplierType**: `company, person, pa, condo`
- **PaymentAccountType**: `standard, bank` — **PaymentMethodType**: `standard, riba` — **PaymentTermsType**: `standard, end_of_month`
- **VatKind** (esigibilità IVA, `ei_data.vat_kind`): `I` (immediata), `D` (differita), `S` (split payment)
- **OriginalDocumentType** (`ei_data.original_document_type`): `ordine, contratto, convenzione`
- **ReceiptType** (corrispettivi): `till_receipt, sales_receipt`
- **F24Status**: `paid, not_paid, reversed`
- **CashbookEntryKind**: `cashbook, issued_document, received_document, tax, receipt, ts_pay` — **CashbookEntryType**: `in, out`
- **FattureInCloudPlanType**: `trial, standard, premium, premium_plus, complete`
- **EmailStatus**: `sending, pending, sent`
- **ShowTotalsMode**: `none, nets, all`
- **TemplateType**: `standard, delivery_note, accompanying_invoice`
- **UserCompanyRole**: `master, subaccount, employee`

## IssuedDocument (campi chiave, 86 totali)

Struttura minima Create: `{"data": {"type": "...", "entity": {...}, "items_list": [...], "payments_list": [...]}}`

- Identità: `id` (mai in Create), `type`, `number` (se omesso → progressivo automatico), `numeration` (sezionale, es. `"/fatt"`; non disponibile per delivery_note), `date` (default oggi), `year`
- Descrizioni: `subject` (interno, non in PDF), `visible_subject` (in PDF), `notes`, `rc_center` (centro ricavo; per supplier_order è centro di costo)
- `currency` (`{"id":"EUR"}`), `language` (`{"code":"it","name":"Italiano"}`)
- Contributi/ritenute: `rivalsa`, `cassa`, `cassa2` (+ varianti `*_taxable`, `amount_*` read-only), `withholding_tax` + `withholding_tax_taxable`, `other_withholding_tax`, `amount_enasarco_taxable`, `stamp_duty`
- Flag: `use_gross_prices`, `use_split_payment`, `e_invoice`, `delivery_note`, `accompanying_invoice`, `is_marked`, `locked` (documento non modificabile)
- E-invoice: `ei_data` (oggetto), `ei_raw`, `ei_status` (read-only, richiede fieldset detailed), `ei_cassa_type`, `ei_cassa2_type`, `ei_withholding_tax_causal`, `ei_other_withholding_tax_type/causal`
- Totali (READ-ONLY, calcolati dal server): `amount_net`, `amount_vat`, `amount_gross`, `amount_rivalsa`, `amount_withholding_tax`, ... — usa gli endpoint `/totals` per verificare in anticipo
- `amount_due_discount`: sconto/maggiorazione sul totale
- PDF/allegati: `template`/`delivery_note_template`/`acc_inv_template` (`{"id":...}`), `h_margins`, `v_margins`, `show_payments`, `show_payment_method`, `show_totals`, `show_tspay_button`, `show_notification_button`, `url`/`dn_url`/`ai_url`/`attachment_url` (temporanei! 7 giorni), `attachment_token` (write-only, da uploadIssuedDocumentAttachment)
- DDT allegato: `dn_number`, `dn_date`, `dn_ai_packages_number`, `dn_ai_weight`, `dn_ai_causal`, `dn_ai_destination`, `dn_ai_transporter`, `dn_ai_notes`
- Altro: `payment_method` (`{"id":...}`), `next_due_date`, `seen_date`, `extra_data` (campi Sistema Tessera Sanitaria), `price_list_id`, `created_at`, `updated_at`

### IssuedDocumentItemsListItem
`id, product_id, code, name, category, description, qty, measure, net_price, gross_price, vat: {"id": N}, not_taxable, apply_withholding_taxes, discount (%), discount_highlight, in_dn, stock, ei_raw`
- `net_price` o `gross_price` a seconda di `use_gross_prices` del documento.
- `vat.id`: da listVatTypes (id 0 = 22% standard sugli account tipici, ma VERIFICA sempre via API — gli id custom variano per company).
- `not_taxable: true` → l'importo non conta come ricavo.
- `stock: true` → movimenta il magazzino.

### IssuedDocumentPaymentsListItem
`id, due_date, amount, status (not_paid|paid|reversed), payment_account: {"id":...}, paid_date (solo se paid), payment_terms: {days, type}, ei_raw`
- ⚠️ La somma degli `amount` deve corrispondere al totale documento (usa /totals per calcolarlo).
- ⚠️ `status: "paid"` RICHIEDE `payment_account.id` esistente, altrimenti errore.

## Entity (cliente/fornitore, anche embedded nel documento)

`id, code, name, type, first_name, last_name, contact_person, vat_number, tax_code, address_street, address_postal_code, address_city, address_province, address_extra, country, country_iso, email, certified_email (PEC), phone, fax, notes, created_at, updated_at`
Solo client: `default_payment_terms, default_payment_terms_type, default_vat, default_payment_method, bank_name, bank_iban, bank_swift_code, shipping_address, e_invoice (bool), ei_code (codice destinatario SDI), has_intent_declaration, intent_declaration_protocol_number/date`

⚠️ **Nessun autocompletamento**: anche passando `entity.id` di un cliente esistente, i campi che vuoi far comparire sul documento (nome, indirizzo, P.IVA...) vanno inseriti esplicitamente nel body. FIC non li copia dall'anagrafica. Stesso discorso per i prodotti (`product_id` non popola nome/prezzo).

## ReceivedDocument (documento ricevuto / spesa)

`id, type, entity (fornitore), date, category, description, amount_net, amount_vat, amount_withholding_tax, amount_other_withholding_tax, amount_gross (RO), amortization, rc_center, invoice_number, is_marked, is_detailed (ha righe), e_invoice (RO), next_due_date (RO), currency, tax_deductibility (%), vat_deductibility (%), items_list, payments_list, attachment_url/attachment_preview_url (RO temporanei), attachment_token (WO), auto_calculate, locked, created_at, updated_at, ei_reception_date (RO, fieldset fic_view), is_from_pending_expenses (RO, fieldset fic_view)`
- `auto_calculate: true` → totale calcolato dalle righe; se false, totali item e pagamenti possono differire.
- Items: `id, product_id, code, name, measure, net_price, category, qty, vat, stock, deductibility_vat_percentage`
- Payments: `id, amount, due_date, paid_date, payment_terms, status, payment_account`
- **Pending Received Documents** (`/received_documents/pending`): fatture passive arrivate da SDI/mail/browser non ancora registrate.

## Product

`id, name, code, net_price, gross_price, use_gross_price, default_vat, net_cost, measure, description, category, notes, in_stock, stock_initial, stock_current (RO), average_cost, average_price, created_at, updated_at`

## VatType

`id, value (RO %), description, notes, e_invoice (usabile in e-fattura), ei_type (Natura es. N1..N7), ei_description, editable (RO), is_disabled, default`
- Recupero: `GET /c/{id}/info/vat_types` (scope `settings:r`). Creazione custom: `POST /c/{id}/settings/vat_types`.

## PaymentMethod / PaymentAccount

- PaymentMethod: `id, name, type (standard|riba), is_default, default_payment_account, details[] (title/description), bank_iban, bank_name, bank_beneficiary, ei_payment_method (codice MP FatturaPA)`
- PaymentAccount: `id, name, type (standard|bank), iban, sia, fic (RO)` — lista via `GET /c/{id}/info/payment_accounts`.

## TaxProfile (`GET /c/{id}/settings/tax_profile`)

`company_type, company_subtype, profession, regime (es. forfettario), rivalsa_name, default_rivalsa, cassa_name, default_cassa(+taxable), cassa2..., default_withholding_tax(+taxable), default_other_withholding_tax, enasarco, enasarco_type, contributions_percentage, profit_coefficient, med (Sistema TS attivo), default_vat`
Utile per capire il regime fiscale della company prima di generare documenti.

## Altre risorse

- **Receipt (corrispettivo)**: `date, number, numeration, amount_net/vat/gross, use_gross_prices, type, description, rc_center, payment_account, items_list`; `GET /receipts/monthly_totals` per i totali mensili.
- **F24**: `due_date, status, payment_account, amount, description, attachment_token/url`.
- **CashbookEntry (prima nota)**: `date, description, kind, type (in|out), entity_name, document, amount_in/payment_account_in, amount_out/payment_account_out`. Id STRINGA.
- **ArchiveDocument**: `date, description, category, attachment_token (OBBLIGATORIO in create), attachment_url`.
- **PriceLists**: `GET /price_lists` e `GET /price_lists/{id}/items`; sul documento si applica con `price_list_id`.
- **Info endpoints** (senza scope): countries, detailed_countries, cities, languages, templates, currencies, measures, dn_causals; per company: payment_methods, payment_accounts, revenue_centers, cost_centers, product_categories, received_document_categories, archive_categories.
- **Cestino (bin)**: documenti eliminati finiscono in `/bin/issued_documents` e `/bin/received_documents`; `POST .../recover` per ripristinare, `DELETE` per eliminazione definitiva.
