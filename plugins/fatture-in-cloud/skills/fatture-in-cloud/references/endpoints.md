# Endpoint API v2 — Riferimento completo (spec 2.1.8)

Base URL: `https://api-v2.fattureincloud.it`. Tutti i path `/c/{company_id}/...` sono company-scoped.

Scope vuoto = nessuno scope specifico richiesto (basta un token valido con accesso alla company).

_Generato automaticamente da `scripts/update_endpoints.py` — 123 operazioni._

## Archive

| Metodo | Path | operationId | Descrizione | Scope |
|---|---|---|---|---|
| GET | `/c/{company_id}/archive` | listArchiveDocuments | List Archive Documents | archive:r |
| POST | `/c/{company_id}/archive` | createArchiveDocument | Create Archive Document | archive:a |
| GET | `/c/{company_id}/archive/{document_id}` | getArchiveDocument | Get Archive Document | archive:r |
| PUT | `/c/{company_id}/archive/{document_id}` | modifyArchiveDocument | Modify Archive Document | archive:a |
| DELETE | `/c/{company_id}/archive/{document_id}` | deleteArchiveDocument | Delete Archive Document | archive:a |
| POST | `/c/{company_id}/archive/attachment` | uploadArchiveDocumentAttachment | Upload Archive Document Attachment | archive:a |

## Cashbook

| Metodo | Path | operationId | Descrizione | Scope |
|---|---|---|---|---|
| GET | `/c/{company_id}/cashbook` | listCashbookEntries | List Cashbook Entries | cashbook:r |
| POST | `/c/{company_id}/cashbook` | createCashbookEntry | Create Cashbook Entry | cashbook:a |
| GET | `/c/{company_id}/cashbook/{document_id}` | getCashbookEntry | Get Cashbook Entry | cashbook:r |
| PUT | `/c/{company_id}/cashbook/{document_id}` | modifyCashbookEntry | Modify Cashbook Entry | cashbook:a |
| DELETE | `/c/{company_id}/cashbook/{document_id}` | deleteCashbookEntry | Delete Cashbook Entry | cashbook:a |

## Clients

| Metodo | Path | operationId | Descrizione | Scope |
|---|---|---|---|---|
| GET | `/c/{company_id}/entities/clients` | listClients | List Clients | entity.clients:r |
| POST | `/c/{company_id}/entities/clients` | createClient | Create Client | entity.clients:a |
| GET | `/c/{company_id}/entities/clients/{client_id}` | getClient | Get Client | entity.clients:r |
| PUT | `/c/{company_id}/entities/clients/{client_id}` | modifyClient | Modify Client | entity.clients:a |
| DELETE | `/c/{company_id}/entities/clients/{client_id}` | deleteClient | Delete Client | entity.clients:a |
| GET | `/c/{company_id}/entities/clients/info` | getClientInfo | Get Client info | entity.clients:r |

## Companies

| Metodo | Path | operationId | Descrizione | Scope |
|---|---|---|---|---|
| GET | `/c/{company_id}/company/info` | getCompanyInfo | Get Company Info — nome, email, piano, licenza, permessi. ⚠️ **niente `vat_number`**: la partita IVA sta in `/user/companies` | — |
| GET | `/c/{company_id}/company/plan_usage` | getCompanyPlanUsage | Get Company Plan Usage | — |

## Emails

| Metodo | Path | operationId | Descrizione | Scope |
|---|---|---|---|---|
| GET | `/c/{company_id}/emails` | listEmails | List Emails | — |

## Info

| Metodo | Path | operationId | Descrizione | Scope |
|---|---|---|---|---|
| GET | `/info/countries` | listCountries | List Countries | — |
| GET | `/info/detailed_countries` | listDetailedCountries | List Detailed Countries | — |
| GET | `/info/cities` | listCities | List Cities | — |
| GET | `/info/languages` | listLanguages | List Languages | — |
| GET | `/info/templates` | listDefaultTemplates | List Default Templates | — |
| GET | `/info/currencies` | listCurrencies | List Currencies | — |
| GET | `/info/measures` | listUnitsOfMeasure | List Units of Measure | — |
| GET | `/info/dn_causals` | listDeliveryNotesDefaultCausals | List Delivery Notes Default Causals | — |
| GET | `/c/{company_id}/info/vat_types` | listVatTypes | List Vat Types | settings:r |
| GET | `/c/{company_id}/info/payment_methods` | listPaymentMethods | List Payment Methods | — |
| GET | `/c/{company_id}/info/payment_accounts` | listPaymentAccounts | List Payment Accounts | — |
| GET | `/c/{company_id}/info/revenue_centers` | listRevenueCenters | List Revenue Centers | — |
| GET | `/c/{company_id}/info/cost_centers` | listCostCenters | List Cost Centers | — |
| GET | `/c/{company_id}/info/product_categories` | listProductCategories | List Product Categories | — |
| GET | `/c/{company_id}/info/received_document_categories` | listReceivedDocumentCategories | List Received Document Categories | — |
| GET | `/c/{company_id}/info/archive_categories` | listArchiveCategories | List Archive Categories | — |

