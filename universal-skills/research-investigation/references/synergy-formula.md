# Synergy Detection Formula

Phase 3 (CROSS-CONNECT) scores every insight pair to identify the strongest connections. Top 30% of pairs advance to Council review, where 5 parallel subagents evaluate each candidate synergy.

**This formula is HARDCODED** — it is not configurable per project. All projects using the research-investigation skill apply the same scoring weights and thresholds.

## Formula

```
synergy_score = relevance_overlap × 0.30
              + mechanism_complementarity × 0.35
              + evidence_agreement × 0.20
              + practical_compound_effect × 0.15
```

Each component is scored on a **0.0 to 1.0** scale. The weighted sum produces a final synergy_score in the same range.

## Component Definitions

### relevance_overlap (0.0–1.0, weight 0.30)

Measures how closely two insights address the same topic or question.

| Score | Meaning | Example |
|-------|---------|---------|
| 1.0 | Same specific question or topic | Both insights about shell output compression via hooks |
| 0.7 | Overlapping domains | One on PreToolUse, one on PostToolUse for shell output |
| 0.4 | Adjacent domains | One on shell compression, one on schema trimming |
| 0.1 | Different domains | One on prompt compression, one on output style |
| 0.0 | No relevance overlap | Unrelated areas — no basis for synergy |

### mechanism_complementarity (0.0–1.0, weight 0.35)

Assesses whether the mechanisms behind each insight can compound or conflict. This is the **highest weighted** component because true synergies arise from different mechanisms working together.

| Score | Meaning | Example |
|-------|---------|---------|
| 1.0 | Different mechanisms that compound | Pre-execution rewrite + post-execution filter on same pipeline |
| 0.7 | Different but independent mechanisms | Cache-based read reduction + output compression |
| 0.4 | Similar mechanisms at different depths | Static context map + dynamic impact analysis |
| 0.1 | Nearly identical mechanisms | Two approaches doing the same thing at the same layer |
| 0.0 | Identical mechanism → potential conflict | Same hook point, same token type, same strategy |

### evidence_agreement (0.0–1.0, weight 0.20)

Evaluates whether the supporting evidence for each insight is consistent, contradictory, or inconclusive.

| Score | Meaning | Example |
|-------|---------|---------|
| 1.0 | Both benchmark-backed, consistent findings | Both report 60–80% savings on same metric |
| 0.7 | Both strong evidence, no contradictions | One benchmarked, one validated in production |
| 0.4 | One strong, one moderate | One has benchmarks, the other has only README claims |
| 0.1 | Conflicting or weak evidence | Different benchmarks showing opposite results, or both unverified |
| 0.0 | Directly contradictory | Same metric, same conditions — one says 70% savings, one says 10% |

### practical_compound_effect (0.0–1.0, weight 0.15)

Estimates whether using both insights together produces a greater effect than either alone. This is the **lowest weighted** component because it is the hardest to assess without actually combining the tools — Council review handles this evaluation in depth.

| Score | Meaning | Example |
|-------|---------|---------|
| 1.0 | A makes B MORE effective (true synergy) | Context map reduces file reads → shell compressor has less noise to compress |
| 0.7 | A + B together better than either alone | Independent tools addressing different token types |
| 0.4 | Can coexist but don't enhance | Tools operate on unrelated parts of the pipeline |
| 0.1 | Slight interference | Overlapping scope causes redundant work |
| 0.0 | Cannot coexist (genuine conflict) | Both hook into the same lifecycle event with incompatible logic |

## Weight Rationale

The weights are assigned by descending significance to synergy detection:

| Component | Weight | Rationale |
|-----------|:------:|-----------|
| mechanism_complementarity | **0.35** | True synergies arise from different mechanisms compounding. Same-mechanism pairs are rarely synergistic and often conflict. This is the most information-rich signal. |
| relevance_overlap | **0.30** | Unrelated insights are not synergistic regardless of how complementary their mechanisms appear. Domain alignment is a necessary (but not sufficient) condition. |
| evidence_agreement | **0.20** | Agreeing evidence builds confidence that the synergy is real, not hypothetical. But evidence alone does not create synergy — it validates it. |
| practical_compound_effect | **0.15** | The most difficult to score correctly without running experiments. This is intentionally weighted lowest so that borderline pairs are not excluded prematurely. Council review (Phase 4) evaluates this in depth with hands-on testing. |

## Conflict Detection

Pairs that score poorly on both mechanism and evidence are flagged for explicit conflict evaluation.

**Trigger condition:**

```
mechanism_complementarity < 0.2 AND evidence_agreement < 0.2
```

When triggered:
- The pair is flagged as **CONFLICT**
- Documented with connection type `"contradicts"` in the connection entry
- The pair is NOT excluded — it still advances if in the top 30% — but Council must explicitly evaluate the conflict
- The `contradicts` relationship is valuable: resolving conflicts often reveals the maximum-coexistence architecture

## Usage in Phase 3

The formula is applied as follows during the CROSS-CONNECT phase:

1. **Score all pairs**: Every unique pair of insights from the insight registry is scored using the formula above.

2. **Rank by synergy_score**: Pairs are sorted descending by their weighted score.

3. **Select top 30%**: The highest-scoring pairs advance to Council review (Phase 4).

4. **Floor rule**: If `total_pairs < 5`, ALL pairs advance regardless of score. This prevents premature filtering when the insight set is small.

5. **Output format**: Each scored pair is written to the connection JSONL file with a `formula_score` field containing the computed value. Example entry:

```json
{
  "conn_type": "synergy",
  "from_insight": "insight-003",
  "to_insight": "insight-007",
  "formula_score": 0.82,
  "components": {
    "relevance_overlap": 0.7,
    "mechanism_complementarity": 1.0,
    "evidence_agreement": 0.7,
    "practical_compound_effect": 0.7
  },
  "conflict_flag": false
}
```

All components are recorded alongside the final score so Council agents can trace how the score was derived. Conflict-flagged entries include `"conflict_flag": true` and `"conn_type": "contradicts"`.