#!/usr/bin/env python3
"""
Rigenera skills/fatture-in-cloud/references/endpoints.md dalla spec OpenAPI
ufficiale di Fatture in Cloud.

Uso:
    pip install pyyaml requests
    python scripts/update_endpoints.py

La spec viene scaricata da:
    https://raw.githubusercontent.com/fattureincloud/openapi-fattureincloud/master/openapi-enriched.yaml

Se la versione della spec cambia, aggiorna anche il numero di versione citato
in SKILL.md e ricontrolla a mano i file references/ scritti a mano (modelli,
fattura elettronica, ecc.): questo script tocca SOLO endpoints.md.
"""

import pathlib
import sys

import requests
import yaml

SPEC_URL = (
    "https://raw.githubusercontent.com/fattureincloud/openapi-fattureincloud/"
    "master/openapi-enriched.yaml"
)
OUT = (
    pathlib.Path(__file__).resolve().parent.parent
    / "plugins"
    / "fatture-in-cloud"
    / "skills"
    / "fatture-in-cloud"
    / "references"
    / "endpoints.md"
)

FOOTER = """
## Parametri comuni (query string)

| Parametro | Dove | Note |
|---|---|---|
| `page` | list | default 1 |
| `per_page` | list | **default 5** (!), min 1, max 100 — impostalo sempre esplicitamente |
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

- Get/Create/Modify incapsulano la risorsa in `{"data": {...}}`; anche i body Create/Modify vanno in `{"data": {...}}` (Create Issued Document accetta anche `"options": {...}`, es. `dry_run`).
- Le List restituiscono paginazione stile Laravel: `current_page`, `data[]`, `last_page`, `next_page_url`, `per_page`, `total`, ecc. Stop quando `next_page_url == null`.
- Ogni risposta include gli header `RateLimit-*` (e `Retry-After` su 403/429).
"""


def main() -> int:
    print(f"Scarico {SPEC_URL} ...")
    spec = yaml.safe_load(requests.get(SPEC_URL, timeout=60).text)
    version = spec["info"]["version"]
    print(f"Spec versione {version}")

    by_tag: dict[str, list[tuple[str, str, str, str, list[str]]]] = {}
    for path, ops in spec["paths"].items():
        for method, op in ops.items():
            if method not in ("get", "post", "put", "delete", "patch"):
                continue
            scopes: list[str] = []
            for sec in op.get("security", []):
                scopes += sec.get("OAuth2AuthenticationCodeFlow", [])
            tag = (op.get("tags") or ["Other"])[0]
            by_tag.setdefault(tag, []).append(
                (method.upper(), path, op.get("operationId", ""), op.get("summary", ""), scopes)
            )

    total = sum(len(v) for v in by_tag.values())
    lines = [
        f"# Endpoint API v2 — Riferimento completo (spec {version})",
        "",
        "Base URL: `https://api-v2.fattureincloud.it`. Tutti i path `/c/{company_id}/...` sono company-scoped.",
        "",
        "Scope vuoto = nessuno scope specifico richiesto (basta un token valido con accesso alla company).",
        "",
        f"_Generato automaticamente da `scripts/update_endpoints.py` — {total} operazioni._",
    ]
    for tag in sorted(by_tag):
        lines += ["", f"## {tag}", "", "| Metodo | Path | operationId | Descrizione | Scope |", "|---|---|---|---|---|"]
        for method, path, oid, summary, scopes in by_tag[tag]:
            lines.append(f"| {method} | `{path}` | {oid} | {summary} | {' / '.join(scopes) or '—'} |")

    OUT.write_text("\n".join(lines) + "\n" + FOOTER, encoding="utf-8")
    print(f"Scritto {OUT} ({total} operazioni)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
