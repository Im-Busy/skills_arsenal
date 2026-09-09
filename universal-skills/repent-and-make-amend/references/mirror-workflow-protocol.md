# Mirror Workflow Protocol

## Definitions

| Term | Definition |
|------|-----------|
| **Source repo** | The private repository where development happens. All skill development, experimentation, and drafting occur here. |
| **Target repo** | The public repository that mirrors content from the source. Must be read-only for public contributors. |
| **Sync branch** | A dedicated branch on the source repo used exclusively to prepare content for mirroring. Named `sync` by convention. |
| **Publication branch** | A branch on the target repo used to receive mirrored content before merging to `main`. Named `publication` by convention — but the target repo must have **no such branch** if it is a pure mirror. |

## The Core Invariant

> The target repo has **exactly one** branch: `main`.

Any additional branch on the target is a workflow error. The branches `public`,
`staging`, `mirror`, `sync`, and `release` must not exist on the target remote.

## Two Mirror Patterns

### Pattern A: Pure Mirror (private source / public target)

Used when the target is a read-only public showcase.

```
Source (private)                          Target (public)
─────────────────                         ────────────────
main       ← development happens here
  │
  │  (when ready to publish)
  │
  ▼
sync       ← all published content passes through here
  │
  │  git push private sync
  │
  │  Pull or cherry-pick onto target main
  ▼
target/main    ← ONLY branch on target; never branched from
```

**Rules for Pattern A:**
1. Development is never on `main` directly if `main` is also the sync target. Use feature branches.
2. The `sync` branch receives merges from feature branches.
3. The `sync` branch is pushed to the private remote.
4. The operator manually pulls `sync` into the target's `main` (or cherry-picks the intended commits).
5. The target never has a `public`, `staging`, or `sync` branch.

### Pattern B: Fork-and-Sync (preferred for larger teams)

Used when the target accepts external contributions.

```
Source (public upstream)    Fork (personal public)
────────────────────        ─────────────────────
main  ← canonical state     main  ← synced from upstream
                              │
                              │  development happens here
                              ▼
                            feature/X  ← PR against fork main
                              │
                              │  approved and merged to fork main
                              ▼
                            upstream/main  ← maintainer pulls from fork
```

**Rules for Pattern B:**
1. The fork's `main` tracks the upstream's `main`.
2. Development uses feature branches on the fork.
3. PRs go to the fork maintainer's repo.
4. The upstream repo follows Pattern A rules.

## What Must Never Happen

| Forbidden action | Why | Evidence from incident |
|-----------------|-----|----------------------|
| Creating a `public` branch on the target | Content label confusion; the target IS the public content | `public` branch ahead of `main` in the mirror target repo |
| Creating a `master` branch on a `main`-default repo | Naming collision; `master` implies default | `master` branch ahead of `main` in the private source repo |
| Pushing from the target back to the source | The target is a downstream consumer, not a producer | — |
| Leaving a target branch ahead of `main` without a PR | The target's `main` is the canonical public state | GitHub "recent push" banner on divergent branch |
| Using a content label as a branch role | Causes confusion about which branch is authoritative | `public` implies content; `main` implies role |

## Step-by-Step Sync Procedure (Pattern A)

1. **[M]** Verify the source default branch is `main`:
   ```bash
   git symbolic-ref refs/remotes/private/HEAD --short
   # Expected: private/main
   ```

2. **[M]** Verify the target default branch is `main`:
   ```bash
   git remote -v
   # Expected: origin → <target-repo>.git
   git symbolic-ref refs/remotes/origin/HEAD --short
   # Expected: origin/main
   ```

3. **[M]** Ensure feature content is on a feature branch, not `main`:
   ```bash
   git branch  # Current branch shown with *
   ```

4. **[M]** Merge feature branch into `sync`:
   ```bash
   git checkout sync
   git merge --no-ff feature/<name>
   ```

5. **[C]** Push `sync` to private source:
   ```bash
   git push private sync
   ```

6. **[M]** Pull into target `main`:
   ```bash
   git checkout main
   git pull private sync
   # OR cherry-pick specific commits:
   git cherry-pick <sha>...
   ```

7. **[C]** Push target `main`:
   ```bash
   git push origin main
   ```

8. **[M]** Verify target remote has exactly one branch:
   ```bash
   git ls-remote --heads origin
   # Expected: exactly one line: <sha> refs/heads/main
   ```

## Naming Rules for Mirror Repos

| Repo | Default | Forbidden branches |
|------|---------|-------------------|
| Source (private) | `main` | `master`, `public` |
| Target (public) | `main` | `public`, `staging`, `mirror`, `sync`, `master` |

## The `repent-and-make-amend` Trigger

This protocol is broken when any of the following is observed:

1. The target remote has more than one branch (per `git ls-remote --heads origin`).
2. A branch named `public` exists on the target remote.
3. A branch named `master` exists in a `main`-default source repo.
4. The `sync` branch on the source has commits that are not reflected in target `main`
   after more than 24 hours.
5. A commit appears on a non-default branch with the commit message prefix
   `feat(public):` or `feat(public-mirror):` — this is scope-label confusion;
   the commit belongs on `main`, not on a named branch.

## Integration with `repent-and-make-amend`

When `repent-and-make-amend` detects a mirror workflow failure, it MUST:

1. Classify the divergence as **Public spill** or **Naming collision** per Step 2.
2. Follow the remediation in Step 3, preferring fast-forward merge over three-way merge.
3. Verify (Step 6) that `git ls-remote --heads origin` returns exactly one line
   after remediation.
4. Update the Default Branch Registry in `standards/git-branch-defaults.md`.
