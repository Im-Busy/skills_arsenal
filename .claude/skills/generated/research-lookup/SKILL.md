---
name: research-lookup
description: "Skill for the Research-lookup area of skills_arsenal. 18 symbols across 3 files."
---

# Research-lookup

18 symbols | 3 files | Cohesion: 79%

## When to Use

- Working with code in `universal-skills/`
- Understanding how example_automatic_selection, example_manual_override, format_response work
- Modifying research-lookup-related functionality

## Key Files

| File | Symbols |
|------|---------|
| `universal-skills/research-lookup/research_lookup.py` | _select_backend, lookup, _get_chat_client, _parallel_lookup, _extract_basis_citations (+7) |
| `universal-skills/research-lookup/examples.py` | example_automatic_selection, example_manual_override, example_batch_queries |
| `universal-skills/research-lookup/lookup.py` | format_response, _detect_venue_tier, main |

## Entry Points

Start here when exploring this area:

- **`example_automatic_selection`** (Function) — `universal-skills/research-lookup/examples.py:15`
- **`example_manual_override`** (Function) — `universal-skills/research-lookup/examples.py:41`
- **`format_response`** (Function) — `universal-skills/research-lookup/lookup.py:16`
- **`main`** (Function) — `universal-skills/research-lookup/lookup.py:148`
- **`example_batch_queries`** (Function) — `universal-skills/research-lookup/examples.py:66`

## Key Symbols

| Symbol | Type | File | Line |
|--------|------|------|------|
| `example_automatic_selection` | Function | `universal-skills/research-lookup/examples.py` | 15 |
| `example_manual_override` | Function | `universal-skills/research-lookup/examples.py` | 41 |
| `format_response` | Function | `universal-skills/research-lookup/lookup.py` | 16 |
| `main` | Function | `universal-skills/research-lookup/lookup.py` | 148 |
| `example_batch_queries` | Function | `universal-skills/research-lookup/examples.py` | 66 |
| `main` | Function | `universal-skills/research-lookup/research_lookup.py` | 437 |
| `write_output` | Function | `universal-skills/research-lookup/research_lookup.py` | 479 |
| `lookup` | Method | `universal-skills/research-lookup/research_lookup.py` | 407 |
| `batch_lookup` | Method | `universal-skills/research-lookup/research_lookup.py` | 421 |
| `_detect_venue_tier` | Function | `universal-skills/research-lookup/lookup.py` | 89 |
| `_select_backend` | Method | `universal-skills/research-lookup/research_lookup.py` | 78 |
| `_get_chat_client` | Method | `universal-skills/research-lookup/research_lookup.py` | 104 |
| `_parallel_lookup` | Method | `universal-skills/research-lookup/research_lookup.py` | 120 |
| `_extract_basis_citations` | Method | `universal-skills/research-lookup/research_lookup.py` | 167 |
| `_perplexity_lookup` | Method | `universal-skills/research-lookup/research_lookup.py` | 200 |
| `_format_academic_prompt` | Method | `universal-skills/research-lookup/research_lookup.py` | 298 |
| `_extract_api_citations` | Method | `universal-skills/research-lookup/research_lookup.py` | 327 |
| `_extract_citations_from_text` | Method | `universal-skills/research-lookup/research_lookup.py` | 369 |

## Execution Flows

| Flow | Type | Steps |
|------|------|-------|
| `Main → _get_chat_client` | cross_community | 5 |
| `Main → _extract_basis_citations` | cross_community | 5 |
| `Main → _extract_citations_from_text` | cross_community | 5 |
| `Main → _format_academic_prompt` | cross_community | 5 |
| `Example_batch_queries → _get_chat_client` | cross_community | 5 |
| `Example_batch_queries → _extract_basis_citations` | cross_community | 5 |
| `Example_batch_queries → _extract_citations_from_text` | cross_community | 5 |
| `Example_batch_queries → _format_academic_prompt` | cross_community | 5 |
| `Example_batch_queries → _extract_api_citations` | cross_community | 5 |
| `Main → _select_backend` | cross_community | 4 |

## How to Explore

1. `context({name: "example_automatic_selection"})` — see callers and callees
2. `query({search_query: "research-lookup"})` — find related execution flows
3. Read key files listed above for implementation details
4. `explain({target: "<file or symbol>"})` — persisted taint findings (source→sink data flows), when indexed with `--pdg`
