---
name: scripts
description: "Skill for the Scripts area of skills_arsenal. 130 symbols across 18 files."
---

# Scripts

130 symbols | 18 files | Cohesion: 92%

## When to Use

- Working with code in `universal-skills/`
- Understanding how main, main, main work
- Modifying scripts-related functionality

## Key Files

| File | Symbols |
|------|---------|
| `universal-skills/ui-ux-pro-max/data/scripts/design_system.py` | _multi_domain_search, _find_reasoning_rule, _apply_reasoning, _select_best_match, _extract_results (+15) |
| `universal-skills/research-lookup/scripts/research_lookup.py` | _get_chat_client, _parallel_lookup, _extract_basis_citations, _perplexity_lookup, _format_academic_prompt (+7) |
| `domain-specific-skills/ml-data-science/timesfm-forecasting/scripts/check_system.py` | check_gpu, check_disk, check_python, check_package, run_checks (+7) |
| `universal-skills/hypothesis-generation/scripts/generate_schematic_ai.py` | _log, _make_request, _extract_image_from_response, _image_to_base64, generate_image (+6) |
| `universal-skills/research-lookup/scripts/generate_schematic_ai.py` | _log, _make_request, _extract_image_from_response, _image_to_base64, generate_image (+6) |
| `universal-skills/scientific-critical-thinking/scripts/generate_schematic_ai.py` | _log, _make_request, _extract_image_from_response, _image_to_base64, generate_image (+6) |
| `universal-skills/jupyter-autonomous-execution/scripts/toggle_autonomous.py` | get_config_path, load_config, save_config, enable, disable (+3) |
| `universal-skills/ui-ux-pro-max/data/scripts/core.py` | detect_domain, search, tokenize, fit, score (+3) |
| `domain-specific-skills/ml-data-science/timesfm-forecasting/scripts/forecast_csv.py` | load_model, load_csv, forecast_series, write_csv_output, write_json_output (+2) |
| `domain-specific-skills/ml-data-science/scikit-learn/scripts/clustering_analysis.py` | preprocess_for_clustering, find_optimal_k_kmeans, compare_clustering_algorithms, visualize_clusters, complete_clustering_analysis |

## Entry Points

Start here when exploring this area:

- **`main`** (Function) — `universal-skills/hypothesis-generation/scripts/generate_schematic_ai.py:725`
- **`main`** (Function) — `universal-skills/research-lookup/scripts/generate_schematic_ai.py:725`
- **`main`** (Function) — `universal-skills/scientific-critical-thinking/scripts/generate_schematic_ai.py:725`
- **`get_config_path`** (Function) — `universal-skills/jupyter-autonomous-execution/scripts/toggle_autonomous.py:16`
- **`load_config`** (Function) — `universal-skills/jupyter-autonomous-execution/scripts/toggle_autonomous.py:23`

## Key Symbols

| Symbol | Type | File | Line |
|--------|------|------|------|
| `main` | Function | `universal-skills/hypothesis-generation/scripts/generate_schematic_ai.py` | 725 |
| `main` | Function | `universal-skills/research-lookup/scripts/generate_schematic_ai.py` | 725 |
| `main` | Function | `universal-skills/scientific-critical-thinking/scripts/generate_schematic_ai.py` | 725 |
| `get_config_path` | Function | `universal-skills/jupyter-autonomous-execution/scripts/toggle_autonomous.py` | 16 |
| `load_config` | Function | `universal-skills/jupyter-autonomous-execution/scripts/toggle_autonomous.py` | 23 |
| `save_config` | Function | `universal-skills/jupyter-autonomous-execution/scripts/toggle_autonomous.py` | 60 |
| `enable` | Function | `universal-skills/jupyter-autonomous-execution/scripts/toggle_autonomous.py` | 67 |
| `disable` | Function | `universal-skills/jupyter-autonomous-execution/scripts/toggle_autonomous.py` | 76 |
| `print_status` | Function | `universal-skills/jupyter-autonomous-execution/scripts/toggle_autonomous.py` | 85 |
| `is_enabled` | Function | `universal-skills/jupyter-autonomous-execution/scripts/toggle_autonomous.py` | 108 |
| `main` | Function | `universal-skills/jupyter-autonomous-execution/scripts/toggle_autonomous.py` | 114 |
| `detect_domain` | Function | `universal-skills/ui-ux-pro-max/data/scripts/core.py` | 197 |
| `search` | Function | `universal-skills/ui-ux-pro-max/data/scripts/core.py` | 220 |
| `hex_to_ansi` | Function | `universal-skills/ui-ux-pro-max/data/scripts/design_system.py` | 252 |
| `ansi_ljust` | Function | `universal-skills/ui-ux-pro-max/data/scripts/design_system.py` | 266 |
| `section_header` | Function | `universal-skills/ui-ux-pro-max/data/scripts/design_system.py` | 274 |
| `format_ascii_box` | Function | `universal-skills/ui-ux-pro-max/data/scripts/design_system.py` | 281 |
| `wrap_text` | Function | `universal-skills/ui-ux-pro-max/data/scripts/design_system.py` | 291 |
| `format_markdown` | Function | `universal-skills/ui-ux-pro-max/data/scripts/design_system.py` | 421 |
| `generate_design_system` | Function | `universal-skills/ui-ux-pro-max/data/scripts/design_system.py` | 531 |

## Execution Flows

| Flow | Type | Steps |
|------|------|-------|
| `Persist_design_system → Tokenize` | cross_community | 7 |
| `Generate → Tokenize` | cross_community | 6 |
| `Generate_design_system → _load_csv` | cross_community | 6 |
| `Generate_design_system → Detect_domain` | cross_community | 6 |
| `Persist_design_system → _load_csv` | cross_community | 6 |
| `Main → _get_total_ram_gb` | cross_community | 5 |
| `Main → _get_available_ram_gb` | cross_community | 5 |
| `Main → Get_config_path` | intra_community | 5 |
| `Main → _get_chat_client` | cross_community | 5 |
| `Main → _extract_basis_citations` | cross_community | 5 |

## How to Explore

1. `context({name: "main"})` — see callers and callees
2. `query({search_query: "scripts"})` — find related execution flows
3. Read key files listed above for implementation details
4. `explain({target: "<file or symbol>"})` — persisted taint findings (source→sink data flows), when indexed with `--pdg`
