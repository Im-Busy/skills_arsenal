---
name: dual-repo-sync
description: Manages a dual-remote Git architecture where a private development repo syncs curated (non-sensitive) files to a public-facing repo. Handles branch curation, .gitignore management, merge safety checks, and leak prevention for progress docs, agent memory, IDE configs, and workspace files.
license: MIT
metadata:
    skill-author: project
---

# Dual-Repo Sync — Private → Public Curation

## Architecture

```
Private Repo (private)              Public Repo (public)
  master branch                       public branch
  [all files]                         [curated files only]

  git push private master             git push public public
       │                                    │
       │  git checkout public               │
       │  git merge master                  │
       │  [safety check]                    │
       │  git push public public            │
       └────────────────────────────────────┘
```

## What Stays Private (ALWAYS excluded)

| Path | Reason |
|------|--------|
| `progress_docs/` | Project plans, handover notes |
| `MEMORY.md` | Agent persistent memory |
| `.vscode/` | IDE config (personal settings) |
| `.claude/` | Claude session files |
| `CLAUDE.md` | Claude instructions |
| `gitnexus_CGC_combo.code-workspace` | Workspace file (leaks local paths) |
| `.python-version` | Local version pin |
| `.gitnexus/` | Regenerable code intelligence index |
| `.cgc/` | Regenerable graph database |
| `.kilo/worktrees/` | Kilo worktree state |
| `.kilo/node_modules/` | Build artifacts |
| `.venv/` | Local virtualenv |
| `__pycache__/`, `*.pyc` | Byte-compiled cache |
| `.pytest_cache/`, `.ruff_cache/`, `.mypy_cache/` | Tool caches |
| `*.egg-info/` | Auto-generated metadata |

## What Goes Public (curated showcase)

| Path | Purpose |
|------|---------|
| `src/` | Config generator + setup scripts |
| `tests/` | Full test suite |
| `platforms/` | Platform matrix registry |
| `docs/` | Documentation, guides |
| `commands/` | Slash command definitions |
| `skills/` | Skill definitions (canonical) |
| `.kilo/agent/` | AI agent definitions |
| `.kilo/command/` | Slash commands |
| `.kilo/skills/` | Skill definitions |
| `.kilo/global-rules.md` | Global behavioral rules |
| `.kilo/project-rules.md` | Project-specific rules |
| `.kilo/kilo.json` | Kilo MCP config |
| `.opencode/commands/` | Opencode slash commands |
| `.opencode/agents/` | Opencode agent definitions |
| `.opencode/skills/` | Opencode skill definitions |
| `README.md`, `AGENTS.md` | Project landing docs |
| `pyproject.toml`, `uv.lock` | Project deps |
| `whitelist.txt` | Public scope definition |
| `.cgcignore` | CGC ignore rules |

## Sync Workflow (CRITICAL ORDER)

### Step 1: Prepare
```bash
git checkout master && git pull private master   # Latest private changes
```

### Step 2: Merge into public branch
```bash
git checkout public
git merge master
```

### Step 3: SAFETY CHECK — verify no private files leaked
```bash
git diff --name-only public@{1}..public | Select-String -Pattern "^progress_docs|^MEMORY|^CLAUDE|^.claude|^.vscode|^.python-version|.code-workspace"
```

**If ANY output appears:** Files have leaked. Run cleanup:
```bash
git rm --cached -r progress_docs/ .claude/ .vscode/ 2>$null
git rm --cached MEMORY.md CLAUDE.md .python-version gitnexus_CGC_combo.code-workspace 2>$null
git commit -m "curate: remove leaked private files from public merge"
```

### Step 4: Push
```bash
git push public public
```

### Step 5: Return to development
```bash
git checkout master
```

## Leak Prevention Rules

1. **Never** push `master` branch to `public` remote — only push the `public` branch
2. **Always** run the safety check after `git merge master` before pushing
3. **Always** verify `git remote -v` shows `public` pointing to the public repo before pushing
4. **Never** add new tracked files to private directories on `master` without also adding `.gitignore` entries for them on `public`
5. If new directories with private data are created on `master`, update this skill file and the public `.gitignore`

## Emergency: If Private Files Get Pushed to Public

1. **Immediately** delete the offending branch from public remote: `git push public --delete <branch>`
2. OR force-push a clean commit: `git push public --force`
3. Rotate any exposed credentials
4. Review GitHub commit history for the leaked data
