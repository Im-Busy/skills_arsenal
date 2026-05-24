---
name: multi-platform-skill-design
description: Use when the user asks to make a project's skills or agent instructions work across multiple AI coding platforms (Kilo, Claude Code, Cursor, OpenCode, Codex, Gemini CLI, etc.). Provisions canonical-source architecture, per-platform SKILL.md mirrors, sync automation, and drift prevention. Use when refactoring a skill to support 3+ platforms, or setting up cross-IDE compatibility for a project.
allowed-tools: Read Write Edit Bash Glob Grep
license: MIT
metadata:
  skill-author: project
---

# Multi-Platform Skill Design

Provision a project's skills to work across 12+ AI coding platforms using the canonical-source architecture proven by planning-with-files.

## When to Activate

Activate this skill when the user:
- Says "make this work across multiple platforms" or "support Cursor/Claude/OpenCode/Codex/etc."
- Wants to prevent skill drift across different IDE directories
- Needs automated cross-platform sync for a skill or project
- Asks to "add multi-platform support" or "cross-IDE compatibility"

## Workflow

### Phase 1: Assess the Project

Examine the project to understand what exists:

1. Find the canonical skill directory. Common patterns:
   - `.kilo/skills/` (Kilo project)
   - `.claude/skills/` (Claude Code project)
   - `skills/` at repo root (generic)
   - If none exists, ask which platform is the primary one and what skills exist

2. List all SKILL.md files and their directory tree. Identify:
   - Number of distinct skills
   - Any shared assets (templates/, scripts/, references/)
   - Any existing platform directories (`.cursor/`, `.opencode/`, etc.)

3. Report findings to the user: "Found N skills in <canonical-dir>. No platform mirrors exist yet." or "Found mirrors in .cursor/ and .opencode/ but they're out of sync."

### Phase 2: Choose the Canonical Directory

The canonical directory is the single source of truth. All other platforms are mirrors.

| Situation | Canonical |
|-----------|-----------|
| Project already uses Kilo | `.kilo/skills/` |
| Project already uses Claude Code | `.claude/skills/` |
| Multi-platform from scratch | `skills/` at repo root |
| User specifies a preference | Whatever they say |

If no canonical directory exists, create it and copy/move existing SKILL.md files there.

### Phase 3: Create the Sync Script

Create `scripts/sync-platforms.py` at the project root. Use this template:

