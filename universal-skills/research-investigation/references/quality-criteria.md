# Insight Quality Criteria — 7-Axis Scoring

Every insight extracted in Phase 2 (DEEP-READ) is scored on 7 axes (0.0–1.0). These scores feed into the confidence calculation and later into the synergy formula. Score based on what the SOURCE provides, not what might be possible.

This scoring system serves three purposes:

1. **Confidence weighting** — higher-scoring insights carry more weight in downstream synthesis and synergy detection.
2. **Traceability** — every insight has a documented evidence basis, so decisions can be audited.
3. **Gap identification** — consistently low scores on certain axes across sources flag where the research base is weak and more investigation is needed.

## Quality Axes

| Axis | Question | 0.0 | 0.5 | 1.0 |
|------|----------|-----|-----|-----|
| **Testability** | Can it be empirically tested? | No testable prediction | Testable in principle but no method described | Specific, reproducible test described |
| **Falsifiability** | What would disprove it? | Cannot be disproven | Disprovable in theory but unclear counter-evidence | Clear conditions that would falsify it |
| **Parsimony** | Is it the simplest explanation? | Unnecessarily complex, many assumptions | Somewhat complex but justified | Simplest explanation fitting the data |
| **Explanatory Power** | How much does it explain? | Explains only the specific observation | Explains related observations | Explains a broad range of phenomena |
| **Scope** | What range does it cover? | Single data point | Narrow domain | Broad cross-domain applicability |
| **Consistency** | Does it align with established principles? | Contradicts established knowledge | Partially consistent, some tensions | Fully consistent with established knowledge |
| **Novelty** | Does it offer new insights? | Already well-known | Incremental improvement on known work | Genuinely new perspective or finding |

## Confidence Calculation

```
confidence = mean(testability, falsifiability, parsimony, explanatory_power, scope, consistency, novelty)

Adjustments (applied after mean):
- evidence_type == "benchmark" → +0.1
- evidence_type == "assertion" → -0.1
- Clamp to [0.0, 1.0]
```

The seven axis scores are averaged to produce a base confidence. Evidence-type adjustments then shift the result: a benchmark-backed claim gets a small boost, while an unsupported assertion gets a penalty. The final value is clamped to the [0.0, 1.0] range to avoid out-of-bounds scores.

### Worked Examples

**High-confidence insight:** A README describes a reproducible benchmark: "codesight reduced exploration tokens by 7x–91x across 50 repos using the included `benchmark.py` script." This scores: testability=0.9 (script provided), falsifiability=0.8 (clear metric, can run and compare), parsimony=0.6 (multiple mechanisms), explanatory_power=0.7, scope=0.6, consistency=0.8, novelty=0.5. Mean = 0.70. evidence_type="benchmark" → +0.1. Final = 0.80.

**Low-confidence insight:** A discussion comment: "I noticed truncating tool descriptions saved lots of tokens for me." This scores: testability=0.0 (no measurement), falsifiability=0.1 (vague), parsimony=0.3, explanatory_power=0.2, scope=0.1, consistency=0.5, novelty=0.3. Mean = 0.21. evidence_type="assertion" → -0.1. Final = 0.11.

### When to Adjust the evidence_type

- **benchmark**: Source provides quantitative measurements, reproducible methodology, and ideally a comparison baseline. The +0.1 reflects that benchmarked claims have survived empirical scrutiny.
- **assertion**: Source states a claim without evidence, data, or methodology. Common in discussions, informal blog posts, and feature requests. The -0.1 reflects the higher risk of overclaiming or anecdotal bias.
- **neither** (default): No adjustment. Applies to well-reasoned arguments, architecture descriptions, and other content that is neither benchmarked nor bare assertion.

## Insight Record Format

Each scored insight is stored with the following fields:

```json
{
  "source": "Tool or discussion name",
  "insight": "The extracted insight statement",
  "scores": {
    "testability": 0.0,
    "falsifiability": 0.0,
    "parsimony": 0.0,
    "explanatory_power": 0.0,
    "scope": 0.0,
    "consistency": 0.0,
    "novelty": 0.0
  },
  "evidence_type": "benchmark | assertion | neither",
  "confidence": 0.0,
  "strength_justification": "Required if any score <0.3 or >0.8",
  "phase": "2 | 3",
  "revised_scores": {}
}
```