## Issued Documents

| Metodo | Path | operationId | Descrizione | Scope |
|---|---|---|---|---|
| GET | `/c/{company_id}/issued_documents` | listIssuedDocuments | List Issued Documents | issued_documents.invoices:r / issued_documents.credit_notes:r / issued_documents.receipts:r / issued_documents.orders:r / issued_documents.quotes:r / issued_documents.proformas:r / issued_documents.delivery_notes:r |
| POST | `/c/{company_id}/issued_documents` | createIssuedDocument | Create Issued Document | issued_documents.invoices:a / issued_documents.credit_notes:a / issued_documents.receipts:a / issued_documents.orders:a / issued_documents.quotes:a / issued_documents.proformas:a / issued_documents.delivery_notes:a |
| GET | `/c/{company_id}/issued_documents/{document_id}` | getIssuedDocument | Get Issued Document | issued_documents.invoices:r / issued_documents.credit_notes:r / issued_documents.receipts:r / issued_documents.orders:r / issued_documents.quotes:r / issued_documents.proformas:r / issued_documents.delivery_notes:r |
| PUT | `/c/{company_id}/issued_documents/{document_id}` | modifyIssuedDocument | Modify Issued Document | issued_documents.invoices:a / issued_documents.credit_notes:a / issued_documents.receipts:a / issued_documents.orders:a / issued_documents.quotes:a / issued_documents.proformas:a / issued_documents.delivery_notes:a |
| DELETE | `/c/{company_id}/issued_documents/{document_id}` | deleteIssuedDocument | Delete Issued Document | issued_documents.invoices:a / issued_documents.credit_notes:a / issued_documents.receipts:a / issued_documents.orders:a / issued_documents.quotes:a / issued_documents.proformas:a / issued_documents.delivery_notes:a |
| POST | `/c/{company_id}/issued_documents/totals` | getNewIssuedDocumentTotals | Get New Issued Document Totals | — |
| POST | `/c/{company_id}/issued_documents/{document_id}/totals` | getExistingIssuedDocumentTotals | Get Existing Issued Document Totals | — |
| POST | `/c/{company_id}/issued_documents/attachment` | uploadIssuedDocumentAttachment | Upload Issued Document Attachment | — |
| DELETE | `/c/{company_id}/issued_documents/{document_id}/attachment` | deleteIssuedDocumentAttachment | Delete Issued Document Attachment | — |
| GET | `/c/{company_id}/issued_documents/info` | getIssuedDocumentPreCreateInfo | Get Issued Document Pre-Create Info | — |
| GET | `/c/{company_id}/issued_documents/{document_id}/email` | getEmailData | Get Email Data | issued_documents.invoices:r / issued_documents.credit_notes:r / issued_documents.receipts:r / issued_documents.orders:r / issued_documents.quotes:r / issued_documents.proformas:r / issued_documents.delivery_notes:r |
| POST | `/c/{company_id}/issued_documents/{document_id}/email` | scheduleEmail | Schedule Email | issued_documents.invoices:r / issued_documents.credit_notes:r / issued_documents.receipts:r / issued_documents.orders:r / issued_documents.quotes:r / issued_documents.proformas:r / issued_documents.delivery_notes:r |
| GET | `/c/{company_id}/issued_documents/transform` | transformIssuedDocument | Transform Issued Document | — |
| GET | `/c/{company_id}/issued_documents/join` | joinIssuedDocuments | Join Issued Documents | — |
| GET | `/c/{company_id}/bin/issued_documents` | ListBinIssuedDocuments | Get Bin Issued Documents List | issued_documents.invoices:r / issued_documents.credit_notes:r / issued_documents.receipts:r / issued_documents.orders:r / issued_documents.quotes:r / issued_documents.proformas:r |
| GET | `/c/{company_id}/bin/issued_documents/{document_id}` | GetBinIssuedDocument | Get Bin Issued Documents List | issued_documents.invoices:r / issued_documents.credit_notes:r / issued_documents.receipts:r / issued_documents.orders:r / issued_documents.quotes:r / issued_documents.proformas:r |
| DELETE | `/c/{company_id}/bin/issued_documents/{document_id}` | DeleteBinIssuedDocument | Delete Bin Issued Document | — |
| POST | `/c/{company_id}/bin/issued_documents/{document_id}/recover` | RecoverBinIssuedDocument | Recover Issued Document From The Bin | — |