```python
#!/usr/bin/env python3
"""
sync-platforms.py — Sync skills from canonical to all platform mirrors.
SHA-256 comparison. Only changed files are touched. Never overwrites
platform-specific files (hooks.json, plugin manifests, etc.).

Usage:
    python scripts/sync-platforms.py           # Sync all platforms
    python scripts/sync-platforms.py --dry-run # Preview
    python scripts/sync-platforms.py --verify  # Check drift (exit 1 if found)
"""

import argparse
import shutil
import sys
import hashlib
from pathlib import Path

CANONICAL = Path("<CANONICAL_DIR>")  # e.g. ".kilo/skills" or "skills"

# List every subdirectory that contains a SKILL.md
SKILL_DIRS = [
    # Fill this in from Phase 1 — every skill directory name under CANONICAL
    # e.g. "gitnexus", "my-skill", "another-skill"
]

# Every platform that gets a mirror. Map: .platform-dir/ → skills subpath
PLATFORM_MANIFESTS = {
    ".claude":     ".claude/skills",
    ".codebuddy":  ".codebuddy/skills",
    ".codex":      ".codex/skills",
    ".continue":   ".continue/skills",
    ".cursor":     ".cursor/skills",
    ".factory":    ".factory/skills",
    ".gemini":     ".gemini/skills",
    ".hermes":     ".hermes/skills",
    ".kiro":       ".kiro/skills",
    ".mastracode": ".mastracode/skills",
    ".opencode":   ".opencode/skills",
    ".pi":         ".pi/skills",
}


def file_hash(path):
    try:
        return hashlib.sha256(Path(path).read_bytes()).hexdigest()
    except FileNotFoundError:
        return None


def sync_tree(src_dir, dst_dir, *, dry_run=False, verbose=True):
    stats = {"created": 0, "updated": 0, "skipped": 0}
    src_dir = Path(src_dir)
    dst_dir = Path(dst_dir)
    if not src_dir.exists():
        if verbose:
            print(f"    MISSING canonical: {src_dir}")
        return stats
    for src_file in sorted(src_dir.rglob("*")):
        if src_file.is_dir():
            continue
        rel = src_file.relative_to(src_dir)
        dst_file = dst_dir / rel
        src_h = file_hash(src_file)
        dst_h = file_hash(dst_file)
        if src_h == dst_h:
            stats["skipped"] += 1
            continue
        action = "created" if dst_h is None else "updated"
        stats[action] += 1
        if not dry_run:
            dst_file.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src_file, dst_file)
            if verbose:
                print(f"    {action.upper()}: {dst_file}")
        elif verbose:
            print(f"    WOULD {action}: {dst_file}")
    return stats


def verify_tree(src_dir, dst_dir):
    drifted = []
    src_dir = Path(src_dir)
    dst_dir = Path(dst_dir)
    if not src_dir.exists():
        return [f"{src_dir} (canonical missing)"]
    for src_file in sorted(src_dir.rglob("*")):
        if src_file.is_dir():
            continue
        rel = src_file.relative_to(src_dir)
        dst_file = dst_dir / rel
        src_h, dst_h = file_hash(src_file), file_hash(dst_file)
        if src_h and dst_h and src_h != dst_h:
            drifted.append(str(dst_file))
        elif src_h and not dst_h:
            drifted.append(f"{dst_file} (missing)")
    return drifted


def parse_args(argv=None):
    p = argparse.ArgumentParser(
        description="Sync skills from canonical to all platform mirrors."
    )
    p.add_argument("--dry-run", action="store_true", help="Preview without writing.")
    p.add_argument("--verify", action="store_true", help="Check drift; exit 1 if found.")
    p.add_argument("--quiet", action="store_true", help="Suppress per-file output.")
    return p.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    if not CANONICAL.exists():
        print(f"Error: Canonical source not found at {CANONICAL}/")
        print("Run from repo root.")
        sys.exit(1)

    label = "[DRY RUN] " if args.dry_run else "[VERIFY] " if args.verify else ""
    print(f"{label}Syncing from {CANONICAL}/\n")

    if args.verify:
        total_drift = 0
        for platform, mirror_base in sorted(PLATFORM_MANIFESTS.items()):
            mirror_dir = Path(mirror_base)
            if not mirror_dir.exists():
                continue
            print(f"  {platform}/")
            for skill in SKILL_DIRS:
                drifted = verify_tree(CANONICAL / skill, mirror_dir / skill)
                for d in drifted:
                    print(f"    DRIFT: {d}")
                    total_drift += 1
                if not args.quiet:
                    status = f"up to date" if not drifted else f"{len(drifted)} drifted"
            print()
        if total_drift > 0:
            print(f"DRIFT: {total_drift} file(s) out of sync.")
            print("Run 'python scripts/sync-platforms.py' to fix.")
            sys.exit(1)
        print("All platform mirrors in sync.")
        sys.exit(0)

    grand = {"created": 0, "updated": 0, "skipped": 0}
    for platform, mirror_base in sorted(PLATFORM_MANIFESTS.items()):
        mirror_dir = Path(mirror_base)
        print(f"  {platform}/")
        for skill in SKILL_DIRS:
            stats = sync_tree(CANONICAL / skill, mirror_dir / skill,
                              dry_run=args.dry_run, verbose=not args.quiet)
            for k, v in stats.items():
                grand[k] += v
            if args.quiet:
                c = stats["created"] + stats["updated"]
                if c > 0:
                    print(f"    {skill}: {c} changed ({stats['skipped']} skipped)")
        print()

    print("-" * 50)
    print(f"  Created: {grand['created']}  Updated: {grand['updated']}  Skipped: {grand['skipped']}")
    if args.dry_run:
        print("\n  Dry run. No files modified. Run without --dry-run to apply.")


if __name__ == "__main__":
    main()
```

Fill in `CANONICAL` and `SKILL_DIRS` from the Phase 1 findings. Example:
```python
CANONICAL = Path(".kilo/skills")
SKILL_DIRS = ["my-skill", "another-skill", "toolkit"]
```

### Phase 4: Run the First Sync

```bash
python scripts/sync-platforms.py
```

This creates all 12 platform mirrors. Then verify:

```bash
python scripts/sync-platforms.py --verify
```

Must show "All platform mirrors in sync."

### Phase 5: Create Version Bump Script (Optional)