The `revised_scores` field is populated during Phase 3 (CROSS-REFERENCE) when new evidence from related tools changes the original assessment. The Phase 2 scores are always preserved for audit trail purposes.

## Common Pitfalls

| Pitfall | Why It Happens | Correct Approach |
|---------|---------------|------------------|
| **Inflating novelty** | Tool seems innovative compared to what the agent knows | Score relative to the source's own claims, not the agent's prior knowledge |
| **Deflating testability** | Agent assumes "no one would benchmark this" | Check for included scripts, metrics, or comparison data before scoring |
| **Middle-score bias** | Avoiding extreme scores by defaulting to 0.5 | 0.5 requires genuine partial evidence on that axis; 0.0 or 1.0 are valid defaults |
| **Contamination** | Letting a strong score on one axis influence others | Score each axis independently based on what the source provides for that dimension |
| **Scope creep** | Assigning high scope because the tool "could" apply broadly | Score based on demonstrated or documented scope, not hypothetical potential |

## Axis Interaction Notes

- **Testability and Falsifiability are correlated but not identical.** A claim may be testable (you can measure something) but hard to falsify (no clear counter-evidence threshold). Example: "compression improves comprehension" — testable via user studies, but what specific result would disprove it?
- **Parsimony often trades off with Explanatory Power.** The simplest explanation may explain less. A more complex mechanism that explains more phenomena may deserve a higher explanatory power score even if parsimony is lower. Score both honestly.
- **Novelty and Consistency can conflict.** A genuinely new insight may contradict established principles. This is valid — score novelty high and consistency appropriately (lower if it genuinely contradicts, but not penalize it merely for being unconventional).
- **Scope and Explanatory Power are related but distinct.** A claim can have high scope (applies to many tools) but low explanatory power (doesn't explain why). Score each independently.

## Scoring Guidelines

- **Score what the source PROVIDES**, not what might be possible. Do not fill gaps with speculation. An axis that the source does not address gets a 0.0, regardless of how obvious the answer seems.
- **If the source doesn't address an axis** → score **0.0** (not 0.5). A silent source on a given criterion is a zero, not a middle score.
- **Justify any score <0.3 or >0.8** in the `strength_justification` field of the insight record. Extreme scores need explanation to support downstream audit and review.
- **Never default to 0.5** "just to be safe" — use evidence. 0.5 indicates genuine partial evidence, not uncertainty avoidance. When unsure, re-read the source rather than guessing.
- **A single well-documented benchmark** can score 0.8+ on testability; a chain of logical arguments without data should score **<0.4**.
- **Novelty is relative to the tool's README or documentation**, not to the entire field. If the source presents the idea as standard practice, score accordingly. A technique may be novel to the agent without being novel in the literature — score the source's framing.
- **Scope and Explanatory Power are related but distinct.** A claim can have high scope (applies to many tools) but low explanatory power (doesn't explain why). Score each independently.
- **Consistency does not mean "agrees with everything."** It means the insight does not contradict well-established principles of token economics, LLM architecture, or the tool's own design. A novel insight that challenges conventional wisdom should score high on novelty but still be evaluated for internal consistency.
- **Re-score after Phase 3 (CROSS-REFERENCE).** New information from related tools or discussions may change axis scores. Record the initial score from Phase 2 and the revised score from Phase 3 separately.

## Adapted From

These criteria are adapted from the **K-Dense-AI/scientific-agent-skills** hypothesis-generation quality scoring system (specifically its seven-axis `InsightQuality` scoring model). The original framework defines quality across seven dimensions for evaluating scientific hypotheses in research workflows.

### What Changed

| Aspect | Original (scientific-agent-skills) | This Adaptation |
|--------|-----------------------------------|-----------------|
| **Domain** | Scientific hypothesis evaluation | Token-saving tool insight evaluation |
| **Scoring anchors** | Academic research standards | README, benchmark, and discussion evidence |
| **Novelty reference** | Relative to published literature | Relative to the tool's own documentation |
| **Confidence adjustment** | Not specified | evidence_type boost/penalty added |
| **Primary artifact** | Research papers and experiments | Tool READMEs, benchmarks, discussion threads |

The axes and anchor descriptions remain structurally identical to the original, but the interpretation of each score point is tuned to the artifacts that the research-investigation skill processes. This ensures consistency: an insight scored by this system can be compared across tools, sessions, and phases, while remaining grounded in the specific evidence the source provides.