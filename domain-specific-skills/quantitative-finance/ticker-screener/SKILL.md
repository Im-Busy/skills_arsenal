# Ticker Screener — Autonomous Ticker Screening Skill

## Overview

Autonomous pipeline that screens candidate tickers for basket training inclusion. Runs fundamental checks + downloads data + walk-forward IC test + correlation check. Logs everything to `docs/ticker-test-log.md`.

## When to Use

- User provides a list of candidate tickers
- User asks "find me good tickers for the basket"
- After model retraining (re-test all tickers)
- Periodic basket review

## Prerequisites

- Latest trained model at `models/pattern_classifier_v3_SPY_*.pkl` (find newest)
- Existing basket tickers for correlation check
- Internet access for Yahoo Finance

## Screening Criteria

### Tier 1: Fundamental Screen (relaxed)

| Criterion | Threshold | Check |
|-----------|-----------|-------|
| Market cap | > $200M | `yf.Ticker(t).info['marketCap']` |
| Daily notional volume | > $5M | `avgVolume * price > 5e6` |
| Institutional ownership | > 25% | `yf.Ticker(t).info['heldPercentInstitutions']` |
| Data history | > 5 years | `len(yf.download(t, start='2010-01-01')) / 252` |
| Annualized volatility | 12-55% | `df.Close.pct_change().std() * sqrt(252)` |
| Exchange | NYSE/NASDAQ only | `info['exchange']` in ['NYQ', 'NMS', 'NCM', 'NGM'] |

### Tier 2: Walk-Forward IC Test

```python
from src.ml.walk_forward import walk_forward_per_ticker
from src.ml.pattern_classifier import PatternClassifier

m = PatternClassifier()
m.load(latest_model_path)
results = walk_forward_per_ticker(m, candidates, initial_train_days=3*252, step_days=6*21, horizon=5)
# PASS if mean_rank_ic > 0.03
```

### Tier 3: Correlation Check

```python
# Extract predictions for candidate + existing winners
# Compute correlation matrix
# PASS if r < 0.70 vs SPY/QQQ/XLK cluster, r < 0.50 preferred
```

## Workflow

```
1. RECEIVE ticker list (or generate via sector scans)
2. FUNDAMENTAL SCREEN → reject failures, log with reason
3. DOWNLOAD DATA → data/raw/{TICKER}_daily.csv
4. WALK-FORWARD IC → run with latest model
5. CORRELATION CHECK → compare against 5-winner cluster
6. LOG RESULTS → append to docs/ticker-test-log.md
7. REPORT → pass/fail table with IC values
```

## Output Format (append to ticker-test-log.md)

```markdown
| YYYY-MM-DD | TICKER | Name | Sector | MC | Vol $M/d | Inst% | History | AnnVol% | IC | Verdict | Notes |
```

## Script Template

```python
"""Autonomous ticker screener — run with: uv run scripts/screen_tickers.py TICKER1 TICKER2 ..."""
import sys
import pandas as pd
import yfinance as yf
from pathlib import Path
from datetime import date

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.ml.pattern_classifier import PatternClassifier
from src.ml.walk_forward import walk_forward_per_ticker

# Config
MIN_MC = 200e6
MIN_VOL_NOTIONAL = 5e6
MIN_INST = 0.25
MIN_YEARS = 5
VOL_RANGE = (0.12, 0.55)
IC_THRESHOLD = 0.03
MODEL_GLOB = "models/pattern_classifier_v3_SPY_*.pkl"
LOG_PATH = "docs/ticker-test-log.md"

def find_latest_model():
    models = sorted(Path().glob(MODEL_GLOB))
    return str(models[-1]) if models else None

def fundamental_screen(ticker):
    info = yf.Ticker(ticker).info
    mc = info.get('marketCap', 0)
    vol = info.get('averageVolume', 0)
    price = info.get('currentPrice') or 50
    inst = info.get('heldPercentInstitutions', 0) or 0
    sector = info.get('sector', 'N/A')

    df = yf.download(ticker, start='2010-01-01', progress=False)
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    years = len(df) / 252
    ann_vol = df['Close'].pct_change().std() * (252**0.5)
    notional_m = vol * price / 1e6

    failures = []
    if mc < MIN_MC: failures.append(f"MC ${mc/1e6:.0f}M < ${MIN_MC/1e6:.0f}M")
    if notional_m < MIN_VOL_NOTIONAL: failures.append(f"Vol ${notional_m:.0f}M/d < ${MIN_VOL_NOTIONAL/1e6:.0f}M/d")
    if inst < MIN_INST: failures.append(f"Inst {inst:.0%} < {MIN_INST:.0%}")
    if years < MIN_YEARS: failures.append(f"Hist {years:.1f}y < {MIN_YEARS}y")
    if ann_vol < VOL_RANGE[0]: failures.append(f"Vol {ann_vol:.1%} < {VOL_RANGE[0]:.0%}")
    if ann_vol > VOL_RANGE[1]: failures.append(f"Vol {ann_vol:.1%} > {VOL_RANGE[1]:.0%}")

    return {
        'ticker': ticker, 'name': info.get('shortName', ticker),
        'sector': sector, 'mc': mc, 'notional_m': notional_m,
        'inst': inst, 'years': years, 'ann_vol': ann_vol,
        'passed': len(failures) == 0, 'failures': failures,
        'df': df,
    }

if __name__ == '__main__':
    tickers = sys.argv[1:] if len(sys.argv) > 1 else []
    if not tickers:
        print("Usage: uv run scripts/screen_tickers.py TICKER1 TICKER2 ...")
        sys.exit(1)

    model_path = find_latest_model()
    if not model_path:
        print("No model found. Train one first.")
        sys.exit(1)

    # Tier 1: fundamental screen
    passed, failed = [], []
    for t in tickers:
        result = fundamental_screen(t)
        if result['passed']:
            passed.append(result)
        else:
            failed.append(result)

    print(f"\nFundamental screen: {len(passed)}/{len(tickers)} passed\n")
    for r in failed:
        print(f"  {r['ticker']:>6} FAIL: {'; '.join(r['failures'])}")

    if not passed:
        sys.exit(0)

    # Tier 2: download + IC test
    for r in passed:
        path = Path(f"data/raw/{r['ticker']}_daily.csv")
        if not path.exists():
            r['df'].to_csv(path)

    m = PatternClassifier()
    m.load(model_path)
    wf_results = walk_forward_per_ticker(
        m, [r['ticker'] for r in passed],
        initial_train_days=3*252, step_days=6*21, horizon=5
    )

    # Print results
    print(f"\n{'Ticker':>6} | {'Name':<25} | {'Sector':<20} | {'IC':>8} | {'Verdict'}")
    print("-" * 85)
    log_lines = []
    for r in passed:
        t = r['ticker']
        wf = wf_results[t]
        ic = wf.mean_rank_ic
        verdict = 'PASS' if ic > IC_THRESHOLD else 'FAIL'
        print(f"{t:>6} | {r['name']:<25} | {r['sector']:<20} | {ic:+8.4f} | {verdict}")
        log_lines.append(f"| {date.today()} | {t} | {r['name']} | {r['sector']} | ${r['mc']/1e9:.1f}B | ${r['notional_m']:.0f}M | {r['inst']:.0%} | {r['years']:.0f}yr | {r['ann_vol']:.1%} | {ic:+.3f} | {verdict} | |")

    # Append to log
    print(f"\nLog appended to {LOG_PATH}")
```
