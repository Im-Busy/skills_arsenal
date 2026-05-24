---
name: cli-anything
description: Auto-generate agent-friendly CLI harnesses for any software via 7-phase pipeline (Analyze→Design→Implement→Test→Document→Publish). 40+ community CLIs available (Blender, GIMP, Zotero, Obsidian, ComfyUI, Draw.io, Ollama, n8n). CLI-Hub meta-skill for agent-autonomous CLI discovery. Use when making any software agent-accessible via structured CLIs.
version: 1.0.0
author: CLI-Anything (Apache 2.0)
source: C:\Dev\useful_repos\CLI-Anything
tags: [CLI, Python, Agent Tooling, Automation, Code Generation, Click]
dependencies: [python>=3.10, click>=8.0, pytest]
---

# CLI-Anything

Auto-generates agent-friendly CLI wrappers around any software, making it accessible to AI coding agents via structured Click-based CLIs with JSON output.

## When to Use

- You have scripts or tools that need consistent, agent-friendly command-line interfaces
- You want AI agents to interact with your software through structured CLI commands
- You need JSON output from tools for programmatic consumption
- You're building an ecosystem of agent-accessible tools

## 7-Phase Pipeline

```
Analyze → Design → Implement → Plan Tests → Write Tests → Document → Publish
```

Each phase is automated. Output: pip-installable Python package with:
- Click-based CLI with `--json` flag for structured output
- SKILL.md for agent discoverability
- pytest test suite
- CLI-Hub registration for auto-discovery

## CLI-Hub Discovery

The CLI-Hub meta-skill lets agents self-discover available CLIs:

```
Agent asks: "What CLIs are available?"
CLI-Hub responds with catalog of 40+ generated CLIs
Agent selects and invokes: cli-anything-blender, cli-anything-gimp, etc.
```

## 40+ Community CLIs

| Category | CLIs |
|----------|------|
| **Creative** | Blender, GIMP, Inkscape, Krita, Draw.io |
| **Knowledge** | Zotero, Obsidian, Logseq, Joplin |
| **AI/ML** | Ollama, ComfyUI, n8n, Stable Diffusion |
| **Productivity** | Thunderbird, Evolution, LibreOffice |
| **Development** | VS Code, Sublime, Vim |

## Integration Pattern

```bash
# Install a generated CLI
pip install cli-anything-blender

# Agent-friendly usage
blender render --scene scene.blend --output out.png --json
```

## SKILL.md + Command Pattern

Every generated CLI ships with:
- **SKILL.md** — When to use, workflow steps, examples
- **Commands** — `/blender-render`, `/blender-export`, etc.
- **JSON output schema** — Structured, parseable results
