# Agent Skill — Fatture in Cloud API v2

Una **skill** per agent (Claude Code, Claude desktop/web, e qualsiasi agent che legga markdown) che dà al modello una visione d'insieme corretta delle [API v2 di Fatture in Cloud](https://developers.fattureincloud.it): endpoint, scope, modelli, linguaggio di query, flusso della fattura elettronica, rate limit e — soprattutto — le trappole che generano la maggior parte degli errori di integrazione.

> Progetto **non ufficiale**, non affiliato a Fatture in Cloud / TeamSystem S.p.A. La documentazione ufficiale resta la fonte di verità.

## Installazione

### Claude Code / Claude desktop (consigliato — due comandi)

```
/plugin marketplace add Clinova-SRL/agent-skill-fatture-in-cloud
/plugin install fatture-in-cloud@clinova
```

Se l'installazione risponde `Run /reload-plugins to activate.`, lancia `/reload-plugins`. Da terminale, senza sessione interattiva:

```bash
claude plugin marketplace add Clinova-SRL/agent-skill-fatture-in-cloud
claude plugin install fatture-in-cloud@clinova
```

Aggiornamenti: `/plugin marketplace update clinova`.

### Claude web / app (upload manuale)

Scarica `fatture-in-cloud.skill` dall'ultima [release](../../releases) e caricalo dalle impostazioni delle skill. Per ricostruirlo da sorgente:

```bash
cd plugins/fatture-in-cloud/skills
zip -r ../../../fatture-in-cloud.skill fatture-in-cloud
```

### Altri agent

I file sono markdown puro: copiali dove il tuo agent cerca le skill (es. `~/.claude/skills/`), passali come contesto o adattali al formato del tuo framework.

## Perché esiste

Gli LLM conoscono le API di Fatture in Cloud a spizzichi e sbagliano quasi sempre le stesse cose: `per_page` che di default è 50 (non 5), `fieldset=detailed` necessario per vedere `items_list`/`payments_list`/`ei_status`, il fatto che creare una e-fattura non la invii all'SDI, il PUT che sostituisce integralmente le liste, gli URL dei PDF che scadono dopo 7 giorni. Questa skill mette quelle regole nero su bianco insieme al riferimento completo generato dalla spec OpenAPI ufficiale.

## Contenuto

```
.claude-plugin/marketplace.json            # catalogo del marketplace
plugins/fatture-in-cloud/
├── .claude-plugin/plugin.json             # manifest del plugin
└── skills/fatture-in-cloud/
    ├── SKILL.md                           # mappa dell'API, 14 regole non negoziabili, workflow
    └── references/
        ├── endpoints.md                   # 123 operazioni per tag, con operationId e scope (generato)
        ├── autenticazione.md              # OAuth2, token e durate, refresh rotante, scope
        ├── query-filtri-paginazione.md    # linguaggio q, campi filtrabili per metodo, fields/fieldset
        ├── modelli.md                     # modelli ed enum (IssuedDocument, Entity, ...)
        ├── fattura-elettronica.md         # ei_data, ei_raw, dry_run, stati ei_status, bollo
        ├── webhooks.md                    # eventi, subscription, verifica, scadenza
        └── errori-limiti.md               # 401/403/422/429, rate limit, plan limits, retry
scripts/update_endpoints.py                # rigenera endpoints.md dalla spec ufficiale
```

## Manutenzione

`references/endpoints.md` si rigenera dalla spec ufficiale (MIT):

```bash
pip install pyyaml requests
python scripts/update_endpoints.py
```

Lo script tocca solo `endpoints.md`; gli altri file sono scritti a mano dalle guide ufficiali e vanno rivisti manualmente quando l'API cambia. La versione della spec su cui è tarata la skill è indicata in `SKILL.md`.

Prima di pubblicare un aggiornamento: bump della `version` in `plugin.json` (senza, gli utenti restano sulla copia in cache) e `claude plugin validate .` dalla root del repo.

## Contribuire

Se trovi un comportamento dell'API che contraddice la skill, apri una issue con la chiamata e la risposta reale (rimuovi token, P.IVA e dati personali). Le regole in `SKILL.md` valgono più di tutto il resto: aggiungerne una verificata sul campo è il contributo più utile.

## Licenza e attribuzione

Codice e testi di questo repo: **MIT** (vedi [LICENSE](LICENSE)).

`references/endpoints.md` è derivato dalla [OpenAPI Specification ufficiale di Fatture in Cloud](https://github.com/fattureincloud/openapi-fattureincloud), rilasciata sotto licenza MIT — vedi [NOTICE](NOTICE). Gli altri file sono sintesi originali della documentazione pubblica, non riproduzioni.

"Fatture in Cloud" è un marchio di TeamSystem S.p.A., citato a soli fini descrittivi.
