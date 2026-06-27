# Project Guidelines — skills_arsenal_for_publishing

## Purpose

A curated collection of AI agent skills (SKILL.md files) — self-contained instruction modules that teach AI coding assistants how to use specific tools, frameworks, and methodologies. Published as a skill repository for agent ecosystems.

## Tech Stack

Markdown (primary) + Python (embedded scripts). No runtime dependencies — this is a documentation/knowledge project.

## Session Start Protocol

Every new AI session MUST start by reading these files in order:

1. **`.opencode/standards/workspace-conventions.md`** — Global coding, bash, git, and tooling standards (if OpenCode)
2. **`MEMORY.md`** — Persistent handover state: current objective, completed tasks, discovered issues, next session priorities
3. **`CATALOG.md`** — Full skill catalog with descriptions — the authoritative inventory
4. **`SUMMARY.md`** — Quick reference

## Skill Anatomy Standard

Every SKILL.md in this repo follows this structure:
1. **YAML frontmatter**: `name`, `description` (trigger conditions), optional `license`, `metadata`
2. **Core instructions**: When to activate, workflow steps, decision trees
3. **Code examples**: Copy-paste ready patterns
4. **References** (`references/`): Deep-dive docs, API references, tutorials
5. **Scripts/templates** (optional): Executable utilities, templates, CSV data

## Catalog Maintenance

When adding a new skill:
1. Place SKILL.md in the correct category directory (`universal-skills/` or `domain-specific-skills/<discipline>/`)
2. Ensure YAML frontmatter has `name`, `description`, and `metadata.skill-author`
3. Add entry to `CATALOG.md` with one-line description
4. Update `SUMMARY.md` if needed
5. Run `git add` and commit with `feat: add skill <name>`

When removing a skill:
1. Remove from both `CATALOG.md` and `SUMMARY.md`

## Skill Categories

| Category | Location |
|----------|----------|
| Universal | `universal-skills/` |
| Domain-Specific | `domain-specific-skills/` |
| — Autonomous Research | `domain-specific-skills/autonomous-research/` |
| — Developer Tooling | `domain-specific-skills/developer-tooling/` |
| — Geospatial | `domain-specific-skills/geospatial/` |
| — LLM Engineering | `domain-specific-skills/llm-engineering/` |
| — ML & Data Science | `domain-specific-skills/ml-data-science/` |
| — Quantitative Finance | `domain-specific-skills/quantitative-finance/` |
| — Scientific Computing | `domain-specific-skills/scientific-computing/` |

> **CATALOG.md is the authoritative inventory.** Do not hardcode counts here — they will go stale. Agents should read CATALOG.md for the current skill list.

## File Creation Guidelines

- New skills go in the appropriate category directory
- Skill directories use lowercase-hyphens format: `skill-name/SKILL.md`
- References go in `references/` (one level deep)
- Scripts go in `scripts/` within the skill directory
- Update CATALOG.md and SUMMARY.md when adding/removing skills

## Anti-Rationalization Guardrails

| Rationalization | Reality |
|----------------|---------|
| "This skill doesn't need a description" | Without a description, the agent can't discover it |
| "I'll add the catalog entry later" | Catalog drift is the #1 maintenance burden |
| "One more tweak will fix it" | Adding without validation adds noise. Verify, then add |

<!-- gitnexus:start -->
# GitNexus — Code Intelligence

This project is indexed by GitNexus as **skills_arsenal** (14428 symbols, 15178 relationships, 84 execution flows). Use the GitNexus MCP tools to understand code, assess impact, and navigate safely.

