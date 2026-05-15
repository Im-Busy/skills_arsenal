# Skill: Trading Papers Knowledge Base

> Distilled insights from academic papers in `useful_resources/papers/` mapped to actionable implementations for this project.

---

## Paper Index & Relevance

| Paper | Key Topic | Relevance | Target Module |
|-------|-----------|-----------|---------------|
| **1.AMultimodalEvent-drivenLSTM** | Multimodal ML for stock prediction | High | `src/ml/`, `src/signals/` |
| **Crash-based quantitative trading (1-s2.0-S1544612321002579)** | Behavioral crash factors, timing strategies | High | `src/strategies/`, `src/risk/` |
| **Risk Management for Event-Driven Funds (ssrn-1018281)** | Event risk, binomial distributions | High | `src/risk/`, `src/backtest/` |
| **Algorithmic Trading book (9780429183942)** | Comprehensive trading strategies | Reference | Multiple modules |
| **Building a Calendar of Events Database** | Event detection from price spikes | Medium | `src/analysis/`, `src/backtest/engine.py` |
| **Investing Is Compression** | Kelly criterion, universal portfolios | High | `src/risk/position_sizing.py` |
| **OOM-RL** | Reinforcement learning alignment via live markets | Low | `src/ml/` (future RL work) |
| **Against a Universal Trading Strategy** | No free lunch, adversarial limits | High | Strategy design philosophy |
| **Emergence of Statistical Financial Factors** | Factor emergence from irrational traders | Medium | `src/ml/regime_model.py` |
| **JPM Why Not 100 Equities** | Portfolio construction | Low | Position sizing context |

---

## High-Priority Insights

### 1. Crash-Based Quantitative Trading Strategies (Fang et al.)

**Core Insight**: Stock market crashes follow a predictable behavioral pattern: prolonged rise → bubble peak → sudden collapse. Crash factors can be quantified and used for timing strategies.

**Key Concepts**:
- **Crash + Timing Strategy (CTS)**: Identify crash-prone stocks using behavioral indicators, exit before crash
- **Crash + Momentum-Reversal Strategy (CMRS)**: Buy after crash when reversal is likely
- Behavioral indicators: herding bias, overconfidence bias, CEO overconfidence

**Implementation Actions**:
```python
# src/risk/crash_detector.py (NEW)
# Detect crash-prone conditions using:
# 1. Herding metrics (volume concentration)
# 2. Overconfidence metrics (analyst dispersion)
# 3. Price bubble indicators (deviation from fundamentals)

# src/strategies/crash_timing.py (NEW)
# CTS: Exit signal when crash indicators exceed threshold
# CMRS: Entry signal after crash when RSI/extreme deviation shows reversal
```

**Risk Implications**:
- Crash risk is systematic during bubbles, idiosyncratic during normal periods
- Stop-loss critical for momentum strategies (momentum crashes documented)
- Han, Zhou, Zhu (2016): Simple stop-loss tames momentum crashes

---

### 2. Event-Driven Risk Management (Jorion)

**Core Insight**: Event-driven strategies have **discontinuous, skewed, binary distributions**. Conventional VaR fails because price history is irrelevant—event outcome determines payoff.

**Key Concepts**:
- Events are binary: merger succeeds/fails, bankruptcy happens/not
- Deal break correlations are **low but positive** (~0.1-0.3 for M&A)
- Most event risk is **idiosyncratic and diversifiable**
- Binomial distribution model for independent events

**Implementation Actions**:
```python
# src/risk/event_risk.py (NEW)
def calculate_event_var(positions: List[EventPosition]) -> float:
    """
    Event VaR using binomial model.
    Each position has: probability_p, payoff_success, payoff_failure
    Portfolio distribution = sum of binomials (correlation-adjusted)
    """
    pass

# src/backtest/metrics.py (UPDATE)
# Add event-specific metrics:
# - Event success rate
# - Deal break correlation tracking
# - Skewness of returns
```

**Project Relevance**:
- Pattern detection signals are event-like (pattern confirmed/not confirmed)
- Signal generation has binary outcomes → similar risk profile
- Position sizing should account for binary outcome distributions

---

### 3. Investing Is Compression (Stiffelman)

**Core Insight**: Kelly criterion decomposes investing into: **Money term × Entropy term × Divergence term**. Universal portfolios can perform optimally without knowing the future.

