---
name: ai-coding-dictionary
description: 62-term glossary of AI coding vocabulary by Matt Pocock. Use when encountering unfamiliar AI coding terminology, need to clarify agent/harness/tool concepts, or want precise language for AI tooling discussions. Activates on terms like "context window", "harness", "session", "tool call", "hallucination", "attention degradation", "handoff", "compaction", etc.
allowed-tools: Read
license: CC0 (public domain glossary adapted from dictionary-of-ai-coding)
metadata:
  source: https://github.com/mattpocock/dictionary-of-ai-coding
  author: Matt Pocock
  terms: 62
---

# AI Coding Dictionary

62 terms defining the vocabulary of AI coding — translated into plain English by Matt Pocock. Organized into 7 sections covering models, sessions, tools, failure modes, handoffs, memory, and work patterns.

## Why This Exists

AI coding jargon creates confusion. The same concepts — context, sessions, tool calls — are described differently across Cursor, Claude Code, Copilot, and other tools. This dictionary provides a single, precise vocabulary that cuts through vendor-specific terminology.

Load this skill when you need to:
- Understand why an agent is behaving unexpectedly (attention degradation, sycophancy)
- Structure multi-session work (handoffs, specs, tickets)
- Debug token usage and billing (prefix cache, input/output tokens)
- Design agent workflows (progressive disclosure, AFK, human-in-the-loop)

---

## Section 1 — The Model (14 terms)

### Model

