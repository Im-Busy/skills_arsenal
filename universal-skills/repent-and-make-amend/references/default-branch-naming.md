# Default Branch Naming

## The One Rule

> A branch name must always describe its **role**, never its **content**.

This single rule prevents the two failures that produced `repent-and-make-amend`:
`master` (a content label — "this is the master copy") used as if it were a role label,
and `public` (a content label — "this is the public content") used as a staging branch name.

## Role vs. Content

| Category | Role label | Content label | Why content is wrong |
|----------|-----------|--------------|---------------------|
| Action | `feature/x`, `fix/y`, `refactor/z` | `new-stuff`, `my-work` | Role is precise; content is vague |
| Environment | `dev`, `staging`, `prod` | `public`, `private` | Stage is a deployment target; public/private describes data classification |
| History | `main`, `master` (historical) | `release`, `stable` | `main` says "this is where things converge"; `stable` says "this has passed tests" — both are role-adjacent but `stable` as a branch name implies a release channel, not a role |
| Temporal | `release/2026-09`, `hotfix/abc` | `september`, `old` | Role includes time; time alone is not a role |

## The `main` Rule

`main` is the industry-standard default branch name (GitHub, GitLab, Bitbucket — all
default to `main` for new repos as of 2020–present). It is a **role label**: "this is
the mainline, the convergence point, the canonical state."

- `main` is **correct** for any repo that serves as a publication or sync target.
- `master` is a **legacy default** from older Git versions. It is not wrong, but it
  is not preferred, and mixing `master` and `main` in the same remote topology is
  an error.
- If a repo has `master` as its default, do not create a `main` branch in that repo
  unless the team has explicitly scheduled a rename.

## The No-Staging-Branch Rule

Public mirror repos must have **exactly one** branch: `main`. Any additional branch
is by definition a workflow error. The following are all wrong:

| Wrong branch name | Why it's wrong | What to do instead |
|-----------------|---------------|-------------------|
| `public` | Content label; implies the content is public; not a role | Delete it; push only to `main` |
| `staging` | Implies a deployment stage on the public mirror; the public mirror is not a deployment target | Delete it; use a sync branch on the private source only |
| `mirror` | Named after the workflow, not the role | Delete it; the sync happens via PR into `main` |
| `private` | Content label; the public repo should not have private content | Hard STOP; do not merge without user approval |

## Pre-Branch Verification (the gate that `repent-and-make-amend` exists to close)

Before every `git checkout -b` or `git push origin <name>`:

```bash
# Always run this first — it costs one network round-trip and prevents one incident
git remote show origin | grep 'HEAD branch'   # bash/WSL/Git Bash

# Faster, no network:
git symbolic-ref refs/remotes/origin/HEAD --short
# Output: origin/main  ← this is the default
```

If the command returns `origin/main`:
- Do NOT create `master`
- Do NOT create a branch with a content label (`public`, `private`, `stable`)

If it returns `origin/master`:
- Do NOT create `main`
- Do not push to a new `main` unless the team has scheduled the rename

## The Default Branch Registry

Every repo in the workspace that has a remote must have an entry in the registry
in `standards/git-branch-defaults.md`. The registry is the single source of truth
for "what is the default branch of this repo?"

```
| Repo                    | Default | Type       | Notes                              |
|-------------------------|---------|------------|------------------------------------|
| <source-repo>           | main    | private    | Development source; mirror source   |
| <target-repo>           | main    | public-mirror | Public target; one branch only    |
```

Add an entry when:
- A new remote is added to any worktree
- A default branch is renamed
- A repo is archived or deleted

## Anti-Patterns

| Anti-pattern | The failure it causes |
|-------------|----------------------|
| Creating `master` in a `main`-default repo | `master` drifts ahead of `main` with no PR; appears as "recent push" on GitHub |
| Creating `public` as a staging branch on a public mirror | Mirror is supposed to have one branch; `public` is content-label confusion |
| Not checking `git remote show origin` before branching | The agent assumes based on habit or prior repo; the assumption is wrong |
| Pushing to a non-default branch without immediately opening a PR | The branch accumulates commits that are not reviewed |
| Using `git init --initial-branch=master` | Spreads the legacy default; `git init --initial-branch=main` is the correct form |
