---
name: mermaid-authoring
description: MUST USE for ANY Mermaid diagram — flowcharts, architecture, sequences, class, state, ER, Gantt, pie, gitgraph. Covers syntax rules validated against official mermaid-js repo parser tests, GitHub rendering limitations, subgraph/styling gotchas, and exact syntax that breaks. Activates on: mermaid, flowchart, architecture diagram, graph TD/LR/TB, sequenceDiagram, classDiagram, stateDiagram, gantt, pie, gitGraph, subgraph, style directive, classDef, linkStyle.
version: 1.0.0
metadata:
  invocation_posture: reference
---

# Mermaid Authoring — Definite Syntax Rules

> Built from the official mermaid-js repository, parser test files, and GitHub rendering analysis. Every rule below is traceable to a test fixture, parser spec, or source file. Clone the upstream repo for reference: `git clone https://github.com/mermaid-js/mermaid.git`
>
## CRITICAL FIRST

Before writing ANY Mermaid diagram, read the rules below. If you encounter a situation not covered here, clone the upstream mermaid-js repo and study the relevant source files. Key reference files:

- `packages/mermaid/src/docs/syntax/flowchart.md` — Canonical flowchart syntax
- `packages/mermaid/src/diagrams/flowchart/parser/flow-text.spec.js` — What breaks
- `packages/mermaid/src/diagrams/flowchart/parser/flow-style.spec.js` — Style syntax
- `packages/mermaid/src/diagrams/flowchart/parser/subgraph.spec.js` — Subgraph rules

## 1. CRITICAL BREAKERS — Never Do These

### `end` in lowercase BREAKS flowcharts

```
A[This node has the word end] → BREAKS
A[This node has the word End] → OK
A[End of pipeline] → OK
```

The word `end` (all lowercase) is a reserved keyword for closing subgraphs. Never use it in node text or node IDs. Capitalize at least one letter: `End`, `END`, `eNd`.

### `o` or `x` after edge dashes creates circle/cross edges

```
A---oB → circle edge to "B", NOT node "oB"
A---xB → cross edge to "B", NOT node "xB"
```

Add a space: `A--- oB`, or capitalize: `A---OB`.

### Nested brackets without quotes BREAK

```
A[something (with parens)] → BREAKS
A["something (with parens)"] → OK
A{"decision (yes/no)"} → BREAKS
```

Any node text containing `()`, `[]`, `{}`, `<>` that matches a shape delimiter must be quoted.

### Quotes inside quotes BREAK

```
A["text with "embedded" quote"] → BREAKS
A["text with #quot;embedded#quot; quote"] → OK (use entity codes)
A["`text with "quotes" embedded`"] → OK (markdown string)
```

Escaping with backslash (`\"`) does NOT work. Use HTML entity codes (`#quot;`) or markdown string syntax with backticks.

## 2. Subgraph Syntax — Exactly These Forms

Subgraph IDs are case-sensitive for linking. These are the only valid forms:

```
subgraph Title                   ← Single-word: title IS the id
subgraph "Multi Word Title"      ← Multi-word: quoted title, auto-generated id
subgraph id [Title]              ← Explicit id + bracketed title
subgraph id ["Quoted Title"]     ← Explicit id + quoted title in brackets
```

### Key rules

- **Do NOT use `subgraph ID["Label"]`** — the bracket-then-quote format is nonstandard. Use `subgraph ID [Label]`.
- **Multi-word titles without quotes**: parser accepts them but behavior is documented as broken. Always quote.
- **IDs can start with numbers**: `subgraph 1group [Label]` works.
- **Dashes in titles**: `subgraph a-b-c` works. Title becomes `a-b-c`.
- **Direction inside subgraph**: `direction TB` inside the subgraph body sets internal layout.
- **Collapsible subgraphs** (Mermaid v11+): `one@{ view: collapsed }`. Internal nodes hidden, edges redirect to boundary.
- **Subgraph direction limitation**: If ANY node inside a subgraph connects to something outside, the subgraph inherits parent direction and `direction` is ignored.

### Edges to/from subgraphs

```
subgraph one [Group One]
    a1 --> a2
end
subgraph two [Group Two]
    b1
end

one --> two              ← Edge from subgraph to subgraph (uses subgraph ID)
two --> b2               ← Edge from subgraph to node inside it
c1 --> one               ← Edge from outside to subgraph
```

