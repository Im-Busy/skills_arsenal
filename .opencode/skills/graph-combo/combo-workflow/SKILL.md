---
name: combo-workflow
description: "Unified workflow for using GitNexus AND CodeGraphContext together. Load when doing complex code tasks that need both impact analysis and code search."
---

# GitNexus + CGC Unified Workflow

This skill teaches the **defense-in-depth** pattern: use BOTH tools for every significant code operation. Each tool has strengths the other lacks.

## The Pattern: Dual-Before-Edit

Before editing ANY symbol, run these two checks:

```
1. gitnexus_impact({target: "symbolName", direction: "upstream"})
   → WHAT breaks? How widely is this used?

2. cgc analyze_code_relationships (callers type on symbolName)
   → WHO calls this? What's the full call tree?
```

If both agree → confident edit. If they disagree → investigate discrepancy.

## Task-Specific Dual Workflows

### Exploring Unfamiliar Code

```
1. gitnexus_query({query: "concept"})      → Execution flows + process grouping
2. cgc find content "concept"              → Fuzzy search across all files
3. gitnexus_context({name: "keySymbol"})   → 360-degree symbol view
4. cgc analyze callers "keySymbol"         → Full call tree
5. Read actual source files                → Implementation details
```

### Pre-Commit Safety Check

```
1. gitnexus_detect_changes()               → What did I change + affected flows
2. cgc analyze dependencies "changedModule" → Who depends on changed modules?
3. gitnexus_impact on each changed symbol   → Blast radius per symbol
4. Report combined risk assessment
```

### Finding Dead Code to Remove

```
1. cgc analyze dead-code                    → CGC's dead code detector
2. gitnexus_impact on each candidate        → Confirm no hidden callers
3. Remove only if BOTH agree it's unused
```

### Debugging a Bug

```
1. gitnexus_query({query: "bug description"})  → Find related execution flows
2. cgc find content "error message"            → Find where error originates
3. gitnexus_context on suspicious symbols      → Call chain analysis
4. cgc analyze callers on the buggy function   → Full upstream trace
```

### Refactoring / Renaming

```
1. gitnexus_impact({target: "oldName"})    → Blast radius
2. cgc analyze callers "oldName"            → Call tree (verify impact depth)
3. gitnexus_rename({target: "oldName", newName: "newName"})
4. gitnexus_detect_changes()               → Verify scope
5. cgc find name "oldName"                  → Sanity check: any stragglers?
```

## When to Use Only One Tool

| Use ONLY GitNexus when... | Use ONLY CGC when... |
|---------------------------|---------------------|
| Renaming symbols | Finding code by content/pattern |
| Pre-commit change detection | Dead code analysis |
| Execution flow tracing | Visual graph exploration |
| Impact/blast radius assessment | Class hierarchy analysis |
| Process-level understanding | Searching pre-indexed bundles |

## Risk Assessment Table

| GitNexus Impact | CGC Callers | Combined Risk |
|----------------|-------------|---------------|
| <5 deps, d=1 only | <5 callers | LOW |
| 5-15 deps, d=1-2 | 5-15 callers | MEDIUM |
| >15 deps, d=3 | >15 callers | HIGH |
| Critical path processes | Core module | CRITICAL |

## Session Start Checklist

At the start of every session:
```
- [ ] npx gitnexus status              → Index fresh?
- [ ] cgc stats <project>              → Index fresh?
- [ ] Verify CGC watcher running       → Auto-update active?
- [ ] Reindex either if stale
```
