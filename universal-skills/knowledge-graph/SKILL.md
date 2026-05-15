# Skill: Knowledge Graph — Paper → Module Cross-Reference Engine

> **CRITICAL**: This skill MUST be loaded and executed whenever new papers are added to `useful_resources/papers/` or when new PDFs are converted to markdown in `useful_resources/papers_md/`.
>
> This skill cross-references all research papers against project modules, identifies gaps and opportunities, and keeps `KNOWLEDGE_GRAPH_INSIGHTS.md` up to date.

---

## When to Activate

Load this skill in ANY of the following scenarios:

1. **New papers added** — new PDFs appear in `useful_resources/papers/`
2. **Papers converted** — new `.md` files appear in `useful_resources/papers_md/`
3. **After paper summarization** — paper2md generates new summaries
4. **On explicit request** — user asks for cross-references, insights, or knowledge graph
5. **After implementing new modules** — to re-evaluate paper alignment

## Core Workflow

### Step 1: Detect New Papers

```bash
# Find PDFs without matching .md files
Get-ChildItem useful_resources/papers/*.pdf | ForEach-Object {
    $md = "useful_resources/papers_md/$($_.BaseName).md"
    if (-not (Test-Path $md)) { $_ }
}
```

### Step 2: Convert New PDFs to Markdown

Use `pdfplumber` for text extraction (primary) or `marker-pdf` for OCR on image-based PDFs:

```bash
uv run python -c "
import pdfplumber
from pathlib import Path
# ... (standard conversion: extract text, save as .md)
"
```

Save output to `useful_resources/papers_md/` with paper title as filename.

### Step 3: Run Knowledge Analysis

Execute the cross-reference script that:
- Scans all 48+ paper MDs for topics (10 categories)
- Maps to 16 project modules in `src/`
- Identifies connections, gaps, and opportunities

```bash
uv run useful_resources/_knowledge_analysis.py
```

This generates/updates `useful_resources/papers_md/KNOWLEDGE_GRAPH_INSIGHTS.md`.

### Step 4: Update Action Plans

After generating insights, add HIGH and MEDIUM priority recommendations to:
- `progress_docs/plans/full.md` (add new tasks)
- `progress_docs/current.md` (log the analysis)

### Step 5: Update This Skill's Paper Index

If new papers introduce novel topics, add them to the paper index below.

---

## Topic Categories (10 total)

The knowledge graph categorizes every paper into these topics via keyword matching:

| # | Topic | Typical Keywords |
|---|-------|-----------------|
| 1 | Overfitting & Data Leakage | overfitting, cross-validation, purged, embargo, out-of-sample |
| 2 | Reinforcement Learning | RL, DQN, PPO, policy gradient, multi-agent, OOM-RL |
| 3 | Sentiment Analysis & NLP | sentiment, NLP, Twitter, tweet, BERT, LLM, news |
| 4 | Portfolio Optimization | Markowitz, Sharpe ratio, Kelly criterion, allocation, Black-Litterman |
| 5 | Machine Learning Methods | XGBoost, LightGBM, CatBoost, LSTM, ensemble, AutoML, evolutionary |
| 6 | Backtesting & Validation | backtest, walk-forward, simulation, paper trading, defensive |
| 7 | Risk Management | VaR, CVaR, drawdown, stop-loss, circuit breaker, volatility |
| 8 | Event-Driven Trading | event-driven, calendar, earnings, macroeconomic, spikes |
| 9 | Factor Models & Alpha | alpha factor, multi-factor, pair trading, statistical arbitrage |
| 10 | Time Series Forecasting | forecasting, ARIMA, GARCH, stationarity, FinCast |

## Project Module Map

| Module | Path | Purpose | Paper Connections |
|--------|------|---------|-------------------|
| `ml` | `src/ml/` | ML pipeline, training, tuning, validation | 25 papers |
| `risk` | `src/risk/` | VaR, CVaR, circuit breakers, position sizing | 14 papers |
| `strategies` | `src/strategies/` | 33+ strategy wrappers | 10 papers |
| `backtest` | `src/backtest/` | Event-driven backtest engine | 6 papers |
| `signals` | `src/signals/` | Signal aggregation, confluence scoring | 4 papers |
| `portfolio` | `src/portfolio/` | Black-Litterman, multi-strategy engine | 3 papers |
| `patterns` | `src/patterns/` | 34+ chart pattern detectors | — |
| `analysis` | `src/analysis/` | Ablation, contribution, DSR/PSR/FDR | — |