## 3. Node Shapes — Reference

### Legacy syntax (works everywhere, safe for GitHub)

| Syntax | Shape | Notes |
|--------|-------|-------|
| `id` | Rectangle | Default |
| `id[text]` | Rectangle with text | |
| `id(text)` | Rounded rect | |
| `id([text])` | Stadium | |
| `id[[text]]` | Subroutine | |
| `id[(text)]` | Cylinder | Use for databases |
| `id((text))` | Circle | |
| `id>text]` | Flag/odd | |
| `id{text}` | Diamond | Use for decisions |
| `id{{text}}` | Hexagon | |
| `id[/text/]` | Parallelogram | |
| `id[\text\]` | Parallelogram alt | |
| `id[/text\]` | Trapezoid | |
| `id[\text/]` | Trapezoid alt | |
| `id(((text)))` | Double circle | |

### Expanded shapes (Mermaid v11.3+, probably NOT on GitHub)

Use only if targeting mermaid.live or a known v11+ renderer. Syntax: `A@{ shape: rect, label: "Text" }`. Available shapes include `rect`, `rounded`, `stadium`, `subproc`, `cyl`, `circle`, `diamond`, `hex`, `lean-r`, `lean-l`, and 30+ more.

## 4. Edge Types

| Syntax | Description | GitHub safe? |
|--------|-------------|:---:|
| `A --> B` | Arrow | ✅ |
| `A --- B` | Open link | ✅ |
| `A -- text --> B` | Arrow with label | ✅ |
| `A -->|text| B` | Arrow with label (alt) | ✅ |
| `A -.-> B` | Dotted arrow | ✅ |
| `A -. text .-> B` | Dotted with label | ✅ |
| `A ==> B` | Thick arrow | ✅ |
| `A == text ==> B` | Thick with label | ✅ |
| `A --o B` | Circle end | ✅ |
| `A --x B` | Cross end | ✅ |
| `A <--> B` | Double arrow | ✅ |
| `A ~~~ B` | Invisible (layout-only) | ✅ |

### Chaining

```
A & B --> C & D     ← A→C, A→D, B→C, B→D
A --> B --> C       ← Chain
```

### Edge length (1-3 dashes)

```
A --- B   A --> B
A ---- B  A ---> B
A ----- B A ----> B
```

## 5. Style Directives — Precise Syntax

### `style` — per-node/per-subgraph styling

```
style nodeId fill:#f9f,stroke:#333,stroke-width:4px,color:#fff
style subgraphId fill:#f99,stroke-width:2px,stroke:#f0f
```

- `fill`: background color
- `stroke`: border color
- `stroke-width`: border thickness
- `color`: text color
- Semicolons optional but recommended
- `style` works on subgraph IDs

### `classDef` — reusable class definitions

```
classDef className fill:#f9f,stroke:#333,stroke-width:4px
classDef firstClass,secondClass font-size:12pt
classDef redBg fill:#622
classDef whiteTxt color:white
```

- **Commas in values must be escaped**: `stroke-dasharray: 9\,5`
- **Spaces in values OK**: `stroke-dasharray: 5 5`
- **Percent in values OK**: `font-size:50%`
- **Dots in values OK**: `border:1.5px solid red`
- **`classDef default`** applies to all unclassed nodes

### `class` — apply class to nodes/subgraphs

```
class nodeId1 className
class nodeId1,nodeId2 className
class subgraphId className        ← applies to subgraph
```

### Inline class via `:::`

```
A:::someclass --> B
A[text]:::exClass --> B[text2]
```

### `linkStyle` — per-edge styling

```
linkStyle 0 stroke:#ff3,stroke-width:4px,color:red
linkStyle 1,2,7 color:blue
linkStyle default stroke-width:1px
```

- **0-based indexing** by edge definition order
- `~~~` (invisible edges) count toward the index
- Out-of-bounds index throws parse error

## 6. Labels: What Works and What Breaks

### Plain text (safe, always works)

```
A[This is a label]
A -->|edge label| B
```

### With special characters (must quote)

```
A["label with (parens) and [brackets]"]
A -->|"edge with / slash and ` backtick"| B
```

### HTML entities

```
A["Contains a #quot; double quote"]
A["Contains a #9829; heart symbol"]
```

### Markdown strings (requires htmlLabels: false)

```
A["`This **bold** and *italic* text`"]
A["`Line1\nLine2\nLine3`"]       ← newlines preserved, no <br> needed
```

Add to diagram frontmatter:
```
---
config:
  htmlLabels: false
