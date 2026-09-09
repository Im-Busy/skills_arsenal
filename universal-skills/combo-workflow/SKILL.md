---
name: combo-workflow
description: Coordinates only the 10-tool Token Saver Meta chain (codesight, GitNexus, CGC, RTK, Repomix, caveman, LG-token-saver, kevin-copilot, ContextSlimAI, and Token Saver Meta) through priority order, synergy chains, and conflict checks. Hybrid invocation — activates on context match or when the LLM identifies relevance at any point. Use when configuring or optimizing a multi-tool context-saving workflow. Do NOT use as a general CLI inventory (use cli-tools), for single-tool operations, general code editing, or tasks unrelated to token optimization.
license: MIT
metadata:
  version: "1.0.0"
  skill-author: project
  invocation_posture: hybrid
---

# Token Saver Combo Workflow

> Master skill for using all 10 Token Saver Meta tools as an integrated system.

## Related Skills

- **Do NOT confuse with `cli-tools`.** This skill coordinates only the Token Saver Meta chain. Use `cli-tools` for general utility inventory and command syntax.

## Quick Reference

| Tool | When to Use |
|------|-------------|
| **codesight** | Session start — project overview via CODESIGHT.md (~200 tok vs 40K+ file reads) |
| **GitNexus** | Before editing any symbol — impact analysis, execution flows |
| **CGC** | Dead code detection, Cypher queries, hierarchy analysis |
| **RTK** | Any shell command — auto-compressed output via hooks |
| **Repomix** | Full codebase context dump for agent prompts |
| **caveman** | Always active — ultra-terse agent output style |
| **LG-token-saver** | Always active — parallelism, dedup, compaction rules |
| **kevin-copilot** | Always active — terseness instructions |
| **ContextSlimAI** | Integrates through the host's supported rules mechanism |
| **Token Saver Meta** | The meta-layer that bundles, detects platform, and applies all above |

## Priority Flow

Apply tools in this order to maximize cumulative savings:

1. **codesight FIRST** — Read `CODESIGHT.md` for project overview (~200 tok). Eliminates 40K+ tokens of file-by-file exploration before any other work begins.

2. **GitNexus** — Before editing any symbol, run impact analysis. Understand what else depends on the change before writing code.

3. **CGC** — Structural queries (Cypher) and dead code detection. Use instead of grep for hierarchy and dependency questions.

4. **Repomix** — When you need full-codebase context as a single prompt input. Packs the repo down to ~30% of raw size.

5. **RTK** — Wraps every shell call automatically via PreToolUse hook. No manual action needed once configured.

6. **caveman + LG-token-saver + kevin-copilot** — Always active. These run on every response; verify they're loaded if output seems verbose.

7. **ContextSlimAI** — Enable it through the host's supported rules mechanism; verify its CLI wrapper if shell output remains large.

## Synergy Chains

Tools compound when used in sequence:

| Chain | Effect |
|-------|--------|
| codesight → GitNexus | Fast overview → precise impact. No blind edits. |
| codesight → Repomix | Skeleton map → full context. Minimizes Repomix token count. |
| RTK → LG-token-saver | Shell output compressed + parallelism rules. Double savings on every shell turn. |
| TSCG → Any MCP tool | 50-72% savings on tool schema size in every request. |

## Anti-Patterns

| Anti-Pattern | Why It Wastes Tokens | Correct Approach |
|---|---|---|
| `grep` before graph query | grep reads and returns raw file content (10-100x more tokens) | Query GitNexus or CGC first |
| `read_file()` on 200+ line files without codesight | Loads entire file without context; may not need it | Read `CODESIGHT.md` first, then read targeted sections |
| Sequential shell calls | Each call re-sends full context; compressed output wasted | Use parallel tool invocations or host-supported command batching |
| Editing without impact analysis | May break dependents; debugging costs 10x what impact analysis would | Always run GitNexus before edit |
| Ignoring index freshness warnings | Stale indices lead to wrong or incomplete results | Re-index when warned: `gitnexus analyze` or `codesight reindex` |
| Enabling automatic shell hooks | Hidden pre-tool behavior can alter or delay every command | Keep shell execution explicit and native. |
| Manual compression when tools are active | Token-saver tools already compress; manual effort adds overhead with no gain | Trust the tool chain; only intervene if output is still oversized |

## Host Activation

Install each tool from its upstream package, register this skill through the
host's supported skill mechanism, and enable required hooks or rules through
documented host configuration. Do not assume a specific config filename or key.

## Verification

Run these checks after setup:

```bash
# Set these to the host's skill root and active agent config.
test -f "$AGENT_SKILLS_DIR/combo-workflow/SKILL.md"

# Verify the active config references the tool chain.
rg "codesight|gitnexus|rtk|repomix" "$AGENT_CONFIG_FILE"
```