## Issued e-invoices

| Metodo | Path | operationId | Descrizione | Scope |
|---|---|---|---|---|
| POST | `/c/{company_id}/issued_documents/{document_id}/e_invoice/send` | sendEInvoice | Send E-Invoice | — |
| GET | `/c/{company_id}/issued_documents/{document_id}/e_invoice/xml_verify` | verifyEInvoiceXml | Verify E-Invoice XML | — |
| GET | `/c/{company_id}/issued_documents/{document_id}/e_invoice/xml` | getEInvoiceXml | Get E-Invoice XML | — |
| GET | `/c/{company_id}/issued_documents/{document_id}/e_invoice/error_reason` | getEInvoiceRejectionReason | Get E-Invoice Rejection Reason | — |

## PriceLists

| Metodo | Path | operationId | Descrizione | Scope |
|---|---|---|---|---|
| GET | `/c/{company_id}/price_lists` | getPriceLists | Get PriceLists | — |
| GET | `/c/{company_id}/price_lists/{price_list_id}/items` | getPriceListItems | Get PriceList Items List | — |

## Products

| Metodo | Path | operationId | Descrizione | Scope |
|---|---|---|---|---|
| GET | `/c/{company_id}/products` | listProducts | List Products | products:r |
| POST | `/c/{company_id}/products` | createProduct | Create Product | products:a |
| GET | `/c/{company_id}/products/{product_id}` | getProduct | Get Product | products:r |
| PUT | `/c/{company_id}/products/{product_id}` | modifyProduct | Modify Product | products:a |
| DELETE | `/c/{company_id}/products/{product_id}` | deleteProduct | Delete Product | products:a |

## Receipts

| Metodo | Path | operationId | Descrizione | Scope |
|---|---|---|---|---|
| GET | `/c/{company_id}/receipts` | listReceipts | List Receipts | receipts:r |
| POST | `/c/{company_id}/receipts` | createReceipt | Create Receipt | receipts:a |
| GET | `/c/{company_id}/receipts/{document_id}` | getReceipt | Get Receipt | receipts:r |
| PUT | `/c/{company_id}/receipts/{document_id}` | modifyReceipt | Modify Receipt | receipts:a |
| DELETE | `/c/{company_id}/receipts/{document_id}` | deleteReceipt | Delete Receipt | receipts:a |
| GET | `/c/{company_id}/receipts/info` | getReceiptPreCreateInfo | Get Receipt Pre-Create Info | receipts:r |
| GET | `/c/{company_id}/receipts/monthly_totals` | getReceiptsMonthlyTotals | Get Receipts Monthly Totals | receipts:r |

## Received Documents

