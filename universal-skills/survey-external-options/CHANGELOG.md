# Changelog

All notable changes to the survey-external-options skill.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.1] - 2026-09-09

### Added
- `## User Usage` block so `/survey-external-options` is one of the
  one-liner answers to "should I redesign X?" — surveys across papers +
  projects + guidelines + forums and returns a ranked comparison
- `## Local workspace notes` section that holds the workspace-relative
  paths (`standards/`, `research/academic-papers/`, `useful_repos/`,
  `projects/`) so the staged public copy can be portable

### Changed
- Generalized workspace paths out of the body and into the
  local-workspace-notes section so the staged public copy survives
  the `skill-publishing-filter` device-specificity gate
- Regenerated `skill.json` with bumped version

## [0.1.0] - 2026-08-30

    10|### Added
- Four-lane survey (papers, GitHub projects, engineering guidelines, forums)
  with extract-then-compare evaluation and a stop-before-clone rule
- `references/lanes.md` for query angles and forum hosts
- Hybrid posture so agents load this skill from description match