---

## Key Cross-References (Living Index)

### Overfitting & Data Leakage → `src/ml/`

| Paper | Insight | Implementation Status |
|-------|---------|----------------------|
| Circuit-Based Intrinsic Methods to Detect Overfitting | Detect overfit by perturbing rare patterns in model circuits | ❌ Not implemented |
| Detecting Overfitting via Adversarial Examples | Use adversarial examples to expose overfit decision boundaries | ❌ Not implemented |
| USING THE TRAINING HISTORY TO DETECT... | Monitor loss curves for overfit detection | ❌ Not implemented |
| Backtest Overfitting in the ML Era | Synthetic OOS comparison framework | ❌ Not implemented |
| Keeping Deep Learning Models in Check | History-based approach: track changes in input→output sensitivity | ❌ Not implemented |

### Sentiment & NLP → `src/signals/`, `src/strategies/`

| Paper | Insight | Implementation Status |
|-------|---------|----------------------|
| Tweet Sentiment Classification (ensemble) | Ensemble classifier achieves higher accuracy | ❌ No NLP module |
| Sentiment Analysis of Twitter Texts Using ML | Benchmark of ML algorithms for Twitter sentiment | ❌ No NLP module |
| NLP-Powered Sentiment Analysis on Twitter | Direct NLP pipeline for sentiment extraction | ❌ No NLP module |
| Leveraging Hybrid Model for Twitter Sentiment | Hybrid model approach for accurate sentiment | ❌ No NLP module |

### Reinforcement Learning → `src/rl/` (NEW)

| Paper | Insight | Implementation Status |
|-------|---------|----------------------|
| OOM-RL | Market-driven alignment via capital depletion | ❌ No RL module |
| An adaptive dual-level RL for trade execution | VWAP tracking via PPO | ❌ No RL module |
| Deep Learning for Portfolio Optimization | Direct Sharpe optimization via deep RL | ❌ No RL module |

### Portfolio Optimization → `src/portfolio/`

| Paper | Insight | Implementation Status |
|-------|---------|----------------------|
| Investing Is Compression | Kelly criterion = entropy/divergence decomposition | ❌ Kelly not in portfolio module |
| JPM Why Not 100 Equities | Diversified portfolio beats concentrated (even for long-term) | ✅ Philosophy adopted |
| Emergence of Statistical Factors | Factors emerge from irrational trader activity | ❌ Not in factor model |

### Event-Driven Trading → `src/data_ingestion/`, `src/strategies/`

| Paper | Insight | Implementation Status |
|-------|---------|----------------------|
| Building a Calendar of Events Database | Detect events from price spikes | ❌ No event pipeline |
| Event-Based Trading: Building Superior Strategies | Event-driven strategy framework | ❌ No event module |
| Risk Management for Event-Driven Funds | Binomial risk model for event positions | ❌ Not in risk module |

---

## Output Deliverable

After every run, this skill produces/updates:

| File | Purpose |
|------|---------|
| `useful_resources/papers_md/KNOWLEDGE_GRAPH_INSIGHTS.md` | Comprehensive cross-reference report (topic distribution, module connections, gap analysis, recommendations) |
| `progress_docs/plans/full.md` | Updated with new action items from insights |
| `progress_docs/current.md` | Session log entry for the analysis run |

---

## Usage Instructions

**Load this skill when**:
- New PDFs appear in `useful_resources/papers/`
- Papers are converted to `.md` in `useful_resources/papers_md/`
- User asks about paper insights, cross-references, or knowledge graph
- Implementing new modules that could benefit from paper research

**This skill will**:
1. Detect new/unprocessed papers
2. Convert PDFs to markdown if needed
3. Run cross-reference analysis against all project modules
4. Update `KNOWLEDGE_GRAPH_INSIGHTS.md` with fresh findings
5. Add actionable tasks to project plans
