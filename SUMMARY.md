# Skills Arsenal — Quick Summary

## What This Is

A curated collection of **96 AI agent skills** — self-contained instruction modules that teach AI coding assistants how to use specific tools, frameworks, and methodologies. Organized into two categories: **universal skills** (broadly applicable) and **domain-specific skills** (organized by discipline).

**Updated 2026-06-02:** 48 universal + 35 domain-specific across 7 disciplines. 97 SKILL.md files total.

## Highlights

### Universal Toolkit (47 skills)

Skills useful in virtually any agentic project:
- **Development Lifecycle**: 23 agent-skills covering the full spec→plan→build→test→review→ship pipeline (Google engineering culture, Addy Osmani)
- **Research & Ideation**: 5 structured brainstorming/ideation/critical-thinking frameworks
- **Cognitive Tools**: Multi-perspective deliberation (12 archetypes), scenario analysis, hypothesis generation, cognitive fingerprinting
- **Knowledge Management**: Cross-referencing research against implementations, consulting-grade market reports
- **Data Access**: Unified API access to 78+ public databases (scientific, biomedical, economic)
- **Search Strategy**: Decision framework for 6 MCP search providers with fallback chains
- **CLI Mastery**: Comprehensive reference for jq, yq, fd, rg, pandoc, uv, repomix, gh, plus marker for PDF conversion
- **Jupyter Automation**: Headless notebook execution with automatic error detection and fix loops
- **Git & Repo Management**: Dual-remote Git architecture setup, sync, and safe commit/push workflows
- **Design Intelligence**: 161 reasoning rules, 67 UI styles, 161 palettes, 57 font pairings
- **LLM Observability**: LangSmith trace/debug/evaluate/monitor integration
- **Agent Vocabulary**: 62-term AI coding dictionary — precise language for agents, harnesses, context, sessions, tools, failure modes, work patterns
- **Skill Engineering**: Canonical-source architecture, per-IDE mirrors, dual .sh/.ps1 scripts, sync/bump automation, portable scripting — ship skills to 17+ AI coding platforms without drift

### Domain Depth (35 skills, 7 disciplines)

- **Quantitative Finance**: Ticker screening pipeline, trading paper distillation, US Treasury API
- **ML/Data Science**: Full lifecycle — classical ML, deep learning, Bayesian inference, survival analysis, interpretability, experiment tracking, zero-shot forecasting
- **LLM Engineering**: Complete stack from LangChain to vector DBs, LLM training (LitGPT/Axolotl/Unsloth/PEFT), DSPy prompt programming, speculative decoding
- **Autonomous Research**: 2 two-loop research architectures + 15-stage DeepScientist research operating system
- **Geospatial**: Remote sensing, GIS, satellite imagery analysis (500+ code examples)
- **Scientific Computing**: Complex network/graph analysis toolkit
- **Developer Tooling**: Auto-generate agent-friendly CLIs for any software + 40 community CLIs

### New Additions (2026-05-16)
- **23 agent-skills lifecycle skills** from Google engineering culture: spec→plan→build→test→review→ship pipeline
- **1 CLI-Anything skill**: 7-phase CLI generation pipeline, 40+ community CLIs, CLI-Hub discovery
- **1 AI Coding Dictionary**: 62-term glossary by Matt Pocock — models, sessions, tools, failure modes, handoffs, memory, work patterns

### Recent Additions (2026-06-02)
- **1 directed-document-research**: 5-phase pipeline for web research → download → convert → filter → report. Searches authoritative sources, batch-downloads PDFs, converts to markdown, reviews for relevance, deletes irrelevant, and reports findings. Works for any domain.

### Past Additions (2026-05-24)
- **1 multi-platform-skill-design**: 8-pattern architecture for cross-IDE compatibility from planning-with-files

### External Skill Curation

Identified, evaluated, and curated the highest-value skills from:
- **Agent Skills** (23 lifecycle skills from Google engineering, Addy Osmani)
- **K-Dense** (134 skills — curated top ~11 for universal + domain relevance)
- **Orchestra Research** (95 skills — curated top ~10 for LLM engineering)
- **DeepScientist** (15 stages — full research operating system from ResearAI)
- **GPT-Researcher** (autonomous web research agent)
- **CLI-Anything** (auto-generate agent CLIs, 40+ community CLIs)
- **AI Coding Dictionary** (62-term glossary by Matt Pocock)
- **Multi-Platform Skill Design** (cross-IDE architecture from planning-with-files)

## File Stats

| Metric | Value |
|--------|-------|
| Total files | ~600+ |
| SKILL.md instruction files | 97 |
| Total size | ~11.5 MB |
| Universal skills | 48 |
| Domain-specific skills | 35 |
| Domain-specific disciplines | 7 |

## Organization Philosophy

```
universal-skills/       → What every agent should know
domain-specific-skills/ → What a specialized agent masters
  ├── quantitative-finance/
  ├── ml-data-science/
  ├── llm-engineering/
  ├── autonomous-research/
  ├── geospatial/
  ├── scientific-computing/
  └── developer-tooling/
```

Skills aren't just documentation — they're **executable context** that transforms an AI agent from a generalist into a domain expert. Each skill decides when to activate, encodes workflows, prevents common errors, and provides deep references.