**Key Concepts**:
- Kelly maximizes **expected log wealth** (not expected wealth)
- Cover's universal portfolio: weight by type class entropy
- Position sizing proportional to entropy (uncertainty)
- Growth shortfall bounded by entropy of winner distribution

**Implementation Actions**:
```python
# src/risk/position_sizing.py (UPDATE)
def kelly_fraction(win_prob: float, win_loss_ratio: float) -> float:
    """
    Kelly criterion: f = (p*b - q) / b
    where b = win/loss ratio, p = win probability
    """
    return (win_prob * win_loss_ratio - (1 - win_prob)) / win_loss_ratio

def entropy_weighted_sizing(signals: List[Signal]) -> Dict[str, float]:
    """
    Size positions proportional to signal entropy (uncertainty).
    Higher entropy = more uncertain = smaller position.
    """
    pass
```

**Key Formula**:
```
Kelly fraction: f = (p*b - q) / b
Half-Kelly recommended for practical use (reduces volatility)
Entropy-weighted: weight_i ∝ exp(-H(sequence_i))
```

---

### 4. Against a Universal Trading Strategy (Adversarial Limits)

**Core Insight**: **No strategy can be universal against reactive environments**. Markets are adversarial—algorithms probe and trade against predictable logic of other algorithms.

**Key Concepts**:
- Cantor diagonalization: for any strategy set, there exists a market that ruins it
- Rice's Theorem: determining failure trajectories is undecidable
- HFT algorithms actively exploit predictable patterns
- No free lunch in adversarial markets

**Implementation Implications**:
1. **Never assume static alpha**: patterns that work today may be exploited tomorrow
2. **Add randomness**: avoid deterministic triggers that can be front-run
3. **Regime adaptation**: strategy must change behavior based on market state
4. **Monitor decay**: track pattern performance over time, detect adversarial exploitation

```python
# src/analysis/pattern_performance_tracker.py (UPDATE)
# Add adversarial decay detection:
def detect_alpha_decay(pattern_returns: pd.Series, window: int = 90) -> float:
    """
    Compare recent performance vs historical.
    Significant decay suggests adversarial exploitation.
    """
    recent = pattern_returns.tail(window).mean()
    historical = pattern_returns.head(len(pattern_returns) - window).mean()
    return recent / historical  # < 1.0 indicates decay

# src/strategies/adaptive_router.py (UPDATE)
# Add random jitter to avoid being front-run:
def jittered_entry(price: float, signal_strength: float) -> float:
    """
    Add small random offset to entry price.
    Prevents exact prediction by adversaries.
    """
    jitter = np.random.normal(0, 0.001 * price)
    return price + jitter * signal_strength
```

---

### 5. Multimodal Event-Driven LSTM (Li et al.)

**Core Insight**: Stock prediction is a **multimodal problem**—fundamentals (continuous, regular) + news (discrete, irregular). Concatenation ignores interactions.

**Key Concepts**:
- News events are **irregularly sampled** vs regular fundamental data
- Cross-modal interactions: news amplifies or dampens fundamental signals
- Event-driven architecture handles irregular data

**Implementation Actions**:
```python
# src/ml/features.py (UPDATE)
def merge_multimodal_data(
    price_data: pd.DataFrame,  # Regular time series
    event_data: pd.DataFrame   # Irregular events (news, announcements)
) -> pd.DataFrame:
    """
    Merge irregular events into regular price data.
    Events create 'shock' features that decay over time.
    """
    pass

# src/ml/regime_model.py (UPDATE)
# Add event awareness to regime detection:
# - Pre-event regime (anticipation)
# - Event shock regime
# - Post-event regime (absorption)
```

---

### 6. Algorithmic Trading Book Reference (Kissell)

**Comprehensive Topics** (relevant chapters):

| Chapter | Topic | Project Application |
|---------|-------|---------------------|
| Ch 5 | Statistical Trading Strategies | All strategies in `src/strategies/` |
| Ch 5.3 | Filter Rules | `src/strategies/donchian_breakout.py` |
| Ch 5.3.2 | Moving Average Variants | `src/strategies/sma_crossover.py`, `ema_ribbon.py` |
| Ch 5.4 | Pattern Discovery via Non-Parametric Smoothing | `src/patterns/` |
| Ch 6 | Dynamic Portfolio Management | `src/signals/position_manager.py` |
| Ch 7 | News Analytics & Sentiment | `src/ml/signal_scorer.py` |
| Ch 9 | Market Impact Models | `src/backtest/engine.py` (transaction costs) |

