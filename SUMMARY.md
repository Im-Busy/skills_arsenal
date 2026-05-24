# Skills Arsenal — Quick Summary

## What This Is

A curated collection of **92 AI agent skills** — self-contained instruction modules that teach AI coding assistants how to use specific tools, frameworks, and methodologies. Organized into two categories: **universal skills** (broadly applicable) and **domain-specific skills** (organized by discipline).

**Updated 2026-05-24:** +1 multi-platform-skill-design (8-pattern architecture for cross-IDE compatibility from planning-with-files). 91 → 92 total.

## Highlights

### Universal Toolkit (45 skills)

Skills useful in virtually any agentic project:
- **Research & Ideation**: 5 structured brainstorming/ideation/critical-thinking frameworks
- **Cognitive Tools**: Multi-perspective deliberation (12 archetypes), scenario analysis, hypothesis generation
- **Knowledge Management**: Cross-referencing research against implementations, consulting-grade market reports
- **Data Access**: Unified API access to 78+ public databases (scientific, biomedical, economic)
- **Search Strategy**: Decision framework for 6 MCP search providers with fallback chains
- **CLI Mastery**: Comprehensive reference for jq, yq, fd, rg, pandoc, uv, repomix, gh
- **Jupyter Automation**: Headless notebook execution with automatic error detection and fix loops
- **Design Intelligence**: 161 reasoning rules, 67 UI styles, 161 palettes, 57 font pairings
- **LLM Observability**: LangSmith trace/debug/evaluate/monitor integration
- **Agent Vocabulary**: 62-term AI coding dictionary — precise language for agents, harnesses, context, sessions, tools, failure modes, work patterns
- **Skill Engineering**: Canonical-source architecture, per-IDE mirrors, dual .sh/.ps1 scripts, sync/bump automation, portable scripting — ship skills to 17+ AI coding platforms without drift

### Domain Depth (37 skills, 6 disciplines)

- **Quantitative Finance**: Ticker screening pipeline, trading paper distillation, US Treasury API
- **ML/Data Science**: Full lifecycle — classical ML, deep learning, Bayesian inference, survival analysis, interpretability, experiment tracking, zero-shot forecasting
- **LLM Engineering**: Complete stack from LangChain to vector DBs, LLM training (LitGPT/Axolotl/Unsloth/PEFT), DSPy prompt programming, speculative decoding
- **Autonomous Research**: 2 two-loop research architectures + 15-stage DeepScientist research operating system
- **Geospatial**: Remote sensing, GIS, satellite imagery analysis (500+ code examples)
- **Scientific Computing**: Complex network/graph analysis toolkit
- **Developer Tooling** (NEW): Auto-generate agent-friendly CLIs for any software + 40 community CLIs

### New Additions (2026-05-16)
- **23 agent-skills lifecycle skills** from Google engineering culture: spec→plan→build→test→review→ship pipeline
- **1 CLI-Anything skill**: 7-phase CLI generation pipeline, 40+ community CLIs, CLI-Hub discovery
- **1 AI Coding Dictionary**: 62-term glossary by Matt Pocock — models, sessions, tools, failure modes, handoffs, memory, work patterns

### External Skill Curation

Identified, evaluated, and curated the highest-value skills from:
- **K-Dense** (134 skills — curated top 11 for universal + domain relevance)
- **Orchestra Research** (95 skills — curated top 10 for LLM engineering)
- **DeepScientist** (15 stages — full research operating system)
- **GPT-Researcher** (autonomous web research agent)

## File Stats

| Metric | Value |
|--------|-------|
| Total files | ~600+ |
| SKILL.md instruction files | 93 |
| Total size | ~11.5 MB |
| Universal skills | 46 |
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
