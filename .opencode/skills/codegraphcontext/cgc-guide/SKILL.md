---
name: cgc-guide
description: "Use for CodeGraphContext operations — indexing code, running Cypher queries, searching for code patterns, analyzing relationships, finding dead code, or visualizing the code graph."
---

# CodeGraphContext Guide

CGC is a Python-native MCP server that indexes code into a graph database for AI-assisted querying.

## Quick Start

```bash
# Install
uv pip install codegraphcontext

# Index a project
cgc index /path/to/project

# Check stats
cgc stats /path/to/project

# Start watcher (auto re-index on file changes)
cgc watch /path/to/project/src
```

## Core Commands

### Indexing

```bash
cgc index <project_path>           # Full index
cgc index --force <project_path>   # Force re-index
cgc stats <project_path>           # Show file/function/class counts
```

### Searching

```bash
cgc find name "functionName"       # Find by name
cgc find pattern "regex*pattern"   # Find by regex
cgc find content "some concept"    # Fuzzy content search
cgc find function "handler"        # Find functions matching name
cgc find class "Controller"        # Find classes matching name
```

### Analysis

```bash
cgc analyze callers "functionName"        # Who calls this?
cgc analyze callees "functionName"        # What does this call?
cgc analyze imports "moduleName"          # Who imports this?
cgc analyze inheritance "ClassName"       # Class hierarchy
cgc analyze dependencies "moduleName"     # Module dependency graph
cgc analyze dead-code                     # Find unused code
cgc analyze complexity                    # Complexity hotspots
```

### Graph Queries

```bash
cgc query "MATCH (f:Function) RETURN f.name LIMIT 10"   # Raw Cypher
cgc visualize                                             # Start viz server
```

## MCP Tools (when loaded as MCP server)

| Tool | Description |
|------|-------------|
| `index_codebase` | Index a directory into the graph |
| `find_code` | Search code by name, pattern, or content |
| `analyze_code_relationships` | Callers, callees, imports, inheritance |
| `execute_cypher_query` | Run read-only Cypher queries |
| `find_dead_code` | Detect unused symbols |
| `get_code_stats` | File/function/class counts |
| `visualize_graph_query` | Generate graph visualization |
| `search_registry_bundles` | Search pre-indexed reference bundles |
| `load_bundle` | Load a pre-indexed bundle |

## Graph Schema

**Nodes:** File, Class, Function, Variable, Import
**Edges:** CALLS, IMPORTS, INHERITS, DEFINES, CONTAINS, REFERENCES

## When to Use CGC vs GitNexus

| Task | Use |
|------|-----|
| Impact analysis / blast radius | GitNexus |
| Code search / fuzzy matching | CGC |
| Dead code detection | CGC |
| Visual graph exploration | CGC |
| Execution flow tracing | GitNexus |
| Safe rename | GitNexus |
| Raw Cypher queries | Either |
| Class hierarchy analysis | CGC |

## Watcher (Auto Re-Index)

```bash
# One-time start (runs until killed)
cgc watch /path/to/project/src

# PowerShell background job (Windows):
Start-Job -Name "CGCWatcher" -ScriptBlock {
    Set-Location <cgc_install_dir>
    $env:PYTHONIOENCODING = "utf-8"
    uv run cgc watch <project_src_path>
}

# Verify: Get-Job -Name "CGCWatcher" → must show "Running"
```
