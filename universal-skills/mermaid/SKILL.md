---
name: mermaid
description: >
  Runs the CLI-Anything Mermaid harness to manage projects and render existing
  Mermaid source to SVG or PNG through mermaid.ink, or generate share URLs.
  Hybrid invocation — activates on context match or when the LLM identifies
  relevance at any point. Use when a task needs CLI rendering, export, project
  state, undo, or redo. Do NOT use to author or validate Mermaid syntax (use
  mermaid-authoring), for Draw.io diagrams, pixel-based images, or GUI-driven tools.
license: MIT
metadata:
  version: "0.1.0"
  skill-author: project
  invocation_posture: hybrid
---

# Mermaid CLI

> Create and render Mermaid diagrams via `cli-anything-mermaid`.
> Set `MERMAID_HARNESS` to the `mermaid/agent-harness/` directory in a CLI-Anything checkout.

## Related Skills

- **Do NOT confuse with `mermaid-authoring`.** Use `mermaid-authoring` to write or validate Mermaid source. Use this skill to operate the CLI harness and produce rendered files or share URLs. Load both when a task needs authoring and rendering.

## Installation

```bash
cd "$MERMAID_HARNESS"
python -m pip install -e .
```

**Prerequisites:** Python 3.10+. No external software needed (cloud rendering via mermaid.ink).

## Quick Start

```bash
cli-anything-mermaid --json project new --sample flowchart -o flow.json
cli-anything-mermaid --json --project flow.json diagram set --text "graph TD; A-->B; B-->C;"
cli-anything-mermaid --json --project flow.json export render output.svg --format svg
```

## Supported Diagram Types

- **flowchart** — `graph TD; ...`
- **sequence** — `sequenceDiagram ...`
- **class** — `classDiagram ...`
- **state** — `stateDiagram-v2 ...`
- **er** — `erDiagram ...`
- **gantt** — `gantt ...`
- **pie** — `pie ...`
- **gitgraph** — `gitGraph ...`

## Command Groups

### Project
| Command | Description |
|---------|-------------|
| `new` | Create project with optional `--sample` preset and `--theme` |
| `open` | Open existing project file |
| `save` | Save to file |
| `info` | Show project info |
| `samples` | List sample diagram presets |

### Diagram
| Command | Description |
|---------|-------------|
| `set` | Set mermaid source (`--text` inline or `--file` path) |
| `show` | Print current mermaid source |

### Export
| Command | Description |
|---------|-------------|
| `render` | Render to SVG/PNG via mermaid.ink (`--format svg|png`) |
| `share` | Generate Mermaid Live Editor URL (`--mode edit|view`) |

### Session
| Command | Description |
|---------|-------------|
| `status` | Session state |
| `undo` | Undo last diagram change |
| `redo` | Redo undone change |

## Examples

### Flowchart
```bash
cli-anything-mermaid project new --sample flowchart -o flow.json
cli-anything-mermaid --project flow.json diagram set --text "graph TD; Start-->Process; Process-->End;"
cli-anything-mermaid --project flow.json export render flow.svg --format svg
```

### Sequence Diagram
```bash
cli-anything-mermaid project new --sample sequence -o seq.json
cli-anything-mermaid --project seq.json diagram set --text "sequenceDiagram; Alice->>Bob: Hello; Bob-->>Alice: Hi;"
cli-anything-mermaid --project seq.json export render seq.svg --format svg
```

### Share URL
```bash
cli-anything-mermaid --project flow.json export share --mode edit
# Returns: https://mermaid.live/edit#...
cli-anything-mermaid --project flow.json export share --mode view
# Returns: https://mermaid.live/view#...
```

## Agent Rules

1. **Always use `--json` flag** for parseable output
2. **Check return codes** — 0 = success, non-zero = error
3. **Parse stderr** for errors
4. **Use absolute paths** for file operations
5. **Verify output files exist** after render
6. **Mermaid syntax is strict** — test with simple diagrams first
7. **mermaid.ink has size limits** — large diagrams may fail; split into sub-diagrams
