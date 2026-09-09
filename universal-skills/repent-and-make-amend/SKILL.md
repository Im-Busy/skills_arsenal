---
name: repent-and-make-amend
description: >
  Detects, diagnoses, and remediates default-branch divergence in git repositories.
  Hybrid invocation — activates when the agent (a) creates a new branch without
  verifying the default, (b) leaves a branch ahead of the default with no PR,
  (c) discovers stray mirror/staging branches sitting atop the default, or when
  the user reports a "I pushed to the wrong branch" incident. Use when the agent
  identifies branch drift, when a mirror workflow spills into the working branch,
  or when a "master" or "public" sentinel branch appears in a main-default repo.
  Do NOT use for routine single-branch development, scheduled maintenance of
  healthy repos, or when the user explicitly asks for a general git hygiene sweep
  (use workspace-housekeeping instead).
version: "0.1.0"
license: MIT
external_grounding: cite-only
metadata:
  skill-author: project
  invocation_posture: hybrid
---

# Repent and Make Amend

When the agent pushes to a non-default branch and leaves it unmerged — or when a
mirror workflow spawns a stray staging branch ahead of `main` — this skill
catches it, diagnoses the pattern, proposes the minimal fix, writes the apology
document, and closes the gap in standards so it cannot recur.

The word "repent" is literal. This skill exists because the agent *knows* the
right thing to do and still failed. The gap is not ignorance — it is the absence
of a pre-push gate. The fix is procedural, not conceptual.

---

## The Incident Pattern

The agent committed one or more of the following:

| # | Sin | Evidence |
|---|-----|----------|
| 1 | Created a branch named `master` in a `main`-default repo | Repo default = `main`; `master` exists and is ahead |
| 2 | Created a branch named `public` in a mirror-target repo | Repo default = `main`; `public` is ahead of `main` |
| 3 | Pushed to a non-default branch and left it without a PR | Divergent tip with no open PR to default |
| 4 | Pushed private content to a public remote branch | Remote-specific branch ahead of default on the public remote |
| 5 | Named a branch after its *content* rather than its *role* | `public` is a content label, not a role label |

---

## The Six Steps

### Step 1 — Discover the Damage

For each repo in scope (identified from the incident or provided by the user):

```
[M] Identify the repo's default branch
    → Run: git remote show origin | grep 'HEAD branch'   # bash/WSL/Git Bash
    → Or:  git ls-remote --symref origin HEAD            # portable; no parsing needed
    → Record: DEFAULT = <branch name>

[M] List all local and remote branches
    → Run: git branch -a
    → Record every branch whose tip is NOT on DEFAULT

[M] For each divergent branch, capture:
    → Branch name and remote
    → SHA of tip commit
    → List of commits unique to this branch: git log DEFAULT..<branch> --oneline
    → Whether the divergent branch has been pushed to a remote
```

**Stop signal:** If no branch is ahead of DEFAULT, the incident was a false alarm.
Stop and report.

### Step 2 — Classify the Divergence

| Class | Criteria | Remediation path |
|-------|----------|-----------------|
| **Working drift** | Commits on a named branch are legitimately ahead; PR exists | Open PR if missing, fast-forward merge |
| **Stray staging** | Mirror or CI pushed a branch that is meant to be ephemeral | Delete branch, do NOT merge |
| **Naming collision** | Branch name matches a remote-specific convention (`public`, `prod`) but repo uses a different default | Rename or delete per the naming rule in §1 of `references/default-branch-naming.md` |
| **Private spill** | A branch on the private remote is ahead of the shared default | Merge to default on private, then mirror |
| **Public spill** | A branch on the public remote contains private content | Hard STOP — do not push anything; escalate to user |

### Step 3 — Generate the Fix

For each divergent branch in class Working drift or Naming collision:

```
[M] Determine the correct merge strategy:
    → If divergent branch is a direct descendant of DEFAULT:
          Fast-forward merge via PR (preferred)
    → If divergent branch has diverged history:
          Three-way merge via PR; show the diff to the user before approving

[M] Generate the remediation command sequence:
    → Create PR: <branch> → DEFAULT (using gh or GitHub web URL)
    → After merge: git checkout DEFAULT && git pull && git branch -d <branch>
    → After local delete: git push origin --delete <branch>
    → Prune stale remotes: git remote prune origin
```

