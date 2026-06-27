---
name: anomaly-detection
description: "Skill for the Anomaly-detection area of skills_arsenal. 5 symbols across 1 files."
---

# Anomaly-detection

5 symbols | 1 files | Cohesion: 100%

## When to Use

- Working with code in `domain-specific-skills/`
- Understanding how detect_context_anomalies, build_synthetic_future, detect_forecast_anomalies work
- Modifying anomaly-detection-related functionality

## Key Files

| File | Symbols |
|------|---------|
| `domain-specific-skills/ml-data-science/timesfm-forecasting/examples/anomaly-detection/detect_anomalies.py` | detect_context_anomalies, build_synthetic_future, detect_forecast_anomalies, plot_results, main |

## Entry Points

Start here when exploring this area:

- **`detect_context_anomalies`** (Function) — `domain-specific-skills/ml-data-science/timesfm-forecasting/examples/anomaly-detection/detect_anomalies.py:47`
- **`build_synthetic_future`** (Function) — `domain-specific-skills/ml-data-science/timesfm-forecasting/examples/anomaly-detection/detect_anomalies.py:95`
- **`detect_forecast_anomalies`** (Function) — `domain-specific-skills/ml-data-science/timesfm-forecasting/examples/anomaly-detection/detect_anomalies.py:118`
- **`plot_results`** (Function) — `domain-specific-skills/ml-data-science/timesfm-forecasting/examples/anomaly-detection/detect_anomalies.py:169`
- **`main`** (Function) — `domain-specific-skills/ml-data-science/timesfm-forecasting/examples/anomaly-detection/detect_anomalies.py:382`

## Key Symbols

| Symbol | Type | File | Line |
|--------|------|------|------|
| `detect_context_anomalies` | Function | `domain-specific-skills/ml-data-science/timesfm-forecasting/examples/anomaly-detection/detect_anomalies.py` | 47 |
| `build_synthetic_future` | Function | `domain-specific-skills/ml-data-science/timesfm-forecasting/examples/anomaly-detection/detect_anomalies.py` | 95 |
| `detect_forecast_anomalies` | Function | `domain-specific-skills/ml-data-science/timesfm-forecasting/examples/anomaly-detection/detect_anomalies.py` | 118 |
| `plot_results` | Function | `domain-specific-skills/ml-data-science/timesfm-forecasting/examples/anomaly-detection/detect_anomalies.py` | 169 |
| `main` | Function | `domain-specific-skills/ml-data-science/timesfm-forecasting/examples/anomaly-detection/detect_anomalies.py` | 382 |

## How to Explore

1. `context({name: "detect_context_anomalies"})` — see callers and callees
2. `query({search_query: "anomaly-detection"})` — find related execution flows
3. Read key files listed above for implementation details
4. `explain({target: "<file or symbol>"})` — persisted taint findings (source→sink data flows), when indexed with `--pdg`
