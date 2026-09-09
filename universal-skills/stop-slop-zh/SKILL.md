---
name: stop-slop-zh
description: >
  Rewrites Chinese prose to reduce formulaic AI phrasing while preserving
  meaning, evidence, terminology, and the requested register. Manual-first
  invocation - use only when the user explicitly names or invokes
  stop-slop-zh. Do NOT use for ordinary Chinese output or general rewrite,
  polish, or de-slopping requests; route those requests to deslop-zh.
version: "0.2.0"
license: MIT
metadata:
  skill-author: community
  invocation_posture: manual-first
  source: https://github.com/pencil20388-eng/stop-slop-zh
---

# Stop Slop ZH

Rewrite Chinese prose so it reads naturally for its audience without changing
the underlying facts or manufacturing a human voice.

## Activation Boundary

- Run only when the user explicitly names or invokes `stop-slop-zh`.
- Route general Chinese rewrite, polish, and de-slopping requests to
  `deslop-zh`.
- Do not apply this skill to ordinary Chinese conversation, technical answers,
  translations, quotations, legal text, code, commands, or structured data
  unless the user explicitly includes that material in the rewrite scope.
- Treat the requested dialect, register, publication format, and house style as
  higher priority than this skill's stylistic suggestions.

## Non-Negotiable Safeguards

- Preserve facts, numbers, names, citations, uncertainty, and causal claims.
- Never invent data, people, quotations, anecdotes, scenarios, sources, or user
  experiences to make the prose feel concrete.
- Never add colloquialisms, emotion, cultural references, or personal voice
  unless the source or requested register supports them.
- Use normal Chinese punctuation, headings, lists, and numbering whenever they
  improve accuracy or scanability. No punctuation mark or document structure is
  categorically banned.
- Do not turn an unsupported claim into a confident statement. Preserve or make
  explicit the source text's uncertainty.

## Workflow

1. Identify the audience, Chinese variety, register, and requested degree of
   rewriting. Preserve the source register when the user gives no alternative.
2. Mark factual claims, technical terms, quotations, numbers, and citations as
   meaning-preservation anchors.
3. Remove only genuine formulaic patterns: redundant transitions, repeated
   conclusions, vague intensifiers, empty scene-setting, and uniform sentence
   rhythm.
4. Rewrite for clarity and natural flow. Prefer concrete verbs and precise nouns
   already supported by the source.
5. Compare the result with the anchors. Restore any lost qualification, detail,
   or technical meaning before returning it.

## Contextual Guidance

| Pattern | Default treatment |
|---|---|
| Repeated throat-clearing | Delete when it adds no meaning |
| Generic transition phrase | Replace only when the paragraph relationship is clear |
| Long bullet list | Keep it when readers need scanning or comparison |
| Numbered procedure | Keep it when order matters |
| Colloquial phrase | Use only when it fits the source voice and audience |
| Concrete example | Preserve sourced examples; do not manufacture one |
| Colon, dash, or quotation marks | Keep when grammatically or technically useful |

## Output

Return the rewritten text directly unless the user asks for annotations, a
change summary, or alternatives. Do not append a self-assessment report by
default.
