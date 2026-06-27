---
name: gitnexus-exploring
description: "Use when the user asks how code works, wants to understand architecture, trace execution flows, or explore unfamiliar parts of the codebase."
---

# Exploring Codebases with GitNexus

## When to Use

- "How does authentication work?"
- "What's the project structure?"
- "Show me the main components"
- Understanding code you haven't seen before

## Workflow

```
1. READ gitnexus://repos                          → Discover indexed repos
2. READ gitnexus://repo/{name}/context             → Codebase overview, check staleness
3. gitnexus_query({query: "<what you want to understand>"})  → Find related execution flows
4. gitnexus_context({name: "<symbol>"})            → Deep dive on specific symbol
5. READ gitnexus://repo/{name}/process/{name}      → Trace full execution flow
```

> If step 2 says "Index is stale" → run `npx gitnexus analyze` in terminal.

## Checklist

```
- [ ] READ gitnexus://repo/{name}/context
- [ ] gitnexus_query for the concept you want to understand
- [ ] Review returned processes (execution flows)
- [ ] gitnexus_context on key symbols for callers/callees
- [ ] READ process resource for full execution traces
- [ ] Read source files for implementation details
```

## Resources

| Resource                                | What you get                                            |
| --------------------------------------- | ------------------------------------------------------- |
| `gitnexus://repo/{name}/context`        | Stats, staleness warning                                |
| `gitnexus://repo/{name}/clusters`       | All functional areas with cohesion scores               |
| `gitnexus://repo/{name}/cluster/{name}` | Area members with file paths                            |
| `gitnexus://repo/{name}/process/{name}` | Step-by-step execution trace                            |

## Tools

**gitnexus_query** — find execution flows related to a concept:
```
gitnexus_query({query: "payment processing"})
→ Processes grouped by flow with file locations
```

**gitnexus_context** — 360-degree view of a symbol:
```
gitnexus_context({name: "validateUser"})
→ Incoming/outgoing calls, participating processes
```
