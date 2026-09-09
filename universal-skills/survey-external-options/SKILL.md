---
name: survey-external-options
description: >
  Searches papers, existing GitHub projects, engineering guidelines, and
  forums (Stack Overflow and sibling sites, Discourse, Reddit, Hacker News),
  then evaluates each option and presents a ranked comparison. Hybrid
  invocation — activates on context match or when the LLM identifies
  relevance at any point. Use when the user asks to search for papers and
  existing projects and engineering guidelines and forums, survey how others
  solve a problem, find all options then compare, or evaluate approaches from
  literature plus GitHub plus practice. Do NOT use for cloning named GitHub
  URLs (use acquire-and-link-repos), page-by-page synthesis of already-held
  PDFs (use research-investigation), PDF-only gathering (use
  directed-document-research), search-tool routing alone (use
  mcp-search-strategy), or finding installable agent skills (use find-skills).
version: "0.1.1"
license: MIT
external_grounding: cite-only
metadata:
  skill-author: workspace
  invocation_posture: hybrid
---

# Survey External Options

Four-lane survey of an open problem: papers, existing projects, engineering
guidelines, and forums. Then evaluate every option and present a ranking.
Do not implement or clone during this skill.

## Related skills

- **Do NOT confuse with `directed-document-research`.** That skill gathers
  and filters PDFs. This skill owns the four-lane survey and the comparison.
  Load that skill only when scholarly PDFs must be downloaded.
- **Do NOT confuse with `research-investigation`.** That skill synthesizes
  materials already held, page by page. Use it only after this survey has
  stored documents the user then asks to investigate.
- **Do NOT confuse with `mcp-search-strategy`.** That skill picks search
  tools. Load it first. It does not evaluate options.
- **Do NOT confuse with `acquire-and-link-repos`.** Hand off only after the
  user names GitHub URLs and a link root.
- **Do NOT confuse with `find-skills`.** That skill finds installable agent
  skills, not problem-domain options.
- **Do NOT confuse with `repo-lifecycle`.** That skill manages clones already
  in a local reference-repo directory.

Before searching, load `mcp-search-strategy` and confirm which search tools are
callable. Before ranking, read your workspace's `standards/evaluation-framework.md`
(or its equivalent comparison standard) for the matrix and the
DEEPEN/BROADEN/PIVOT/CONCLUDE decision rules. When papers or arXiv appear,
check your local academic-papers catalog before downloading anything; see
your workspace's `standards/academic-papers.md` for the registration rule.

Lane queries and forum hosts: [references/lanes.md](references/lanes.md).

## When To Use

Activate on the opening prompt or mid-session when the user wants a
landscape of how others solved a problem, not a single known URL or a
local bug fix.

```
Need a ranked set of external options?
    |
    +-- User named clone URLs and a link root?
    |     -> acquire-and-link-repos only
    |
    +-- User handed local PDFs to synthesize?
    |     -> research-investigation only
    |
    +-- User asked for papers + projects + guidelines + forums,
    |   "what options exist", or "evaluate approaches"?
    |     -> this skill
    |
    +-- Otherwise
          -> do not load
```

## Workflow

1. Inspect callable search tools. Follow `mcp-search-strategy`. Name
   browser-goat only when it is callable and healthy. Escalate to Tavily
   for multi-source research and Exa for semantic code. Use GitHub search
   for repositories. Report a missing lane instead of inventing results.
2. Search locally first: the academic-papers catalog, the local
   `useful_repos/` reference clone directory, and any existing `projects/`
   tree. Do not re-download a cataloged paper. Do not clone a repo that
   already exists under `useful_repos/`.
3. Run the four lanes in parallel. Use at least two query angles per lane.
   Keep every hit until the extract step. See [references/lanes.md](references/lanes.md).
4. Filter after collection, not before. Drop marketing posts, unknown
   authors, student-only writeups, and sources that only mention the topic.
   Keep a source if it states a distinct option, mechanism, or measurement.
5. Register kept scholarly PDFs in the academic-papers catalog with tag
   `academic-papers`. Project notes cite catalog `id` values.
6. Extract every distinct option with no premature filter. Target ten or
   more when the topic is substantial. Then compare out loud using the
   evaluation-framework matrix: source, impact, cost, fit, risk, rank.
   Score GitHub repos on the 8-dimension matrix when a clone decision is
   on the table. End with DEEPEN, BROADEN, PIVOT, or CONCLUDE.
7. Present the ranking first. Use a Cursor canvas when the comparison is
   the deliverable. Do not dump a large table in chat when a canvas exists.
8. Stop. Do not clone, junction, or implement. If the user then names URLs
   and a link root, hand off to `acquire-and-link-repos`.

## Output

State the recommended option or stack, the decision
(CONCLUDE / DEEPEN / BROADEN / PIVOT), catalog ids for kept papers, repo
URLs with star and license facts, and which lanes were unavailable.

## User Usage

**Slash command:** /survey-external-options
**When to use it:** Fires when you want a landscape of how others have solved
an open problem — across papers, GitHub projects, engineering guidelines, and
practitioner forums — before committing to an approach.
**What it needs from you:** A clear problem statement and (optionally) the
workspace zone or project you are evaluating.
**What it gives back:** A four-lane survey, a ranked comparison matrix, and
a DEEPEN / BROADEN / PIVOT / CONCLUDE decision with the evidence behind it.
**What it won't do:** Clone repositories, implement anything, or replace
narrow search-and-link skills like `acquire-and-link-repos`,
`research-investigation`, or `mcp-search-strategy`.

## Governance

**LOCKED:** four lanes; local catalog before download; extract then
compare; no clone or implement in this skill; compose
`mcp-search-strategy`; academic PDFs go to `academic-papers`.

**IMPROVABLE:** forum host list; query phrasing; presentation layout.