> Index stale? Run `node .gitnexus/run.cjs analyze` from the project root — it auto-selects an available runner. No `.gitnexus/run.cjs` yet? `npx gitnexus analyze` (npm 11 crash → `npm i -g gitnexus`; #1939).

## Always Do

- **MUST run impact analysis before editing any symbol.** Before modifying a function, class, or method, run `impact({target: "symbolName", direction: "upstream"})` and report the blast radius (direct callers, affected processes, risk level) to the user.
- **MUST run `detect_changes()` before committing** to verify your changes only affect expected symbols and execution flows. For regression review, compare against the default branch: `detect_changes({scope: "compare", base_ref: "main"})`.
- **MUST warn the user** if impact analysis returns HIGH or CRITICAL risk before proceeding with edits.
- When exploring unfamiliar code, use `query({search_query: "concept"})` to find execution flows instead of grepping. It returns process-grouped results ranked by relevance.
- When you need full context on a specific symbol — callers, callees, which execution flows it participates in — use `context({name: "symbolName"})`.
- For security review, `explain({target: "fileOrSymbol"})` lists taint findings (source→sink flows; needs `analyze --pdg`).

## Never Do

- NEVER edit a function, class, or method without first running `impact` on it.
- NEVER ignore HIGH or CRITICAL risk warnings from impact analysis.
- NEVER rename symbols with find-and-replace — use `rename` which understands the call graph.
- NEVER commit changes without running `detect_changes()` to check affected scope.

## Resources

| Resource | Use for |
|----------|---------|
| `gitnexus://repo/skills_arsenal/context` | Codebase overview, check index freshness |
| `gitnexus://repo/skills_arsenal/clusters` | All functional areas |
| `gitnexus://repo/skills_arsenal/processes` | All execution flows |
| `gitnexus://repo/skills_arsenal/process/{name}` | Step-by-step execution trace |

## CLI

| Task | Read this skill file |
|------|---------------------|
| Understand architecture / "How does X work?" | `.claude/skills/gitnexus/gitnexus-exploring/SKILL.md` |
| Blast radius / "What breaks if I change X?" | `.claude/skills/gitnexus/gitnexus-impact-analysis/SKILL.md` |
| Trace bugs / "Why is X failing?" | `.claude/skills/gitnexus/gitnexus-debugging/SKILL.md` |
| Rename / extract / split / refactor | `.claude/skills/gitnexus/gitnexus-refactoring/SKILL.md` |
| Tools, resources, schema reference | `.claude/skills/gitnexus/gitnexus-guide/SKILL.md` |
| Index, status, clean, wiki CLI commands | `.claude/skills/gitnexus/gitnexus-cli/SKILL.md` |
| Work in the Scripts area (130 symbols) | `.claude/skills/generated/scripts/SKILL.md` |
| Work in the Research-lookup area (18 symbols) | `.claude/skills/generated/research-lookup/SKILL.md` |
| Work in the Data area (11 symbols) | `.claude/skills/generated/data/SKILL.md` |
| Work in the Covariates-forecasting area (6 symbols) | `.claude/skills/generated/covariates-forecasting/SKILL.md` |
| Work in the Anomaly-detection area (5 symbols) | `.claude/skills/generated/anomaly-detection/SKILL.md` |

<!-- gitnexus:end -->

<!-- gitnexus-leanctx:start -->
## Code Intelligence + Context Persistence

### Rule: Store code intelligence findings via lean-ctx
After running gitnexus impact analysis, CGC code search, or any structural code exploration, you MUST store findings in lean-ctx's knowledge graph:

- Architecture facts: `ctx_knowledge remember key="<symbol/topic>" category="architecture" value="<finding>"`
- Pattern discoveries: `ctx_knowledge pattern pattern_type="<type>" value="<pattern>"`
- Risk analysis: `ctx_knowledge remember key="risk-<symbol>" category="testing" value="<risk_level>"`
- Cross-references: `ctx_knowledge relate "<source>" "<target>" "<relationship>"`

### Rule: Recall before analyzing
Before running gitnexus impact or CGC analysis on a symbol, first check lean-ctx for prior findings:
```
ctx_knowledge recall query="<symbol>"
```
If prior analysis exists AND the code hasn't changed (verified via gitnexus detect_changes), use the cached information. If code has changed, re-run analysis and update lean-ctx.

### Rule: Session continuity
At the start of every session, run `ctx_session load` to restore prior context including code intelligence findings. At the end of significant work, run `ctx_session save` with key findings summarized.
<!-- gitnexus-leanctx:end -->
