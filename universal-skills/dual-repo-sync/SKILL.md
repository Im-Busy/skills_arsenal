---
name: dual-repo-sync
description: Manages a dual-remote Git architecture where a private development repo syncs curated (non-sensitive) files to a public-facing repo. Handles branch curation, .gitignore management, merge safety checks, and leak prevention for data/models/outputs/experiments/reports/notebooks/logs.
version: 0.1.0
license: MIT
metadata:
  invocation_posture: manual-first
---
    skill-author: project
---

# Dual-Repo Sync — Private → Public Curation

## Architecture

```
Private Repo (origin)              Public Repo (public)
  main branch                        public branch
  [all files]                        [curated files only]

  git push origin main               git push public public
       │                                    │
       │  git checkout public               │
       │  git merge main                    │
       │  [safety check]                    │
       │  git push public public            │
       └────────────────────────────────────┘
```

## What Stays Private (ALWAYS excluded)

| Directory | Contents | Reason |
|-----------|----------|--------|
| `data/` | Datasets, CSVs, market data | Proprietary data |
| `models/` | Serialized ML model files | Serialized binaries |
| `outputs/` | Generated artifacts, ML runs | Run outputs |
| `experiments/` | Experiment results | Training runs |
| `reports/` | Generated analysis reports | Generated reports |
| `notebooks/` | Jupyter notebooks | Execution artifacts |
| `logs/` | Log files | Runtime output |
| `useful_resources/**` | Cloned repos, papers | Third-party content |
| `*.db` | Databases (mlflow, sqlite, etc.) | Tracking metadata |
| IDE config dirs | `.vscode/`, `.idea/`, etc. | Personal settings |
| `scripts/_archived/`, `scripts/archive/` | Obsolete scripts | Not public-ready |
| `src/*.egg-info/` | Auto-generated metadata | Build artifact |

## What Goes Public (curated showcase)

| Directory | Purpose |
|-----------|---------|
| `src/` | All source code |
| `tests/` | Full test suite |
| `scripts/` | CLI scripts (excluding archived) |
| `docs/` | Documentation, guides |
| Project root `.md` files | README, AGENTS, project docs |
| Project config files | pyproject.toml, lock files, IDE-agnostic config |

## Sync Workflow (CRITICAL ORDER)

### Step 1: Prepare
```bash
git checkout main && git pull origin main   # Latest private changes
```

### Step 2: Merge into public branch
```bash
git checkout public
git merge main
```

### Step 3: SAFETY CHECK — verify no private files leaked
```bash
git diff --name-only public@{1}..public | rg "^(data|models|outputs|experiments|reports|notebooks|logs)/|\.db$"
```

**If ANY output appears:** Files have leaked. Run cleanup:
```bash
git rm --cached -r data/ models/ outputs/ experiments/ reports/ notebooks/ logs/ 2>/dev/null
git rm --cached *.db 2>/dev/null
git commit -m "curate: remove leaked private files from public merge"
```

### Step 4: Push
```bash
git push public public
```

### Step 5: Return to development
```bash
git checkout main
```

## Leak Prevention Rules

1. **Never** push `main` branch to `public` remote — only push the `public` branch
2. **Always** run the safety check after `git merge main` before pushing
3. **Always** verify `git remote -v` shows `public` pointing to the public repo before pushing
4. **Never** add new tracked files to private directories on `main` without also adding `.gitignore` entries for them on `public`
5. If new directories with private data are created on `main`, update the public `.gitignore`

## Emergency: If Private Files Get Pushed to Public

1. **Immediately** delete the offending branch from public remote: `git push public --delete <branch>`
2. OR force-push a clean commit: `git push public --force`
3. Rotate any exposed credentials
4. Review GitHub commit history for the leaked data