Present the command sequence to the user as a numbered checklist **before executing**.
Do NOT auto-execute the commands. Wait for explicit user approval.

### Step 4 — Write the Repentance Report

Author a markdown document at the root of the affected repo:

**Filename:** `REBRANCH-REMEDIATION.md`

**Schema:**

```markdown
# Branch Remediation Report

**Repo:** <owner/repo>
**Date:** YYYY-MM-DD
**Agent session:** <transcript id or date range>
**Default branch:** <main|master|trunk|other>

## What Went Wrong

| Sin # | Description | Branch | SHA |
|-------|------------|--------|-----|
| 1     | <description> | <branch> | <sha> |

## Root Cause

<2–3 sentences. Name the specific gap: no pre-push check, wrong default
branch assumption, missing naming rule, mirror workflow not documented.>

## Rule Gap

| Gap | File that should have caught it | Status |
|-----|--------------------------------|--------|
| Default branch not verified pre-push | `standards/git-branch-defaults.md` | Missing |
| Mirror workflow not documented | `standards/mirror-workflow.md` | Missing |

## Remediation Applied

| Branch | Action | PR link |
|--------|--------|---------|
| <branch> | Merged → default / Deleted | <link or N/A> |

## Prevention: Rule Changes Required

1. **<standards/git-branch-defaults.md>** — new file; see `references/default-branch-naming.md`
2. **<standards/mirror-workflow.md>** — new file; see `references/mirror-workflow-protocol.md`
3. **<AGENTS.md>** — add "verify default branch" to the Git Discipline checklist

## Acknowledgment

This incident was caught by [the agent | the user]. The agent takes full
responsibility for not applying the pre-push default-branch check. The fix
is procedural, not conceptual — the agent knew better.
```

### Step 5 — Propose Rule Gap Closures

After writing the repentance report, immediately surface these proposals:

**[A] Author `standards/git-branch-defaults.md`**

New file. Minimum content:

```markdown
# Git Default Branch Policy

## Rule 1: Always Verify Before Branching or Pushing

Before running `git checkout -b <name>` or `git push origin <name>`,
inspect the repo's default branch:

```bash
git remote show origin | grep 'HEAD branch'   # bash/WSL/Git Bash
# OR (faster, no network):
git symbolic-ref refs/remotes/origin/HEAD --short
```

If the default is `main`, do NOT create `master`. If the default is
`master`, do NOT create `main` unless the team has explicitly scheduled
a rename.

## Rule 2: Branch Names Must Be Role Labels, Not Content Labels

| Good | Bad | Why |
|------|-----|-----|
| `feature/xyz` | `xyz` | Unambiguous role |
| `fix/abc` | `abc` | Unambiguous role |
| `release/2026-09` | `public` | "public" describes content, not role |
| `release/2026-09` | `master` | Historical default is now a naming violation |

**Rationale:** A branch named `public` implies the content is public. A branch
named `master` implies it is the default. Neither is true if the repo's default
is `main`. A content-labeled branch ahead of the canonical default is, by
definition, unmerged divergence.

## Rule 3: Mirror Workflows Have Exactly One Target Branch

If a repo has a private → public mirror relationship, the public repo's
`main` is the **only** valid target. No intermediate staging branches
may exist on the public remote. If a staging branch appears, it was a
workflow error — delete it without merging.

## Rule 4: Pre-Push Checklist (copy into every new repo's AGENTS.md)

```
Before every `git push`:
1. git branch --show-current  → is this the default branch?
2. git remote -v             → is this the correct remote?
3. git log --oneline -3      → does this look right?
4. git status                → no untracked secrets or private files?
If any answer is unexpected: STOP and report before pushing.
```

## Default Branch Registry

| Repo | Default | Notes |
|------|---------|-------|
| <source-repo> | `main` | Private mirror source |
| <target-repo> | `main` | Public mirror target |

*Maintain this table. Add new repos as they are created.*
```