| Metodo | Path | operationId | Descrizione | Scope |
|---|---|---|---|---|
| GET | `/c/{company_id}/received_documents` | listReceivedDocuments | List Received Documents | received_documents:r / stock:r |
| POST | `/c/{company_id}/received_documents` | createReceivedDocument | Create Received Document | received_documents:a / stock:a |
| GET | `/c/{company_id}/received_documents/{document_id}` | getReceivedDocument | Get Received Document | received_documents:r / stock:r |
| PUT | `/c/{company_id}/received_documents/{document_id}` | modifyReceivedDocument | Modify Received Document | received_documents:a / stock:a |
| DELETE | `/c/{company_id}/received_documents/{document_id}` | deleteReceivedDocument | Delete Received Document | received_documents:a / stock:a |
| GET | `/c/{company_id}/received_documents/pending` | listPendingReceivedDocuments | List Pending Received Documents | received_documents:r |
| GET | `/c/{company_id}/received_documents/pending/{document_id}` | getPendingReceivedDocument | Get Pending Received Document | received_documents:r |
| POST | `/c/{company_id}/received_documents/totals` | getNewReceivedDocumentTotals | Get New Received Document Totals | received_documents:a / stock:a |
| POST | `/c/{company_id}/received_documents/{document_id}/totals` | getExistingReceivedDocumentTotals | Get Existing Received Document Totals | received_documents:a / stock:a |
| POST | `/c/{company_id}/received_documents/attachment` | uploadReceivedDocumentAttachment | Upload Received Document Attachment | received_documents:a / stock:a |
| DELETE | `/c/{company_id}/received_documents/{document_id}/attachment` | deleteReceivedDocumentAttachment | Delete Received Document Attachment | received_documents:a / stock:a |
| GET | `/c/{company_id}/received_documents/info` | getReceivedDocumentPreCreateInfo | Get Received Document Pre-Create Info | received_documents:r |
| GET | `/c/{company_id}/bin/received_documents` | ListBinReceivedDocuments | Get Bin Received Documents List | — |
| GET | `/c/{company_id}/bin/received_documents/{document_id}` | GetBinReceivedDocument | Get Bin Received Documents List | — |
| DELETE | `/c/{company_id}/bin/received_documents/{document_id}` | DeleteBinReceivedDocument | Delete Bin Received Document | — |
| POST | `/c/{company_id}/bin/received_documents/{document_id}/recover` | RecoverBinReceivedDocument | Recover Received Document From The Bin | — |

## Settings

| Metodo | Path | operationId | Descrizione | Scope |
|---|---|---|---|---|
| POST | `/c/{company_id}/settings/payment_methods` | createPaymentMethod | Create Payment Method | settings:a |
| GET | `/c/{company_id}/settings/payment_methods/{payment_method_id}` | getPaymentMethod | Get Payment Method | — |
| PUT | `/c/{company_id}/settings/payment_methods/{payment_method_id}` | modifyPaymentMethod | Modify Payment Method | settings:a |
| DELETE | `/c/{company_id}/settings/payment_methods/{payment_method_id}` | deletePaymentMethod | Delete Payment Method | settings:a |
| POST | `/c/{company_id}/settings/payment_accounts` | createPaymentAccount | Create Payment Account | settings:a |
| GET | `/c/{company_id}/settings/tax_profile` | getTaxProfile | Get Tax Profile | settings:r |
| GET | `/c/{company_id}/settings/payment_accounts/{payment_account_id}` | getPaymentAccount | Get Payment Account | — |
| PUT | `/c/{company_id}/settings/payment_accounts/{payment_account_id}` | modifyPaymentAccount | Modify Payment Account | settings:a |
| DELETE | `/c/{company_id}/settings/payment_accounts/{payment_account_id}` | deletePaymentAccount | Delete Payment Account | settings:a |
| POST | `/c/{company_id}/settings/vat_types` | createVatType | Create Vat Type | settings:a |
| GET | `/c/{company_id}/settings/templates` | listTemplates | List Templates | — |
| GET | `/c/{company_id}/settings/templates/{template_id}` | getTemplate | Get Template | — |
| GET | `/c/{company_id}/settings/vat_types/{vat_type_id}` | getVatType | Get Vat Type | — |
| PUT | `/c/{company_id}/settings/vat_types/{vat_type_id}` | modifyVatType | Modify Vat Type | settings:a |
| DELETE | `/c/{company_id}/settings/vat_types/{vat_type_id}` | deleteVatType | Delete Vat Type | settings:a |

## Suppliers

| Metodo | Path | operationId | Descrizione | Scope |
|---|---|---|---|---|
| GET | `/c/{company_id}/entities/suppliers` | listSuppliers | List Suppliers | entity.suppliers:r |
| POST | `/c/{company_id}/entities/suppliers` | createSupplier | Create Supplier | entity.suppliers:a |
| GET | `/c/{company_id}/entities/suppliers/{supplier_id}` | getSupplier | Get Supplier | entity.suppliers:r |
| PUT | `/c/{company_id}/entities/suppliers/{supplier_id}` | modifySupplier | Modify Supplier | entity.suppliers:a |
| DELETE | `/c/{company_id}/entities/suppliers/{supplier_id}` | deleteSupplier | Delete Supplier | entity.suppliers:a |

## Taxes

