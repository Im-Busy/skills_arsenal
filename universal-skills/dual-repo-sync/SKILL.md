---
name: dual-repo-sync
description: Manages a dual-remote Git architecture where a private development repo syncs curated (non-sensitive) files to a public-facing repo. Handles branch curation, .gitignore management, merge safety checks, and leak prevention for data/models/outputs/experiments/reports/notebooks/logs.
license: MIT
metadata:
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
| `data/` | 105 CSV files, 45 MB market data | Proprietary data |
| `models/` | 167 .pkl files, 34 MB ML models | Serialized binaries |
| `outputs/` | 739 files, 443 MB generated artifacts | ML run outputs, parquet |
| `experiments/` | 105 files, experiment results | Training runs |
| `reports/` | 367 files, 24 MB analysis | Generated reports |
| `notebooks/` | 73 files, 17 MB Jupyter | Execution artifacts |
| `logs/` | Log files | Runtime output |
| `useful_resources/**` | 152 files, cloned repos/papers | Third-party repos |
| `mlflow.db` | MLflow tracking database | Training metadata |
| `.vscode/`, `.roo/`, `.kilocode/` | IDE/config dirs | Personal settings |
| `scripts/_archived/`, `scripts/archive/` | Obsolete scripts | Not public-ready |
| `src/investment_trying.egg-info/` | Auto-generated metadata | Build artifact |

## What Goes Public (curated showcase)

| Directory | Files | Purpose |
|-----------|-------|---------|
| `src/` | 536 files | All source code (patterns, ML, backtest, risk, portfolio) |
| `tests/` | 119 files | Full test suite |
| `scripts/` | 77 files (excl. archived) | CLI scripts |
| `docs/` | 32 files | Documentation, guides |
| `progress_docs/` | 88 files | Project plans, handovers |
| `.kilo/agent/` | 4 files | AI agent definitions |
| `.kilo/command/` | 5 files | Slash commands |
| `.kilo/skills/` | 25+ files | Skill definitions |
| `.useful_commands/` | 10 files | Command reference |
| `pipeline/` | 4 files | Pipeline definitions |
| `BESTS.md`, `AGENTS.md`, `README.md` | 3 files | Project landing docs |
| `pyproject.toml`, `uv.lock`, `kilo.json` | 3 files | Project config |

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
git diff --name-only public@{1}..public | findstr /R "^data\|^models\|^outputs\|^experiments\|^reports\|^notebooks\|^logs\|^mlflow"
```

**If ANY output appears:** Files have leaked. Run cleanup:
```bash
git rm --cached -r data/ models/ outputs/ experiments/ reports/ notebooks/ logs/ 2>$null
git rm --cached mlflow.db 2>$null
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
5. If new directories with private data are created on `main`, update `.kilo/skills/dual-repo-sync/SKILL.md` and the public `.gitignore`

## Emergency: If Private Files Get Pushed to Public

1. **Immediately** delete the offending branch from public remote: `git push public --delete <branch>`
2. OR force-push a clean commit: `git push public --force`
3. Rotate any exposed credentials
4. Review GitHub commit history for the leaked data