The [parameters](#parameters). [Stateless](#stateless) — does [next-token prediction](#next-token-prediction) and nothing else. "Claude Opus 4.7" and "GPT-5" are models. On its own a model can't do anything agentic; it has to be [harnessed](#harness).

*Avoid:* "the AI", "the bot" (too vague).

### Parameters

The numbers inside a model — often billions of them — tuned during [training](#training). Everything the model "knows" lives in them. Training sets them; [inference](#inference) uses them unchanged. Also called *weights*.

### Training

The process that sets a model's parameters, by exposing it to vast amounts of text and adjusting parameters to improve [next-token prediction](#next-token-prediction). A one-time, expensive process done by the [model provider](#model-provider).

### Inference

Running a trained model to generate output — what happens on every [model provider request](#model-provider-request). Parameters stay fixed; the model just does [next-token prediction](#next-token-prediction) over the [context](#context) it's given. Cheap relative to training, but billed per [token](#token) and the dominant cost of using a model.

### Token

The atomic unit a model reads and writes. Roughly word-sized but not exactly — common words are one token, rare or long ones split into several. [Context window](#context-window) size, cost, and latency are all counted in tokens.

*Avoid:* "word" — token boundaries don't match word boundaries.

### Next-token prediction

What the model actually does. Given a [context](#context), it samples one next token, appends it, and runs again. Every output — a sentence, a [tool call](#tool-call), a thousand-line file — is built one token at a time.

### Non-determinism

The same input can produce different output. Run a model twice with identical context and you may get two different answers. It's a property of how models generate text — there's no setting you can flip to make it go away. Be careful not to over-narrativize pattern of good/bad runs.

### Model provider

Whatever serves a model for inference. Usually a remote service (Anthropic, OpenAI, Google), but can also be local — Ollama, LM Studio, llama.cpp. The [harness](#harness) doesn't run the model itself; it asks a provider to.

### Harness

Everything around the model that turns it into an [agent](#agent): [tools](#tool), [system prompt](#system-prompt), context-window management, permissions, hooks. Claude.ai and Claude Code run on the same model but behave differently because their harnesses differ.

### Model provider request

One round-trip from the harness to the model provider. The harness sends the current context; the provider returns one response (a [tool call](#tool-call) or a final answer). A single user message can spawn many model provider requests if the agent calls tools.

### Input tokens

Tokens the harness sends on each model provider request. Billed at a lower rate than [output tokens](#output-tokens).

### Output tokens

Tokens the model generates back. Billed at a higher rate than input tokens, since they cost more compute to produce.

### Prefix cache

The provider-side store that lets consecutive model provider requests skip re-processing a shared prefix. When the start of a request matches the start of a recent one, the provider reuses its prior work and bills those tokens as [cache tokens](#cache-tokens) at a much lower rate. Anything that changes the prefix (reordering files, injecting a timestamp) invalidates the cache.

### Cache tokens

Input tokens the provider has cached from a previous model provider request so it doesn't have to re-process them. Billed at a much lower rate. The lever that makes long [sessions](#session) affordable.

---

## Section 2 — Sessions, Context Windows & Turns (8 terms)

### Stateless

Carries no information forward. The model is stateless across model provider requests — each request resends the full [context window](#context-window). An [agent](#agent) is stateless across [sessions](#session) by default: a new session starts empty. Counterpart to [stateful](#stateful).

### Context

The relevant information the agent has access to right now. The abstract noun — not the raw input the model sees (that's the [context window](#context-window)), not the running history (that's the [session](#session)), but *what the agent knows that's pertinent to the task*. "Loading something into context" means making it part of this set; "context engineering" is the discipline of curating it.

### Context window

Everything the model sees on each model provider request. Finite, model-specific, and the *only* surface through which the model perceives anything.

*Avoid:* "memory" — the context window is working state and doesn't persist across [sessions](#session).

### Stateful

Carries information forward. A [session](#session) is stateful across turns — context accumulates as the session runs, which is why long sessions drift into the [dumb zone](#smart-zone). An agent can be made stateful across sessions by adding a [memory system](#memory-system). The model is never stateful; any apparent continuity is the harness re-feeding context.

### Agent

A model harnessed with [tools](#tool), a [system prompt](#system-prompt), and a [context window](#context-window), that takes turns with a user. *Claude Code is an agent. Cursor is an agent. Claude.ai is an agent.* An agent is what you actually talk to — it's the model in motion, configured for a purpose.

*Avoid:* "the AI", "the bot" (too vague — they hide whether you mean the parameters or the harnessed thing).

### System prompt

The instructions the harness prepends to every model provider request — the agent's standing brief: who it is, how to behave, which [tools](#tool) it can call, what conventions to follow. Usually stable across a [session](#session).

### Session

One bounded run of interaction with an agent. Starts empty, accumulates messages, [tool results](#tool-result), and files read, and ends when [cleared](#clearing), closed, or [compacted](#compaction) into a fresh session. The session is what *fills* the context window.

### Turn

One user message plus everything the agent does in response, up until it yields back to the user. Contains one or more model provider requests — many, if the agent calls [tools](#tool). The hierarchy is: Session > Turn > Model provider request.

---

## Section 3 — Tools & Environment (10 terms)

### Environment

The world the agent acts on — anything outside the [harness](#harness) that the agent perceives through [tool results](#tool-result) and changes through [tool calls](#tool-call). A [filesystem](#filesystem) is the most common kind of environment, but not the only one (a database, a remote API, a browser session can all be environments).

### Filesystem

A tree of files and directories the agent reads from, writes to, and executes within — the default kind of [environment](#environment) for a coding agent. [AGENTS.md](#agentsmd), [skills](#skill), source code, build scripts, and tool configs all live in a filesystem.

### Tool

A function the harness exposes for the agent to call — Read, Write, Bash, Search. Tools are how an agent perceives and acts on the [environment](#environment): it can't see the environment except through [tool results](#tool-result), and can't change it except through [tool calls](#tool-call).

### Tool call

The model's output naming a tool and its arguments — just structured text. It doesn't do anything on its own; the harness has to read it and execute. Produced by the model in one model provider request.

### Tool result

What the harness sends back after executing a [tool call](#tool-call) — the file contents, the command output, the error. The agent's only window onto the [environment](#environment).

### MCP

**Model Context Protocol.** A protocol for plugging external tool servers into a harness — how an agent gets tools beyond what the harness ships with. The agent never "calls MCP"; it calls a tool, and the harness happens to have gotten that tool from an MCP server.

### Permission request

What the harness shows the user before executing a tool call that isn't pre-approved. The mechanism by which a harness puts a human in the [loop](#human-in-the-loop) for risky or sensitive actions.

### Permission mode

The permission-gating slice of an [agent mode](#agent-mode) — which tool calls trigger a permission request and which run automatically.

### Agent mode

A preset that shapes how the agent operates at runtime — bundles a permission mode with behavioral instructions injected into the [system prompt](#system-prompt). Examples: a default that prompts on risky calls, a **plan mode** that blocks edits, a **bypass permissions** mode (YOLO mode) that auto-approves everything.

### Sandbox

An isolated [environment](#environment) the agent runs inside — a container, VM, ephemeral filesystem, or restricted-permission shell. Limits the blast radius of agent actions. The safety substrate that makes [AFK](#afk) practical.

---

## Section 4 — Failure Modes (9 terms)

### Sycophancy

Confidently agreeable model output. Caused by [training](#training): the model was shaped to favor answers humans liked, and humans tend to like agreement more than they like being told they're wrong.

*Surfaces as:* Caving under pushback, praising bad input, biased framing, mimicry.

*Diagnostic test:* would the model have said this without your steer?

*Fix:* hide your preferences. Phrase prompts neutrally.

### Hallucination

Confidently-wrong model output. Two flavors:
- **Factuality hallucination** — invented or wrong facts about the world. Caused by [parametric knowledge](#parametric-knowledge) gaps. Fix: load the right [contextual knowledge](#contextual-knowledge).
- **Faithfulness hallucination** — output drifts from the contextual knowledge that's loaded. Symptom of [attention degradation](#attention-degradation). Fix: [clear](#clearing) or [compact](#compaction).

*Avoid:* "hallucination" as a bare synonym for "wrong" — without naming the flavor, the term has no diagnostic value.

### Parametric knowledge

What the model "knows" from training, stored in its parameters. Frozen at training time. Source of fluency on common topics, and of fabrication on uncommon ones. Counterpart to [contextual knowledge](#contextual-knowledge).

### Knowledge cutoff

The date past which a model has no parametric knowledge. Libraries, APIs, and events from after the cutoff are fabrication traps unless their docs are loaded as contextual knowledge.

### Contextual knowledge

Facts the agent can read directly from the [context](#context) right now — the user's task, files the agent has read in, [tool results](#tool-result), [AGENTS.md](#agentsmd) content. Counterpart to parametric knowledge: parametric is *recalled*; contextual is *read*. Hallucinations are much less common when the agent works from contextual knowledge.

*Avoid:* "working memory" — contextual knowledge is what's in the window *now*; a memory system is what gets cross-session content into it.

### Attention relationship

When predicting each token, the model factors in every other token in the context — some heavily, others barely at all. The pairing between two tokens is an attention relationship. A context of N tokens has on the order of N² relationships.

### Attention budget

Each token has a finite amount of influence to distribute across the rest of the context. Heavy influence on one relationship leaves less for others. The budget is per-token and doesn't grow when the context does, which is why long sessions dilute.

### Attention degradation

As a session grows, each token's attention budget is spread across more competitors. The signal on any one meaningful relationship shrinks; noise from irrelevant context crowds in. Cause of the smart zone / dumb [zone effect](#smart-zone).

### Smart zone

Early in a session the agent is in a "smart zone" — sharp, focused, recall is good. As the session grows it drifts into a "dumb zone": sloppier, forgetful, more mistakes — and more faithfulness [hallucinations](#hallucination). On frontier models, the dumb zone commonly begins around 100,000 tokens. [Clear](#clearing) or [compact](#compaction) when the session bloats; don't push through.

---

## Section 5 — Handoffs (7 terms)

### Clearing

Ending the current [session](#session) and starting a fresh one. The next message begins with an empty session and an empty context window. Usually user-driven.

### Handoff

Transferring agent context from one session to another, with no return path. The carry mechanism varies — a written [handoff artifact](#handoff-artifact), an in-memory summary ([compaction](#compaction)). Reasons: switching roles (planner → implementer), kicking off an AFK run, fanning out to parallel sessions, or freeing up context window room.

### Handoff artifact

A document used as the carry mechanism for a [handoff](#handoff) — written by one session to be read by another. One way among several (see also compaction).

### Spec

A handoff artifact describing a multi-session piece of work — what's being built, not how each session does its share. Mutates as work progresses. Made of [tickets](#ticket).

### Ticket

A handoff artifact scoping one session of work. Stands alone, or hangs off a [spec](#spec) as one of its children. Tickets can block or be blocked by sibling tickets.

### Compaction

A handoff done in-memory: the previous session's history is summarised and seeds a fresh session. Lossy — detail traded for headroom. Triggered manually by the user, or [automatically](#autocompact).

### Autocompact

Compaction triggered automatically by the harness when the context window approaches full.

---

## Section 6 — Memory and Steering (6 terms)

### Memory system

A system that attempts to make an agent [stateful](#stateful) across [sessions](#session). Persists information into the [environment](#environment) during a session and reloads it into the context window at the start of future ones.

### AGENTS.md

A file in the environment that the harness loads into the context window at session start — the project's standing brief to the agent. Cross-harness convention.

*Avoid:* using AGENTS.md for content that should be [progressively disclosed](#progressive-disclosure) — anything in it pays a token cost every turn.

### Progressive disclosure

Loading only the context an agent needs right now, with [context pointers](#context-pointer) to the rest. Borrowed from UI design.

### Context pointer

A mention in one document that points to another, so the agent can pull it into the context window only when the task calls for it. The unit [progressive disclosure](#progressive-disclosure) is built from.

### Skill

A teachable capability bundled as a unit — instructions and resources for doing one task well, kept in the environment until a context pointer pulls it into the context window for the task at hand. The unit of progressive disclosure in a harness.

*Avoid:* "tool" — a tool is what the agent *calls*; a skill is instructions it *reads*.

### Subagent

An agent spawned by another agent via a tool call. Runs in its own session with its own context window, and reports a single tool result back. Distinct from a [handoff](#handoff) — the parent specifically expects a return. Cannot spawn further subagents — the tree is one level deep.

---

## Section 7 — Patterns of Work (8 terms)

### Human-in-the-loop

A working pattern where one or more humans pair with the agent during a session — reviewing, redirecting, or collaborating in real time. The human is present and engaged, not just gating individual actions.

### AFK

Away from keyboard. A working pattern where the user kicks off a session and leaves the agent to run unattended. The throughput multiplier of AI coding — many AFK sessions can run in parallel. Usually requires a permissive permission mode plus [sandboxing](#sandbox) to be safe.

*Avoid:* "background agent" — centers the machine rather than the human pattern.

### Automated check

A deterministic verification that runs in the environment — tests, type checks, lints, build, pre-commit hooks. Pass/fail, no judgement. The signal an agent can self-correct from without involving anyone else.

*Avoid:* "feedback loop" / "backpressure" — both lump checks together with review. "test" — tests are automated checks, but not all automated checks are tests.

### Automated review

An agent reviewing another agent's work, often with a different model or system prompt. Non-deterministic: it forms a judgement. Runs anywhere — pre-merge on a PR, post-hoc on commit history, mid-session as a subagent.

*Avoid:* "AI review" / "agent review" — too vague to distinguish from the working agent itself.

### Human review

The user reading the code the agent produced and forming a judgement on it. Reading the diff or the changed files counts; reading the agent's *description* of what it did does not — narration is not the artifact.

### Vibe coding

A working pattern where the user accepts the agent's code without human review. The diff is treated as opaque — what matters is whether the program behaves, not what's inside.

*Avoid:* "vibe coding" as a synonym for "low-quality AI coding" — the term names the review stance, not the resulting code.

### Design concept

The shared understanding of what's being built, held in common between user and agent but separate from any asset. Brookes' term (*The Design of Design*): the conversation, handoff artifacts, and the code are all assets that try to capture or reach the design concept, but none of them *are* it.

### Grilling

A technique for developing a design concept with an agent: the agent interviews the user Socratically, one decision at a time, proposing a recommended answer for each. Slows the rush to a finished plan — no handoff artifact is written until the concept stabilises.

---

## Quick Reference

| Term | Category | One-liner |
|------|----------|-----------|
| Model | Model | The parameters; stateless, does next-token prediction only |
| Parameters | Model | The numbers (weights) tuned during training |
| Training | Model | One-time process that sets parameters |
| Inference | Model | Running a trained model to generate output |
| Token | Model | Atomic unit of model input/output (~words) |
| Next-token prediction | Model | What the model actually does, one token at a time |
| Non-determinism | Model | Same input → different output |
| Model provider | Model | Service that serves the model (Anthropic, OpenAI, Ollama) |
| Harness | Model | Everything around the model (tools, prompt, permissions) |
| Model provider request | Model | One round-trip: harness→provider→response |
| Input tokens | Model | Tokens sent to the model; billed lower |
| Output tokens | Model | Tokens generated by the model; billed higher |
| Prefix cache | Model | Provider-side cache for shared request prefixes |
| Cache tokens | Model | Input tokens billed at reduced rate via prefix cache |
| Stateless | Sessions | No information carried forward |
| Context | Sessions | Relevant information the agent has access to |
| Context window | Sessions | Everything the model sees on each request |
| Stateful | Sessions | Information carried forward across turns/sessions |
| Agent | Sessions | Model + harness + tools + turns |
| System prompt | Sessions | Standing instructions prepended to every request |
| Session | Sessions | One bounded run of interaction |
| Turn | Sessions | One user message + agent response up to yield |
| Environment | Tools | World the agent acts on (filesystem, DB, API) |
| Filesystem | Tools | Default coding agent environment |
| Tool | Tools | Function the harness exposes for the agent |
| Tool call | Tools | Model output naming a tool and arguments |
| Tool result | Tools | Harness response after executing a tool call |
| MCP | Tools | Protocol for plugging external tool servers |
| Permission request | Tools | User prompt before risky tool execution |
| Permission mode | Tools | Which tool calls trigger permission requests |
| Agent mode | Tools | Preset: permission mode + behavioral instructions |
| Sandbox | Tools | Isolated environment to limit blast radius |
| Sycophancy | Failure | Confidently agreeable output; caving under pushback |
| Hallucination | Failure | Confidently-wrong output (factuality or faithfulness) |
| Parametric knowledge | Failure | What the model "knows" from training |
| Knowledge cutoff | Failure | Date past which model has no parametric knowledge |
| Contextual knowledge | Failure | Facts the agent can read from current context |
| Attention relationship | Failure | Token-to-token influence pairing |
| Attention budget | Failure | Finite influence per token across context |
| Attention degradation | Failure | Signal dilution as session grows |
| Smart zone | Failure | Early session sharpness; degrades past ~100K tokens |
| Clearing | Handoffs | Ending current session, starting fresh |
| Handoff | Handoffs | Transferring context between sessions, no return |
| Handoff artifact | Handoffs | Document carrying context between sessions |
| Spec | Handoffs | Multi-session work description |
| Ticket | Handoffs | Single-session work scope |
| Compaction | Handoffs | In-memory summarised handoff |
| Autocompact | Handoffs | Compaction triggered by harness at window-full |
| Memory system | Memory | Cross-session state persistence |
| AGENTS.md | Memory | Project standing brief loaded at session start |
| Progressive disclosure | Memory | Loading only what's needed now; pointers to rest |
| Context pointer | Memory | Link to pull content into context on demand |
| Skill | Memory | Teachable capability bundled as a unit |
| Subagent | Memory | Agent spawned by another, with own context window |
| Human-in-the-loop | Work | Human actively pairs with agent during session |
| AFK | Work | Agent runs unattended (Away From Keyboard) |
| Automated check | Work | Deterministic verification (tests, lints, typecheck) |
| Automated review | Work | Agent reviews another agent's work |
| Human review | Work | Human reads the code/diff agent produced |
| Vibe coding | Work | Accepting agent output without human review |
| Design concept | Work | Shared understanding between user and agent |
| Grilling | Work | Socratic interview to develop design concept |
