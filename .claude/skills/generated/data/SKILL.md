---
name: data
description: "Skill for the Data area of skills_arsenal. 11 symbols across 1 files."
---

# Data

11 symbols | 1 files | Cohesion: 80%

## When to Use

- Working with code in `universal-skills/`
- Understanding how lum, is_dark, on_color work
- Modifying data-related functionality

## Key Files

| File | Symbols |
|------|---------|
| `universal-skills/ui-ux-pro-max/data/data/_sync_all.py` | lum, is_dark, on_color, derive_row, rebuild_colors (+6) |

## Entry Points

Start here when exploring this area:

- **`lum`** (Function) — `universal-skills/ui-ux-pro-max/data/data/_sync_all.py:21`
- **`is_dark`** (Function) — `universal-skills/ui-ux-pro-max/data/data/_sync_all.py:26`
- **`on_color`** (Function) — `universal-skills/ui-ux-pro-max/data/data/_sync_all.py:29`
- **`derive_row`** (Function) — `universal-skills/ui-ux-pro-max/data/data/_sync_all.py:41`
- **`rebuild_colors`** (Function) — `universal-skills/ui-ux-pro-max/data/data/_sync_all.py:187`

## Key Symbols

| Symbol | Type | File | Line |
|--------|------|------|------|
| `lum` | Function | `universal-skills/ui-ux-pro-max/data/data/_sync_all.py` | 21 |
| `is_dark` | Function | `universal-skills/ui-ux-pro-max/data/data/_sync_all.py` | 26 |
| `on_color` | Function | `universal-skills/ui-ux-pro-max/data/data/_sync_all.py` | 29 |
| `derive_row` | Function | `universal-skills/ui-ux-pro-max/data/data/_sync_all.py` | 41 |
| `rebuild_colors` | Function | `universal-skills/ui-ux-pro-max/data/data/_sync_all.py` | 187 |
| `h2r` | Function | `universal-skills/ui-ux-pro-max/data/data/_sync_all.py` | 14 |
| `r2h` | Function | `universal-skills/ui-ux-pro-max/data/data/_sync_all.py` | 18 |
| `blend` | Function | `universal-skills/ui-ux-pro-max/data/data/_sync_all.py` | 32 |
| `shift` | Function | `universal-skills/ui-ux-pro-max/data/data/_sync_all.py` | 37 |
| `derive_ui_reasoning` | Function | `universal-skills/ui-ux-pro-max/data/data/_sync_all.py` | 249 |
| `rebuild_ui_reasoning` | Function | `universal-skills/ui-ux-pro-max/data/data/_sync_all.py` | 358 |

## Execution Flows

| Flow | Type | Steps |
|------|------|-------|
| `Rebuild_colors → H2r` | cross_community | 5 |
| `Rebuild_colors → R2h` | cross_community | 4 |

## How to Explore

1. `context({name: "lum"})` — see callers and callees
2. `query({search_query: "data"})` — find related execution flows
3. Read key files listed above for implementation details
4. `explain({target: "<file or symbol>"})` — persisted taint findings (source→sink data flows), when indexed with `--pdg`