**[B] Author `standards/mirror-workflow.md`**

New file. Minimum content:

```markdown
# Mirror Workflow Policy

## Definitions

| Term | Meaning |
|------|---------|
| **Source repo** | The private repo where development happens |
| **Target repo** | The public repo that mirrors source |
| **Sync branch** | A dedicated branch on source used solely for mirror pushes |

## Protocol

1. Development happens on `main` (or a named feature branch off `main`).
2. When ready to sync, merge the feature branch into the **sync branch**
   on source.
3. Push the sync branch to source remote.
4. Pull or cherry-pick onto target `main`. **Do not push from target.**
5. The target has **exactly one** branch (`main`). No `public` branch.
6. If a `public` branch appears on the target, it is an error: delete it.
```

**[C] Update `<workspace>/AGENTS.md` — Git Discipline section**

Add to the pre-push checklist:

```
- Inspect `git remote show origin | grep 'HEAD branch'` before creating
  a new branch or pushing to a non-default remote.
- Never push to a branch named `master` if the repo default is `main`,
  and vice versa.
- Mirror repos: the public target has one branch (`main`). No staging
  branch may appear on the public remote.
```

### Step 6 — Verify and Attest

```
[M] Run completion attestation on the affected repos:
    → Capture: python scripts/completion_attestation.py capture --repo <repo-root> --scope ...
    → Verify: python scripts/completion_attestation.py verify --repo <repo-root> --scope ... --baseline ...

[M] Re-run audit-agent-routing.py if any MCP-related paths were affected.

[M] Update system-dossier:
    → If a new standard was authored, update research/system-dossier/SYSTEM.md
    → If a project repo state changed, update that project's SYSTEM.md
```

---

## Pre-Commit Hook (Optional Enhancement)

To prevent recurrence automatically, add a `pre-push` hook to any repo:

```bash
#!/bin/sh
# .git/hooks/pre-push
DEFAULT=$(git symbolic-ref refs/remotes/origin/HEAD --short | sed 's:origin/::')
CURRENT=$(git branch --show-current)
if [ "$CURRENT" != "$DEFAULT" ]; then
    echo "WARNING: pushing '$CURRENT' but default is '$DEFAULT'"
    echo "Did you mean to push to '$DEFAULT' instead?"
    read -p "Continue? (y/N) " confirm
    [ "$confirm" != "y" ] && exit 1
fi
```

Note: This is a manual install per repo. Do not automate its installation
across the workspace without user approval.

---

## Git Best Practices Reference (2026)

Source: GitHub `github/renaming` (2026), Git-Tower, Scott Hanselman.

| Practice | Recommendation | Source |
|----------|---------------|--------|
| Default branch name | `main` for all new repos | GitHub, 2020–present |
| Old repos on `master` | Rename if team agrees; maintain CI pipeline refs | GitHub renaming guide |
| `main` vs `master` in scripts | Check `init.defaultBranch` config; `git config --global init.defaultBranch main` | Git 2.28+ |
| Branch naming | Role labels (`feature/X`, `fix/Y`) over content labels (`public`, `stable`) | Git-Tower, industry consensus |
| Pre-push check | Verify default branch matches current branch before push | This skill's Step 1 |
| Mirror staging branch | One sync branch on source; target has only `main` | See `references/mirror-workflow-protocol.md` |

---

## User Usage

**Slash command:** `/repent-and-make-amend`
**When to use it:** Fires when the agent has pushed to the wrong branch, left
a branch ahead of the default with no PR, or created a stray mirror staging branch.
Also fires when the user says "I pushed to the wrong branch" or "there's a
`master`/`public` branch that shouldn't be there".
**What it needs from you:** The name of the affected repo(s), or the GitHub URL.
**What it gives back:** A diagnosis, a remediation checklist, a written apology
document, and proposed rule gap closures.
**What it won't do:** Routine scheduled maintenance (use workspace-housekeeping);
general git hygiene sweeps; push or merge without your approval.