| Metodo | Path | operationId | Descrizione | Scope |
|---|---|---|---|---|
| GET | `/c/{company_id}/taxes` | listF24 | List F24 | taxes:r |
| POST | `/c/{company_id}/taxes` | createF24 | Create F24 | taxes:a |
| GET | `/c/{company_id}/taxes/{document_id}` | getF24 | Get F24 | taxes:r |
| PUT | `/c/{company_id}/taxes/{document_id}` | modifyF24 | Modify F24 | taxes:a |
| DELETE | `/c/{company_id}/taxes/{document_id}` | deleteF24 | Delete F24 | taxes:a |
| POST | `/c/{company_id}/taxes/attachment` | uploadF24Attachment | Upload F24 Attachment | taxes:a |
| DELETE | `/c/{company_id}/taxes/{document_id}/attachment` | deleteF24Attachment | Delete F24 Attachment | taxes:a |

## User

| Metodo | Path | operationId | Descrizione | Scope |
|---|---|---|---|---|
| GET | `/user/info` | getUserInfo | Get User Info | — |
| GET | `/user/companies` | listUserCompanies | List User Companies — per ogni azienda dà anche **`vat_number` e `tax_code`**: è l'unico posto dove stanno | — |

## Webhooks

| Metodo | Path | operationId | Descrizione | Scope |
|---|---|---|---|---|
| GET | `/c/{company_id}/subscriptions` | listWebhooksSubscriptions | List Webhooks Subscriptions | — |
| POST | `/c/{company_id}/subscriptions` | CreateWebhooksSubscription | Create a Webhook Subscription | — |
| GET | `/c/{company_id}/subscriptions/{subscription_id}` | getWebhooksSubscription | Get Webhooks Subscription | — |
| PUT | `/c/{company_id}/subscriptions/{subscription_id}` | modifyWebhooksSubscription | Modify Webhooks Subscription | — |
| DELETE | `/c/{company_id}/subscriptions/{subscription_id}` | deleteWebhooksSubscription | Delete Webhooks Subscription | — |
| POST | `/c/{company_id}/subscriptions/{subscription_id}/verify` | verifyWebhooksSubscription | Verify Webhooks Subscription | — |

## Parametri comuni (query string)

| Parametro | Dove | Note |
|---|---|---|
| `page` | list | default 1 |
| `per_page` | list | **default 50** (verificato 12/08/2026), min 1, max 100 — impostalo sempre esplicitamente |
| `sort` | list | campi separati da virgola, prefisso `-` per discendente (es. `sort=-date,number`) |
| `q` | list | filtro SQL-like URL-encoded (vedi query-filtri-paginazione.md) |
| `fields` | list/get | lista campi separati da virgola da includere nella risposta |
| `fieldset` | list/get | `basic` (default), `detailed`, `fic_view` — molti campi (es. `ei_status`, `items_list`, `payments_list`) compaiono SOLO con `detailed` |
| `type` | issued/received docs | seleziona il tipo documento |
| `include_attachment` | getEInvoiceXml | include allegato nell'XML |

## Parametri di transform e join

- `GET /c/{company_id}/issued_documents/transform` — query: `original_document_id`, `new_type`, `type` (tipo attuale), `e_invoice`, `transform_keep_copy`.
- `GET /c/{company_id}/issued_documents/join` — query: `ids` (separati da virgola), `group`, `type`.

## Risposte

- Get/Create/Modify incapsulano la risorsa in `{"data": {...}}`; anche i body Create/Modify vanno in `{"data": {...}}` (Create Issued Document accetta anche `"options": {...}`).

  🔴 **`dry_run` è documentato solo su `e_invoice/send`, non sulla Create.** Nella specifica OpenAPI 2.1.8 la stringa `dry_run` non compare **nemmeno una volta**: l'unica fonte è la documentazione dell'invio a SDI. Non dare per scontato che `options.dry_run` renda innocuo un `POST /issued_documents` — quella chiamata crea un documento **vero**, con un numero vero, nella numerazione vera. Se l'ipotesi è sbagliata non te ne accorgi da un errore: te ne accorgi da una fattura da stornare con una nota di credito. Per provare senza rischi si apre un secondo account FIC con un'azienda finta: una sandbox non esiste.
- Le List restituiscono paginazione stile Laravel: `current_page`, `data[]`, `last_page`, `next_page_url`, `per_page`, `total`, ecc. Stop quando `next_page_url == null`.
- Ogni risposta include gli header `RateLimit-*` (e `Retry-After` su 403/429).