**Key Equations**:
```
Market Impact: MI = k * (Q/V)^γ * σ^δ
where Q = order size, V = avg volume, σ = volatility
k, γ, δ calibrated empirically
```

---

## Medium-Priority Insights

### 7. Building a Calendar of Events Database

**Core Insight**: Price spikes reveal events. Analyze abnormal returns to build event calendar retrospectively.

**Application**:
- `src/analysis/` could detect events from price spikes
- Link spikes to news/announcements for causality
- Use for backtest event-aware simulation

---

### 8. Emergence of Statistical Financial Factors

**Core Insight**: Factors emerge from **irrational trader activity**, not just rational pricing.

**Application**:
- Regime model could track "noise trader intensity"
- Behavioral factors (herding, overconfidence) as regime inputs

---

## Low-Priority / Future Work

### 9. OOM-RL (Out-of-Money Reinforcement Learning)

**Concept**: Align RL agents by letting them lose real money—capital depletion is unhackable feedback.

**Future Application**:
- If project adds RL components, live-paper trading as alignment
- Prevent sycophancy/overfitting through real market friction

### 10. JPM Why Not 100 Equities

Portfolio construction context—not directly actionable for current signal-based system.

---

## Implementation Priority Matrix

| Priority | Paper | Immediate Action | Module |
|----------|-------|------------------|--------|
| **P0** | Crash-based trading | Add crash detection | `src/risk/crash_detector.py` |
| **P0** | Event-driven risk | Event VaR model | `src/risk/event_risk.py` |
| **P0** | Kelly criterion | Entropy-weighted sizing | `src/risk/position_sizing.py` |
| **P1** | Adversarial limits | Alpha decay detection | `src/analysis/pattern_performance_tracker.py` |
| **P1** | Adversarial limits | Entry jitter | `src/strategies/*.py` |
| **P2** | Multimodal LSTM | News integration | `src/ml/features.py` |
| **P2** | Algorithmic Trading book | Transaction cost model | `src/backtest/engine.py` |

---

## Key Formulas Reference

```python
# Kelly Criterion
kelly_fraction = (p * b - q) / b  # p=win_prob, b=win/loss_ratio, q=1-p

# Half-Kelly (practical)
practical_fraction = kelly_fraction / 2

# Event VaR (binomial)
var_event = sum(position_size * max_loss * event_fail_prob for each event)

# Market Impact
impact = k * (order_size / avg_volume) ** gamma * volatility ** delta

# Alpha Decay Ratio
decay_ratio = recent_performance / historical_performance  # <1.0 = decay

# Entropy-weighted sizing
weight_i = exp(-entropy_i) / sum(exp(-entropy_j) for all j)
```

---

## Behavioral Finance Checklist

When implementing strategies, consider these behavioral factors:

1. **Herding**: Volume concentration → crash risk
2. **Overconfidence**: Analyst dispersion → mispricing
3. **Disposition effect**: Hold losers too long, sell winners too early
4. **Momentum crashes**: Stop-loss critical during regime shifts
5. **Event anticipation**: Pre-event pricing different from post-event
6. **Adversarial adaptation**: Patterns decay when exploited

---

## References to Add to Project

Key papers to cite in strategy documentation:

1. Fang et al. (2021) - Crash-based quantitative trading strategies
2. Jorion - Risk Management for Event-Driven Funds
3. Kelly (1956) - A new interpretation of information rate
4. Cover - Universal portfolios
5. Han, Zhou, Zhu (2016) - Taming momentum crashes with stop-loss

---

## Usage Instructions

**Load this skill when**:
- Implementing new strategies in `src/strategies/`
- Working on risk management in `src/risk/`
- Designing backtest metrics in `src/backtest/`
- Adding ML features in `src/ml/`
- Reviewing pattern performance in `src/analysis/`

**What this skill provides**:
- Academic justification for implementation choices
- Key formulas and equations
- Behavioral finance considerations
- Risk management frameworks for event-like payoffs
- Adversarial awareness (alpha decay, front-running)
