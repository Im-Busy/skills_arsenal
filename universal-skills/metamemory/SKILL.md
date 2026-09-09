---
name: metamemory
description: >
  Maps what an agent knows, does not know, and can verify, then chooses human or
  specialist-agent escalation for unresolved gaps. Hybrid invocation — activates
  on context match or when the LLM identifies relevance at any point. Use when an
  agent must separate evidence from assumptions, identify a knowledge boundary,
  or decide who should resolve it; confidence may inform that decision but is not
  the primary output. Do NOT confuse with `confidence-check`, which supplies the
  pre-delivery 0-100 scoring rubric and hedging audit. Do NOT use for trivial
  yes/no answers or factual lookups with direct evidence.
license: MIT
metadata:
  version: "0.1.0"
  skill-author: project
  invocation_posture: hybrid
---

# metamemory

## Overview

Metamemory identifies what the agent knows, what remains unverified, and when a specialist agent or human must resolve the gap. A confidence estimate can support that boundary decision, but `confidence-check` owns the scoring rubric and delivery audit.

## 1. Confidence Self-Check

Before delivering a complex or high-stakes response, run this mental checklist:

### Phase 1 — Self-Verification (always)
- **Truthfulness**: Am I stating facts or speculating? Can I cite a source?
- **Source validity**: Are my references real files/paths/URLs? Did I actually read them?
- **Hidden assumptions**: Am I assuming something the user didn't state?
- **Knowledge boundaries**: Is this within my training data, or am I guessing?
- **Self-consistency**: Do earlier parts of my response contradict later parts?

### Phase 2 — External Verification (when high stakes)
- Cross-check claims against actual file contents (read, don't assume)
- Run commands to verify assumptions (build, test, lint)
- If confidence < 85% on any claim → flag it: "I'm not fully confident about X because Y"

### Phase 3 — Uncertainty Framing (when unsure)
When confidence is low, frame your response honestly:
- "I'm not fully confident about this, but based on what I can see..."
- "Here's my best understanding — verify X before relying on it"
- "I couldn't confirm Y — would you like me to investigate further?"

## 2. Knowledge Boundaries

### What you know:
- Code you've actually read in this session
- Established patterns from official documentation
- Your training data (with appropriate confidence)

### What you DON'T know:
- Unread files — don't assume their contents
- Runtime behavior — test, don't guess
- User intent — ask, don't assume
- External system state — check, don't presume

### Boundary recognition triggers:
- You're about to say "this should work" without testing
- You're making design decisions without seeing existing patterns
- You're guessing API behavior without checking documentation
- You're assuming file contents without reading them

## 3. Escalation Triggers

### Escalate to ANOTHER AGENT when:
- The task requires domain expertise you lack → use agent-roster to find specialist
- You've failed 2+ fix attempts on a specific problem → consult oracle
- Architecture decisions affect multiple systems → delegate to architect

### Escalate to HUMAN when:
- A decision is irreversible, destructive, or safety-critical
- Multiple valid approaches exist with significant tradeoffs
- You need credentials, permissions, or access you don't have
- You've exhausted all automated options and remain blocked

### Do NOT escalate when:
- You can resolve it yourself with research or testing
- The answer is discoverable from existing code or documentation
- Another agent can handle it (delegate, don't bother the user)

## Related skills / Do NOT confuse with

- **confidence-check**: Do NOT confuse it with this skill. Use `confidence-check` for pre-output 0-100 scoring and hedging or contradiction audits; use `metamemory` to track knowledge boundaries and decide when to escalate.
- **agent-roster**: For finding the right specialist to escalate to
- **delegation-context**: For how to delegate effectively once you've decided to escalate
- **debugging**: For when metacognition reveals a bug you can't explain

## Inspiration

These patterns are derived from NOVA's metacognition plugins:
- `confidence-check`: Two-phase pipeline (self-verify → external eval → framing)
- `self-awareness`: Semantic embedding comparison against curated trigger phrases

Source: NOVA Mind upstream project, `cognition/metacognition/`