---
```

### What NEVER works

- Backslash escaping: `A["escaped \"quote\""]` does NOT work
- Mixed quoted/unquoted: `A(this has "string" in it)` breaks
- Capitalization: node IDs are case-sensitive. `A` ≠ `a`.

## 7. GitHub Rendering — What GitHub Strips

GitHub wraps every diagram in a sandboxed `<iframe>`. Mermaid.js renders inside. The iframe blocks JavaScript execution and cross-frame DOM access.

### Broken on GitHub

- `click` directives with JavaScript callbacks — JS blocked
- `click A href "..."` — links work unreliably in nested iframes
- Tooltips — require DOM access that the iframe doesn't have
- `htmlLabels: true` with complex HTML — DOMPurify strips most tags
- `layout: elk` — ELK is a separate package GitHub likely doesn't bundle
- `securityLevel: loose` — GitHub enforces security, directives ignored
- `font-awesome` icons — GitHub doesn't load external CSS

### Works on GitHub

- All node shapes
- All edge types
- Subgraphs (not collapsible)
- `style`, `classDef`, `class`, `linkStyle` with hex colors
- `theme`, `themeVariables` (hex colors only)
- `flowchart`, `sequenceDiagram`, `classDiagram`, `stateDiagram`, `gantt`, `pie`, `gitGraph`

### For GitHub-safe diagrams

1. Use ````mermaid` fenced code blocks, not `graph` or `flowchart`
2. Use `neutral` theme or `base` with explicit `themeVariables`
3. Use hex colors only in `themeVariables` (never color names)
4. Never use `click`, JavaScript callbacks, or tooltips
5. Use `htmlLabels: false` with markdown strings for formatting
6. Stick to `dagre` layout (default)

## 8. Frontmatter Config

```
---
config:
  theme: neutral
  htmlLabels: false
  darkMode: true
  themeVariables:
    primaryColor: "#1a1a2e"
    lineColor: "#e0e0e0"
---
flowchart TB
    ...
```

- `darkMode: true` affects how derived colors calculate
- `theme: base` required for `themeVariables` to take effect
- `theme: neutral` is safest for GitHub (works on light and dark backgrounds)

## 9. Comments

```
%% Single-line comment — must be on its own line
flowchart LR
    A --> B
    %% This is fine
    C --> D
```

- Comments must be on their own line
- Do NOT use `%%{ }%%` curly brace syntax in comments — confuses directive parser
- Node/external comments: `A --> B %% inline comment` — does NOT work

## 10. Quick Reference: Sin List

| Don't | Because | Do Instead |
|-------|---------|------------|
| `A[end]` | `end` is reserved keyword | `A[End]` or `A["end"]` |
| `A---oB` | Creates circle edge | `A--- oB` |
| `A[text (parens)]` | Nested brackets break | `A["text (parens)"]` |
| `A["text \"quote\""]` | Backslash escape doesn't work | `A["text #quot;quote#quot;"]` |
| `style id fill:red` | Color names don't work | `style id fill:#ff0000` |
| `linkStyle 1 stroke:red` | 1-based index off | `linkStyle 0 stroke:#ff0000` (0-based) |
| `classDef my fill:#fff` | Class definitions use `classDef` | `classDef my fill:#fff` (correct) |
| `%%{ ... }%%` in comment | Confuses directive parser | `%% plain comment` |
| `click A callback()` | JS blocked on GitHub | Omit entirely |
| `layout: elk` for GitHub | Not bundled | Use `dagre` (default) |

## 11. When Unsure — Read the Source

When you encounter a Mermaid syntax question not covered here, clone the upstream mermaid-js repo and consult these key files:

1. `packages/mermaid/src/docs/syntax/flowchart.md` — canonical reference
2. `packages/mermaid/src/diagrams/flowchart/parser/flow-text.spec.js` — edge cases
3. `packages/mermaid/src/diagrams/flowchart/parser/flow-style.spec.js` — style syntax
4. `packages/mermaid/src/diagrams/flowchart/parser/subgraph.spec.js` — subgraph rules
5. `packages/mermaid/src/docs/config/theming.md` — theme variables

Also test on [mermaid.live](https://mermaid.live/) before committing to GitHub markdown.

