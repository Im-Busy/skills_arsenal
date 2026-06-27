---
name: dual-repo-setup
description: Guides the agent to provision a dual-remote Git architecture for any project — private development repo (main/master) + curated public-facing mirror (public branch). Detects project structure, identifies private vs public files, creates whitelist, repo-syncer infrastructure, and gitignore exclusions. Use when user wants to publish a curated subset of a private repo without leaking secrets, IDE configs, internal docs, or agent memory.
license: MIT
metadata:
    skill-author: project
---

# Dual-Repo Setup — Provision a Private→Public Architecture

Set up a dual-remote Git architecture so a private development repo can publish a curated subset to a public mirror while keeping sensitive files private.

## Architecture Pattern

```
Private Repo (git remote: private)    Public Repo (git remote: public)
  main/master branch                    public branch
  [all files, full history]             [curated subset only]

  git push private main                 git push public public
       │                                      │
       │  git checkout public                 │
       │  git merge main                      │
       │  [safety check + strip leaks]        │
       │  git push public public              │
       └──────────────────────────────────────┘
```

## When to Use This Pattern

You have a private repo with files you want to share publicly, but some files must stay private:

| Stay Private | Go Public |
|---|---|
| Internal planning docs, handover notes | Source code (`src/`, `lib/`) |
| Agent memory files | Tests (`tests/`, `spec/`) |
| IDE configs (`.vscode/`, `.idea/`, `.claude/`, `.cursor/`) | Public documentation (`docs/`, `README.md`) |
| Workspace files (`.code-workspace`) | AI tool infrastructure (agents, commands, skills) |
| Data files (`data/`, `*.csv`, `*.parquet`) | Project configs (`pyproject.toml`, `package.json`, lock files) |
| ML models (`models/`, `*.pkl`, `*.pt`) | Platform/registry configs |
| Generated outputs, experiment results | License, contributing guide |

## Reference Examples

Two common patterns:

### Example A: Tool/Bootstrap Kit

| Private only | Public |
|---|---|
| Progress docs, handover notes | Source code, tests |
| Agent memory | AI tool agents, commands, skills |
| IDE configs, workspace files | Docs, README |
| Local version pins | Project configs, lock files |
| Regenerable indexes | Whitelist, gitignore rules |

### Example B: Research/Data System

| Private only | Public |
|---|---|
| Proprietary data files | All source code |
| Serialized models | Test suite |
| Generated outputs, experiments | CLI scripts, pipelines |
| Analysis reports, notebooks | Docs, landing page |
| Third-party papers, reference repos | Project configs |

## Step-by-Step Setup

### Step 1: Detect current project state

```bash
git remote -v
git branch -a
git ls-tree -r --name-only HEAD
```

Identify the current branch name (main or master), existing remotes, and file structure.

### Step 2: Classify files into public vs private

Walk the root directory and classify EVERY file/directory:

| Category | Public if... | Private if... |
|----------|-------------|---------------|
| Source code | `src/`, `lib/`, source files | Build artifacts |
| Tests | `tests/`, `test/`, `spec/` | Benchmarks with proprietary data |
| Docs | `docs/`, `README.md`, `CONTRIBUTING.md` | Internal planning, handover notes |
| Configs | `pyproject.toml`, `package.json`, lock files, `.gitignore` | `.env`, credentials, local overrides |
| IDE | — | `.vscode/`, `.idea/`, `.claude/`, `.cursor/`, `.roo/` |
| AI tooling | Agent/command/skill definitions | Worktree state, build artifacts, MCP configs with local paths |
| Data | — | `data/`, `*.csv`, `*.parquet`, `*.db`, `*.sqlite` |
| Models | — | `models/`, `*.pkl`, `*.pt`, `*.onnx`, `outputs/` |
| Generated | — | `dist/`, `build/`, `*.egg-info/`, `__pycache__/` |
| Memory/plans | — | `progress_docs/`, `plans/`, agent memory files, `*.code-workspace` |

### Step 3: Create whitelist.txt

Create a `whitelist.txt` at the project root listing public paths:

```
# Whitelist for public repo sync
# Lines starting with # are ignored. Directories must end with /.

# === Source Code ===
src/

# === Tests ===
tests/

# === Documentation ===
docs/
README.md

# === Project Config ===
pyproject.toml
package.json
.gitignore

# ... (add your project's entries)
```

### Step 4: Update .gitignore with public exclusions

Append to `.gitignore` only files that should never be tracked on any branch:

```
# ===== PUBLIC REPO EXCLUSIONS (both branches) =====
# IDE configs — platform-specific, never tracked
/.vscode/
/.idea/
/.claude/
/.cursor/
/.roo/

# Indexes — regenerable
/.some-index-dir/
```

**Important:** Do NOT add files tracked on the private branch (like internal docs, agent memory) to `.gitignore` — the sync agent strips them during merge. `.gitignore` only excludes files that should never be tracked on ANY branch.

### Step 5: Configure git remotes

```bash
# If remotes don't exist yet, add them:
git remote add private <https://github.com/you/private-repo.git>
git remote add public <https://github.com/you/public-repo.git>
```

### Step 6: Create public branch

```bash
git checkout -b public
```

The public branch starts identical to your private branch. The first curation commit will strip private files.

### Step 7: Make the initial curation commit

Remove private files from tracking on the public branch:

```bash
git checkout public
git rm --cached -r private-dir1/ private-dir2/ 2>$null
git rm --cached internal-file.md agent-memory.md 2>$null
git commit -m "curate: remove private files for public mirror"
```

### Step 8: Create the sync infrastructure

Create three files for ongoing sync management:

1. **An AI agent definition** — Safety-checking agent with merge workflow and private file stripping. Defines the sync steps: verify remotes → pull → merge → safety check → strip leaks → push → return.
2. **A slash command** — Invokes the sync agent with sub-commands: `check` (verify safety), `status` (show state), and full sync.
3. **A sync skill document** — Full workflow docs with leak prevention rules, emergency procedures, and the list of what stays private vs goes public.

Customize the private files list in each based on your Step 2 classification.

### Step 9: Push the public branch

```bash
git push public public
```

### Step 10: Return to development

```bash
git checkout main   # or master
```

### Step 11: Update project instructions

Add a "Repository Architecture" section to your project's agent instructions file documenting remotes, branches, and the sync command.

### Step 12: Verify

```bash
git remote -v                    # Must show private + public
git branch -a                    # Must show main + public
git ls-remote --heads public     # Must show ONLY refs/heads/public
```

## After Setup: Ongoing Sync

Use your sync command to merge private changes to public:

```
/sync         # Full sync: merge → strip leaks → push public
/sync check   # Verify no private files on public branch
/sync status  # Show current state
```

## Leak Prevention Rules

1. Never push your private branch to the public remote — only the `public` branch
2. Always run the safety check after merging before pushing
3. Always verify remotes before pushing
4. If new private directories are created on the private branch, update the sync agent's exclusion list
5. If private files appear on the public repo, immediately delete with: `git push public --delete main`