If the project uses version numbers, create `scripts/bump-project-version.py`:

```python
#!/usr/bin/env python3
"""
bump-project-version.py — Atomically bump version across all parity-locked files.
Usage: python scripts/bump-project-version.py 1.2.0 [--dry-run]
"""

import argparse, re, sys, json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

PLATFORM_DIRS = [
    ".kilo", ".claude", ".codebuddy", ".codex", ".continue",
    ".cursor", ".factory", ".gemini", ".hermes", ".kiro",
    ".mastracode", ".opencode", ".pi",
]

SKILL_DIRS = [
    # Same list as sync-platforms.py
]

VERSION_RE = re.compile(r"^\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.\-]+)?$")


def find_all_skill_md_files():
    files = []
    for platform in PLATFORM_DIRS:
        platform_skills = REPO_ROOT / platform / "skills"
        if not platform_skills.exists():
            continue
        for skill in SKILL_DIRS:
            for skmd in (platform_skills / skill).rglob("SKILL.md"):
                files.append(skmd)
    return files


def bump_skill_md(path, new, *, dry_run=False):
    text = path.read_text(encoding="utf-8")
    pattern = re.compile(r'(version:\s*")([^"]+)(")')
    match = pattern.search(text)
    if not match:
        return None, f"no version field in {path}"
    old = match.group(2)
    if old == new:
        return old, None
    new_text = pattern.sub(rf'\g<1>{new}\g<3>', text, count=1)
    if not dry_run:
        path.write_text(new_text, encoding="utf-8")
    return old, None


def bump_json(path, new, *, dry_run=False):
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, FileNotFoundError):
        return None, f"invalid JSON: {path}"
    if "version" not in data:
        return None, f"no version field in {path}"
    old = data["version"]
    if old == new:
        return old, None
    data["version"] = new
    if not dry_run:
        path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    return old, None


def parse_args(argv=None):
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("new_version", help="Target semver, e.g. 1.2.0")
    p.add_argument("--dry-run", action="store_true")
    return p.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    new = args.new_version.lstrip("v")
    if not VERSION_RE.match(new):
        print(f"Error: '{new}' not valid semver.", file=sys.stderr)
        return 2

    print(f"{'[DRY RUN] ' if args.dry_run else ''}Bumping to {new}\n")

    changed, skipped, failures = 0, 0, []
    for path in find_all_skill_md_files():
        rel = path.relative_to(REPO_ROOT)
        old, err = bump_skill_md(path, new, dry_run=args.dry_run)
        if err:
            failures.append(err)
            print(f"  ERROR: {rel} ({err})")
        elif old == new:
            skipped += 1
        else:
            changed += 1
            print(f"  bumped: {rel}  {old} -> {new}")

    for json_file in ["kilo.json", "opencode.json"]:
        p = REPO_ROOT / json_file
        if p.exists():
            old, err = bump_json(p, new, dry_run=args.dry_run)
            if err:
                failures.append(err)
            elif old == new:
                skipped += 1
            else:
                changed += 1
                print(f"  bumped: {json_file}  {old} -> {new}")

    print(f"\nChanged: {changed}  Unchanged: {skipped}  Errors: {len(failures)}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
```

Fill in `SKILL_DIRS` matching the sync script. Fill in `PLATFORM_DIRS` (just copy the list shown — it covers all 13 platforms including canonical).

### Phase 6: Update AGENTS.md or CLAUDE.md

Inject a cross-platform architecture section into the project's agent instruction file (AGENTS.md, CLAUDE.md, or .cursorrules — whichever exists). The section must include:

1. **Canonical-source statement** — which directory is the single source of truth
2. **Sync command** — `python scripts/sync-platforms.py` and `--verify`
3. **Drift prevention rule** — "Never edit SKILL.md in `.cursor/skills/`, `.opencode/skills/`, etc. directly. Edit canonical only, then sync."
4. **Platform-skill-path table** — map each platform to its skill discovery path

Use these markers for idempotency:
```
<!-- multi-platform:start -->
...section content...
<!-- multi-platform:end -->
```

If AGENTS.md already has a `<!-- gitnexus:start -->` block or similar, inject the multi-platform section separately — it's a different concern. Wrap it in its own markers.

### Phase 7: Verify and Report

Run the final verification sequence:

