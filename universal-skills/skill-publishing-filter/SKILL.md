---
name: skill-publishing-filter
description: >
  Gates whether agent knowledge belongs in an existing skill, new skill,
  AGENTS.md rule, MCP, or script, and whether the result is safe to publish.
  Hybrid invocation — activates on context match or when the LLM identifies
  relevance at any point. Use when packaging agent guidance, removing
  device-specific details, or preparing a public skill. Do NOT use as the
  SKILL.md format reference (use the host platform's skill-authoring standard)
  or for ordinary application code changes unrelated to agent skills.
license: MIT
metadata:
  version: "0.1.0"
  skill-author: project
  invocation_posture: hybrid
---

# skill-publishing-filter

## Purpose

Gate every new or edited skill through packaging choice, device-specificity
review, generalization, and publish consent.

## Packaging decision (first)

Pick the lightest form that works:

| Form | When |
|------|------|
| **Existing skill update** | Same domain already has a skill; add a section or reference |
| **New skill** | Reusable procedure with clear triggers and negative triggers |
| **AGENTS.md** | Always-on constraint that must load every turn and stays short |
| **MCP** | Needs live tools, ports, APIs, or long-running services |
| **Other** (standard, script, command only) | One-shot automation without agent narrative |

Do not create a skill when a two-line AGENTS.md rule or an existing skill section is enough.

## Device-specificity gate

**Do not publish** content that embeds private machine state:

- Absolute paths unique to one machine or username
- Personal credentials, tokens, API keys
- Local-only ports/services without portable configuration
- Private repo paths, home directories, or one-off hardware notes

If the capability is useful to others, strip device specifics and rewrite for plug-and-play:

- Prefer relative paths, env vars, and documented config keys
- Prefer tool names over machine-local install paths
- Put local-only notes in a clearly labeled **Local workspace notes** section that stays private

## Publish workflow

1. **Author** the skill against the host platform's skill-authoring standard (frontmatter, posture, description formula, `skill.json`).
2. **Audit** with the skill repository's validator; fix FAIL/WARN before publish.
3. **Generalize** wording for other machines and users.
4. **Stage** a copy in the public skill collection when the skill is public-worthy.
5. **Ask before commit** to the arsenal or any public remote. Never auto-commit or auto-push publish artifacts.
6. **Record** the decision: private-only | generalized-and-staged | not-a-skill (other form).

## Decision tree

```
Need reusable agent procedure?
  ├─ Already covered? → extend existing skill
  ├─ Always-on tiny rule? → AGENTS.md
  ├─ Live service/API? → MCP (+ optional thin skill)
  └─ New skill → write → device gate
        ├─ private-only → keep local; do not publish
        └─ public-worthy → generalize → audit → ask user → commit only after yes
```

## Related Skills

- **Do NOT confuse with the host platform's skill-authoring standard.** This skill decides packaging, device scrubbing, publish suitability, and consent. The standard defines SKILL.md format and metadata.
- `skill-audit` — structural and registration checks
