---
name: gitnexus-debugging
description: "Use when the user wants to trace bugs, understand why something is failing, or investigate unexpected behavior in the codebase."
---

# Debugging with GitNexus

## When to Use

- "Why is X failing?"
- "This function returns wrong results"
- "The API is broken"
- Tracing bug root causes through the codebase

## Workflow

```
1. gitnexus_query({query: "<bug description>"})           → Find related execution flows
2. gitnexus_context({name: "<suspicious symbol>"})        → 360-degree view
3. READ gitnexus://repo/{name}/process/{processName}      → Trace full execution
4. Read source files at key steps in the flow
5. Identify where the bug likely originates
```

## Checklist

```
- [ ] gitnexus_query to map the affected execution flow
- [ ] gitnexus_context on entry points and key symbols
- [ ] READ the process resource to see all steps
- [ ] Read source for each step in the flow
- [ ] gitnexus_impact on candidate fix targets
- [ ] Verify fix doesn't break dependents
```

## Tips

- Start with `gitnexus_query` — returns processes ranked by relevance
- Use `gitnexus_context` on symbols at the boundary (API endpoints, event handlers)
- Trace the full process with `gitnexus://repo/{name}/process/{name}` to see data flow
- Before fixing, run `gitnexus_impact` on your target to check blast radius