```bash
# 1. Verify zero drift
python scripts/sync-platforms.py --verify

# 2. Dry-run to confirm idempotent (should show 0 changes)
python scripts/sync-platforms.py --dry-run

# 3. List all mirror directories
ls -d .*/skills/ 2>/dev/null
```

Report the final state:
```
Multi-platform architecture provisioned:
  Canonical: .kilo/skills/ (11 skills)
  Mirrors:   .claude/, .codebuddy/, .codex/, .continue/, .cursor/,
             .factory/, .gemini/, .hermes/, .kiro/, .mastracode/,
             .opencode/, .pi/
  Sync tool: scripts/sync-platforms.py (--verify passes, 0 drift)
  Docs:      AGENTS.md updated with cross-platform section
```

## Key Rules

- **Pick one canonical, stick with it.** Every edit to any SKILL.md starts in the canonical directory.
- **Run sync after every skill edit.** `python scripts/sync-platforms.py && python scripts/sync-platforms.py --verify`
- **Never edit mirror files directly.** They get overwritten by the next sync.
- **The canonical directory stays in the project as-is.** Don't rename it to `skills/` just to match a pattern — use whatever the project already has.
- **If the user's platform is missing from PLATFORM_MANIFESTS, add it.** The 12 listed cover Kilo, Claude Code, Cursor, OpenCode, Codex, CodeBuddy, FactoryAI, Gemini CLI, Hermes, Kiro, Mastra Code, Continue.dev, and Pi Agent. If the user mentions another platform (Cline, Roo Code, Augment Code, GitHub Copilot, Windsurf, BoxLite, AdaL, Antigravity, OpenClaw), add it to the manifest.

## Platform Skill Path Reference

When writing AGENTS.md sections or docs, use these platform-appropriate paths:

| Platform | Skill Path | Discovery Mechanism |
|----------|-----------|-------------------|
| Kilo | `.kilo/skills/<name>/SKILL.md` | Auto-loads from `.kilo/skills/` |
| Claude Code | `.claude/skills/<name>/SKILL.md` | Auto-loads from `.claude/skills/` |
| Cursor | `.cursor/skills/<name>/SKILL.md` | Skills system + optional hooks.json |
| OpenCode | `.opencode/skills/<name>/SKILL.md` | Skills or oh-my-opencode plugin |
| CodeBuddy | `.codebuddy/skills/<name>/SKILL.md` | Skills + hooks support |
| Codex | `.codex/skills/<name>/SKILL.md` | Skills + hooks.json |
| Gemini CLI | `.gemini/skills/<name>/SKILL.md` | Skills + settings.json hooks |
| Continue.dev | `.continue/skills/<name>/SKILL.md` | Skills + .prompt files |
| FactoryAI | `.factory/skills/<name>/SKILL.md` | Skills + hooks |
| Hermes | `.hermes/skills/<name>/SKILL.md` | Agent Skill |
| Kiro | `.kiro/skills/<name>/SKILL.md` | Agent Skills |
| Mastra Code | `.mastracode/skills/<name>/SKILL.md` | Skills + hooks |
| Pi Agent | `.pi/skills/<name>/SKILL.md` | Skills (npm package) |
| GitHub Copilot | `.github/copilot-instructions.md` | Custom instructions (no skills dir) |
| Cline | `.clinerules` | Rules file (no skills dir) |
| Roo Code | `.roorules` | Rules file (no skills dir) |
| Windsurf | `.windsurfrules` | Rules file (no skills dir) |
| Augment Code | `.augment/rules.md` | Rules file (no skills dir) |

Platforms in the last rows (Copilot, Cline, Roo Code, Windsurf, Augment) don't use `skills/` directories. For these, write a short meta-directive into their rules/config file pointing to AGENTS.md instead of mirroring skills.

## Anti-Patterns

| Don't | Why | Instead |
|-------|-----|---------|
| Edit mirror SKILL.md files | Creates drift | Edit canonical, then sync |
| Create sync script by hand in each project | Error-prone | Use the template in Phase 3 |
| Sync before canonical is committed | Mirrors won't survive checkout | Commit canonical first, then sync |
| Skip `--verify` after sync | Ships drift to contributors | Always run verify after sync |
| Hard-code paths specific to one developer's machine | Breaks for others | Use repo-relative paths (`Path(__file__).resolve().parents[1]`) |
| Create mirrors for rule-file platforms | Rules aren't skills | Write AGENTS.md redirect instead |
