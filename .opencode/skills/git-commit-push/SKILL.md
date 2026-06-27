---
name: git-commit-push
description: Safely commits and pushes current changes with dual-repo awareness. Auto-detects branch, stages files appropriately, commits with conventional message format, and pushes to the correct remote. Prevents pushing private branches to public remotes. Works with both single-remote and dual-remote architectures.
license: MIT
metadata:
    skill-author: project
---

# Git Commit & Push — Repository-Aware

Commit and push current working tree changes, respecting repository architecture.

## Pre-Flight Checks

### 1. Determine repository architecture

```bash
git remote -v
git branch --show-current
```

Results tell you:
- **Single remote** (`origin` only): standard push to origin
- **Dual remote** (`private` + `public`, or `origin` + `public`): requires branch-aware routing
- Current branch determines the push target

### 2. Review what will be committed

```bash
git status
git diff --stat
git diff --cached --stat
```

### 3. If code intelligence tools are available

Check for `detect_changes` or similar impact analysis tools. If available, run them to verify changes only affect expected symbols. Warn if unexpected scope detected.

## Staging

### What to stage

Stage source files, tests, docs, configs, and infrastructure files.

**Rules:**
- Stage source files, tests, documentation, configs
- Stage new infrastructure files (agents, commands, skills)
- **Never** stage IDE configs (`.vscode/`, `.idea/`, `.claude/`, `.cursor/`)
- **Never** stage index files (`.some-index/`)
- **Never** stage secrets (`.env`, credentials, tokens)
- **Never** stage agent memory files unless explicitly asked
- If uncertain about a file, ask before staging

### Verify staged changes

```bash
git diff --cached --stat
```

## Commit

### Message format

Use conventional commit style:

```
<type>: <description>

<optional body>
```

**Types:**
| Type | When to use |
|------|------------|
| `feat` | New feature or capability |
| `fix` | Bug fix |
| `infra` | Infrastructure, tooling, CI, skills, agents |
| `docs` | Documentation only |
| `chore` | Maintenance, cleanup, curation |
| `test` | Tests only |
| `refactor` | Code restructuring (no behavior change) |

**Examples:**
```
infra: add dual-repo sync infrastructure (whitelist, sync agent, command, skill)
feat: add platform auto-detection for config generation
fix: handle edge case in config merge
chore: curate public branch - strip IDE configs and internal docs
```

### Execute commit

```bash
git commit -m "<type>: <description>" -m "<optional body>"
```

## Push

### Dual-remote architecture

```
On main/master branch → git push private main
On public branch      → git push public public
```

**CRITICAL: Never push the private branch to the public remote. Never push the public branch to the private remote.**

Verify before pushing:
```bash
git branch --show-current          # Confirm branch
git remote get-url public           # Confirm public remote URL
git remote get-url private          # Confirm private remote URL
```

### Single-remote architecture

```
git push origin <current-branch>
```

## Post-Push Verification

```bash
git status                         # Working tree clean
git log --oneline -3               # Confirm commit is latest
```

For dual-remote, verify public only has the public branch:
```bash
git ls-remote --heads public       # Should show only refs/heads/public
# If refs/heads/main appears, private files may have leaked
```

## Safety Rules (NEVER DO)

- NEVER `git push --force` on shared branches without explicit request
- NEVER push the private branch to the public remote in dual-repo setup
- NEVER skip hooks (`--no-verify`, `--no-gpg-sign`) unless explicitly requested
- NEVER amend commits that were already pushed to a remote
- NEVER commit files containing secrets or credentials
- NEVER commit binary artifacts (`.pkl`, `.parquet`, `.zip`, `.tar`) without explicit request

## Full Workflow

```
git status
git diff --stat
git add <files>
git diff --cached --stat                     # verify staging
git commit -m "<type>: <description>"
git branch --show-current                    # confirm target
git push <remote> <branch>                   # push to correct remote
git status                                   # verify clean
```
