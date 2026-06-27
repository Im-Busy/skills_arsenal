---
name: covariates-forecasting
description: "Skill for the Covariates-forecasting area of skills_arsenal. 6 symbols across 1 files."
---

# Covariates-forecasting

6 symbols | 1 files | Cohesion: 100%

## When to Use

- Working with code in `domain-specific-skills/`
- Understanding how generate_sales_data, create_visualization, add_divider work
- Modifying covariates-forecasting-related functionality

## Key Files

| File | Symbols |
|------|---------|
| `domain-specific-skills/ml-data-science/timesfm-forecasting/examples/covariates-forecasting/demo_covariates.py` | generate_sales_data, create_visualization, add_divider, demonstrate_api, explain_xreg_modes (+1) |

## Entry Points

Start here when exploring this area:

- **`generate_sales_data`** (Function) — `domain-specific-skills/ml-data-science/timesfm-forecasting/examples/covariates-forecasting/demo_covariates.py:48`
- **`create_visualization`** (Function) — `domain-specific-skills/ml-data-science/timesfm-forecasting/examples/covariates-forecasting/demo_covariates.py:129`
- **`add_divider`** (Function) — `domain-specific-skills/ml-data-science/timesfm-forecasting/examples/covariates-forecasting/demo_covariates.py:160`
- **`demonstrate_api`** (Function) — `domain-specific-skills/ml-data-science/timesfm-forecasting/examples/covariates-forecasting/demo_covariates.py:390`
- **`explain_xreg_modes`** (Function) — `domain-specific-skills/ml-data-science/timesfm-forecasting/examples/covariates-forecasting/demo_covariates.py:416`

## Key Symbols

| Symbol | Type | File | Line |
|--------|------|------|------|
| `generate_sales_data` | Function | `domain-specific-skills/ml-data-science/timesfm-forecasting/examples/covariates-forecasting/demo_covariates.py` | 48 |
| `create_visualization` | Function | `domain-specific-skills/ml-data-science/timesfm-forecasting/examples/covariates-forecasting/demo_covariates.py` | 129 |
| `add_divider` | Function | `domain-specific-skills/ml-data-science/timesfm-forecasting/examples/covariates-forecasting/demo_covariates.py` | 160 |
| `demonstrate_api` | Function | `domain-specific-skills/ml-data-science/timesfm-forecasting/examples/covariates-forecasting/demo_covariates.py` | 390 |
| `explain_xreg_modes` | Function | `domain-specific-skills/ml-data-science/timesfm-forecasting/examples/covariates-forecasting/demo_covariates.py` | 416 |
| `main` | Function | `domain-specific-skills/ml-data-science/timesfm-forecasting/examples/covariates-forecasting/demo_covariates.py` | 435 |

## Execution Flows

| Flow | Type | Steps |
|------|------|-------|
| `Main → Add_divider` | intra_community | 3 |

## How to Explore

1. `context({name: "generate_sales_data"})` — see callers and callees
2. `query({search_query: "covariates-forecasting"})` — find related execution flows
3. Read key files listed above for implementation details
4. `explain({target: "<file or symbol>"})` — persisted taint findings (source→sink data flows), when indexed with `--pdg`
