---
name: gitnexus-refactoring
description: "Use when the user wants to rename, extract, split, or refactor code — especially when they consider find-and-replace which is dangerous."
---

# Refactoring with GitNexus

## When to Use

- Renaming a function, class, or variable
- Extracting code into a new module
- Splitting a large file
- Any structural change that affects multiple files

## Golden Rule

**NEVER use find-and-replace for renames.** GitNexus `rename` understands the call graph and renames all references with confidence-tagged edits.

## Workflow

```
1. gitnexus_impact({target: "oldName", direction: "upstream"})   → Blast radius
2. READ gitnexus://repo/{name}/processes                         → Affected flows
3. gitnexus_rename({target: "oldName", newName: "newName"})      → Coordinate rename
4. Review confidence-tagged edits
5. gitnexus_detect_changes()                                     → Verify scope
```

## Checklist

```
- [ ] gitnexus_impact to assess blast radius (ALWAYS first)
- [ ] READ processes to see affected execution flows
- [ ] gitnexus_rename with dry_run if uncertain
- [ ] Review all confidence-tagged edits
- [ ] gitnexus_detect_changes to verify scope
- [ ] Run tests on affected flows
```

## gitnexus_rename

```
gitnexus_rename({
  target: "oldFunctionName",
  newName: "newFunctionName",
  dry_run: false
})

→ Renamed: 8 occurrences in 4 files
→ Confidence: 100% — call graph verified all are the same symbol
→ Warning: 1 occurrence in doc/README.md (80% — human review recommended)
```

## Safety Tips

- Always `dry_run: true` first for high-risk renames
- Review low-confidence (<90%) edits manually
- Run tests after rename, especially for affected processes
- Never rename by find-and-replace — it misses call graph relationships
