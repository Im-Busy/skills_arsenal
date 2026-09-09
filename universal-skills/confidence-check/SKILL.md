---
name: confidence-check
description: >
  Scores an agent's confidence from 0-100 before delivery and audits the draft
  for hedging, unsupported assertions, and self-contradictions. Hybrid invocation
  — activates on context match or when the LLM identifies relevance at any point.
  Use before complex responses, in high-consequence domains, or when delivering
  uncertain output. Do NOT confuse with `metamemory`, which tracks knowledge
  boundaries and chooses human or specialist-agent escalation. Do NOT use for
  trivial yes/no answers, factual lookups with direct evidence, or routine
  single-step operations.
license: MIT
metadata:
  version: "1.0.0"
  skill-author: project
  invocation_posture: hybrid
---

# Confidence Check Skill

> **Source**: Adapted from nova-mind's `cognition/metacognition/confidence-check/` plugin.
> Skill-based adaptation — self-check only, no external LLM call required.

## Purpose

This skill teaches agents metacognitive self-evaluation: before delivering output, assess your own confidence, check for common failure patterns, and flag uncertainty.

## Related skills / Do NOT confuse with

- **Do NOT confuse with `metamemory`.** Use this skill for pre-output 0-100 scoring plus hedging and contradiction audits. Use `metamemory` to track knowledge boundaries and choose human or agent escalation.

## When to Load
- Before delivering any complex response or deliverable
- When the agent is uncertain about correctness
- When working in domains with high consequences for errors
- After the orchestrator's session is loading this skill

## How to Use

### 1. Self-Assessment (before delivering)
Before presenting output, ask yourself:
1. **Am I confident?** Rate 0-100
2. **What am I uncertain about?** Name specific points
3. **Could I verify this?** Check if evidence is available

### 2. Confidence Scoring Rubric

| Score | Meaning | Action |
|-------|---------|--------|
| 90-100 | High confidence — evidence-backed, well-understood domain | Deliver normally |
| 75-89 | Moderate confidence — mostly sure, minor uncertainties | Deliver with one-sentence caveat |
| 50-74 | Low confidence — significant uncertainty | Flag: "I'm not fully confident about this. Key uncertainties: [list]" |
| <50 | Very low confidence — guessing | State: "I'm uncertain here. Here's my best guess: [answer]. Would you like me to research further?" |

### 3. Hedging Phrase Checklist
Self-audit: does your output contain these red flags?

| Hedging Phrase | Why It's a Red Flag |
|---------------|---------------------|
| "should work" | Haven't tested it |
| "probably" | Uncertainty not quantified |
| "I think" | Guess, not knowledge |
| "seems like" | No concrete evidence |
| "in most cases" | Edge cases not checked |
| "generally" | Not verified |
| "might" | Speculative |

If your output has 3+ of these, your confidence is below 75. Reassess.

### 4. Assertion Verification
For each factual claim in your output, ask:
- **Source**: Where did I get this information?
- **Freshness**: Is this still current?
- **Verifiability**: Could a reader confirm this?

If any claim lacks a traceable source, mark it as unverified.

### 5. Self-Contradiction Check
Scan your output for:
- Inconsistent numbers (two different figures for the same metric)
- Contradictory recommendations ("use X" then "avoid X")
- Mismatched assumptions (stated assumption vs actually used)

### 6. When Confidence < 85%
State explicitly: "I'm not fully confident about [specific point]. My reasoning is [brief]. To be certain, I would [verification step]. Would you like me to verify this?"

## Counter-Indications
Do NOT use this skill for:
- Trivial factual lookups (file contents, git log, docker ps)
- Tool outputs where the result IS the verification
- Simple yes/no questions with clear evidence

## Philosophy
nova-mind's confidence-check plugin uses a two-phase pipeline (self-verify → external evaluate → frame) with LLM scoring. The skill-based version achieves the same metacognitive benefit through structured self-audit: the agent checks its own output for hedging, unsupported assertions, and contradictions before delivering.

## References
- NOVA Mind upstream source, `cognition/README.md` — confidence-check plugin specification
- NOVA Mind upstream source, `cognition/metacognition/confidence-check/` — original implementation
