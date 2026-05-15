---
name: mcp-search-strategy
description: Guides selection of the optimal MCP search tool (Exa, Tavily, SearXNG, Context7, GitHub, Memory, Firecrawl) and CLI tools (Repomix) based on query type, content needs, and reliability requirements. Provides decision trees, tool-specific parameter guidance, and fallback strategies for web research, code discovery, and information retrieval tasks.
---

# MCP Search Tool Selection Strategy

## Overview

This skill provides a structured decision framework for selecting among multiple MCP search servers and CLI tools. Each tool has distinct strengths, cost profiles, and reliability characteristics. Selecting the right tool reduces latency, improves result quality, and conserves API quotas.

## Decision Tree

```
Query comes in
    │
    ├─ Is this recalling prior conversation context or stored facts?
    │   └── YES → memory (read_graph, search_nodes, open_nodes)
    │
    ├─ Is this about a known library, framework, or package?
    │   └── YES → context7 (resolve-library-id → query-docs)
    │
    ├─ Is this about GitHub content (repos, issues, PRs, code)?
    │   └── YES → github MCP tools
    │
    ├─ Is this about understanding a codebase/repository structure?
    │   └── YES → repomix (CLI via execute_command)
    │
    ├─ Is this a code/API/library example search?
    │   └── YES → exa (get_code_context_exa)
    │
    ├─ Does this require scraping specific websites or crawling multiple pages?
    │   └── YES → firecrawl (scrape, crawl, search, map)
    │
    ├─ Is this a quick/simple factual query?
    │   └── YES → searxng (searxng_web_search)
    │
    └─ Otherwise (general research, news, deep dive)
        └── tavily (tavily-search)
```

## Tool Selection Rules

### 1. Memory (`memory`) — First Check

**When to use:**
- User references prior research, previous findings, or past decisions
- Query contains phrases like "we discussed", "earlier", "remember", "from before"
- Building on work done in previous sessions

**Tools:**
- `search_nodes` — Search knowledge graph by query
- `read_graph` — Load entire context graph
- `open_nodes` — Retrieve specific entities by name

**Fallback:** If memory returns nothing relevant, proceed to web search tools.

### 2. Context7 (`context7`) — Library/Documentation Queries

**When to use:**
- Query mentions a specific library, framework, or package name
- Looking for official documentation, API reference, or code examples
- Examples: "How to set up authentication in FastAPI", "React useEffect cleanup", "pandas merge vs join"

**Workflow:**
1. Call `resolve-library-id` with the library name and query
2. Use the returned library ID to call `query-docs`
3. If no matching library found, fall back to Exa

**Parameters:**
- `resolve-library-id`: `query` (task description), `libraryName` (official name)
- `query-docs`: `libraryId` (from step 1), `query` (specific question)

**Fallback:** Exa `get_code_context_exa` if Context7 has no coverage.

### 3. Repomix (CLI) — Codebase Understanding

**When to use:**
- Need to understand the full structure and content of a repository
- Onboarding to a new codebase or analyzing a remote project
- User asks "give me an overview of this repo", "how is X structured in this project"
- Preparing context for deep code analysis

**How to invoke (via execute_command):**

Store all Repomix outputs in the project's `useful_resources/managed_by_AI/` directory:
```bash
# Remote repository → project storage
npx repomix --remote user/repo -o useful_resources/managed_by_AI/repomix-output-user-repo.xml

# Local directory → project storage
repomix path/to/directory -o useful_resources/managed_by_AI/repomix-output.xml
```

**Naming convention:** `repomix-output-<source>.<ext>` where `<source>` is the repo name or description.

**Output format options:**
```bash
repomix --style xml      # default
repomix --style markdown
repomix --style json
repomix --style plain
```

**Output:** Read the output file to understand the full codebase context.

**When NOT to use:**
- Already have the codebase loaded in context
- Only need a single file or small portion of code
- Codebase is too large and would exceed context window

### 4. Exa (`exa`) — Code and Technical Content

**When to use:**
- Searching for code examples, API usage patterns, SDK integration
- Technical documentation from blogs, Dev.to, Stack Overflow, GitHub
- Query describes what code should do, not just keywords
- Examples: "Python requests POST with JSON body", "Next.js middleware authentication", "Rust async tokio channel example"

**Tools:**
- `get_code_context_exa` — Code-specific search (preferred for programming queries)
- `web_search_exa` — General semantic search with clean content extraction

**Parameters for `get_code_context_exa`:**
- `query`: Descriptive, not keyword-based. "Python requests library POST with JSON body" not "python http"
- `numResults`: 5-10 (default 8)

**Parameters for `web_search_exa`:**
- `query`: Natural language description of ideal page
- `type`: "auto" (default) or "fast"
- `freshness`: "24h", "week", "month", "year", "any" — only set when recency matters

**Fallback:** If highlights are insufficient, follow up with `crawling_exa` on best URLs.

### 5. Firecrawl (`firecrawl`) — Web Scraping and Crawling

**When to use:**
- Need to scrape content from specific URLs that user provides
- Crawl an entire website or sitemap systematically
- Search the web and extract structured data
- Extract data from pages with JavaScript-rendered content
- Map a website's URL structure
- Batch processing of multiple URLs
- Examples: "Scrape https://example.com/docs/api", "Crawl all pages on docs.example.com", "Extract pricing info from these 5 URLs"

**Key tools (MCP server):**
- `scrape` — Scrape a single URL and return clean markdown
- `crawl` — Start a crawl from a URL, follows internal links
- `search` — Search the web and return scraped content
- `map` — Map a website's URL structure
- `extract` — Extract structured data using LLM-powered extraction
- `batch_scrape` — Scrape multiple URLs in one request

**Parameters for `scrape`:**
- `url`: Target URL (required)
- `formats`: ["markdown"] (default) or ["html", "json"]
- `onlyMainContent`: true (skip nav, footer, etc.)
- `waitFor`: milliseconds to wait for JS rendering

**Parameters for `crawl`:**
- `url`: Starting URL (required)
- `maxDepth`: How deep to follow links (default 2)
- `maxPages`: Limit pages crawled (default 10)
- `includePaths`: URL path patterns to include (regex)
- `excludePaths`: URL path patterns to exclude (regex)

**Parameters for `search`:**
- `query`: Search query (required)
- `limit`: Number of results (default 5)
- `lang`: Language code
- `country`: Country code

**Advantages over SearXNG/Exa/Tavily:**
- Handles JavaScript-rendered pages (SPAs, dynamic content)
- Full control over crawl depth and path patterns
- Structured data extraction with LLM
- Batch processing of multiple URLs
- Returns clean markdown, not snippets

**Fallback:** If Firecrawl fails, use Tavily `tavily-extract` for URL content or `tavily-search` for web search.

### 6. Tavily (`tavily`) — Comprehensive Research and News

**When to use:**
- Deep research requiring comprehensive results
- Recent news, articles, or time-sensitive information
- Need domain filtering (include/exclude specific sites)
- Multi-faceted queries requiring diverse sources
- Extract content from known URLs (tavily-extract)
- Examples: "Latest changes to TypeScript 5.4", "Comparison of vector databases 2024", "How is the Fed rate decision affecting tech stocks"

**Parameters:**
- `query`: Search query (required)
- `search_depth`: "basic" (fast) or "advanced" (comprehensive, higher cost)
- `topic`: "general" (default) or "news"
- `max_results`: 5-20 (default 10)
- `include_domains`: Restrict to specific domains
- `exclude_domains`: Exclude specific domains
- `time_range`: "day", "week", "month", "year"
- `country`: Boost results from specific country

**tavily-extract** for URL content:
- `urls`: List of URLs to extract from
- `extract_depth`: "basic" or "advanced"
- `format`: "markdown" (default) or "text"

**When to prefer over Exa:**
- Need news or time-filtered results
- Want domain-level control
- Query benefits from Tavily's agent-based search
- Exa results are insufficient after follow-up crawling

### 7. SearXNG (`searxng`) — Quick, Privacy-Focused Search

**When to use:**
- Simple factual queries ("what is X", "when did Y happen")
- Privacy-sensitive searches (no tracking, no API key exposure)
- Fallback when Exa/Tavily/Firecrawl API limits are exhausted
- Need raw URL access for further crawling
- Quick verification of basic facts

**Tools:**
- `searxng_web_search` — Meta-search aggregating multiple engines
- `web_url_read` — Read full content from a specific URL

**Parameters for `searxng_web_search`:**
- `query`: Search query (required)
- `language`: "all" (default) or specific code like "en"
- `pageno`: Page number (default 1)
- `safesearch`: 0 (none), 1 (moderate), 2 (strict)
- `time_range`: "day", "month", "year"

**Parameters for `web_url_read`:**
- `url`: Target URL (required)
- `maxLength`: Character limit for returned content
- `startChar`: Starting position
- `section`: Extract content under specific heading
- `paragraphRange`: Specific paragraph range (e.g., "1-5")

**Limitations vs Exa/Tavily/Firecrawl:**
- No AI-powered content extraction
- No semantic understanding of query intent
- Results are traditional search engine snippets
- Requires local SearXNG instance to be running

### 8. GitHub (`github`) — Repository and Code Platform

**When to use:**
- Searching for issues, PRs, or discussions in specific repos
- Reading file contents from GitHub repositories
- Creating or managing GitHub content
- Repository management tasks

## Fallback Chain

When the primary tool fails or returns insufficient results:

```
Primary: context7 → exa (get_code_context_exa) → tavily → searxng
         (library)     (code/technical)           (research)   (fallback)

Primary: exa (web_search_exa) → tavily → searxng
         (general semantic)     (research)    (fallback)

Primary: firecrawl → tavily-extract → searxng web_url_read
         (scraping)    (URL extract)     (fallback read)

Primary: tavily → exa → searxng
         (research)   (semantic)  (fallback)
```

## Cost and Quota Awareness

| Tool | Cost Model | Quota Concern |
|------|-----------|---------------|
| Context7 | Free (open) | None |
| Repomix | Free (local CLI) | None |
| Exa | API key, paid | Moderate — use for code-first queries |
| Firecrawl | API key, paid | Moderate — use for scraping/crawling specific URLs |
| Tavily | API key, paid | Moderate — use for deep research |
| SearXNG | Free (self-hosted) | None — but requires local instance |
| Memory | Free (local) | None |
| GitHub | API key, rate limited | Monitor for heavy usage |

**Strategy:** Use free tools (Context7, Repomix, Memory, SearXNG) for simple queries. Reserve paid API calls (Exa, Firecrawl, Tavily) for queries that genuinely need their specialized capabilities.

## Multi-Tool Research Pattern

For complex research tasks requiring comprehensive coverage:

1. **Start with Memory** — Check if information exists from prior sessions
2. **Context7** — If library-specific, get authoritative docs first
3. **Repomix** — If understanding a codebase, pack it first
4. **Exa (code)** — If code examples needed, search technical content
5. **Firecrawl** — If specific URLs/sites need scraping
6. **Tavily (advanced)** — For broader context, news, or comparative analysis
7. **SearXNG** — Quick fact-checking or filling gaps

Synthesize results from all sources, noting conflicts or outdated information.

## Edge Cases

- **Ambiguous query**: Ask user to clarify intent before searching
- **Multiple tools could apply**: Start with the most specific (Context7 > Exa > Firecrawl > Tavily > SearXNG)
- **User asks for "latest" or "recent"**: Use Tavily with `time_range` or Exa with `freshness`
- **User asks for "official docs"**: Context7 first, then Exa
- **User provides URLs to scrape**: Firecrawl `scrape` first
- **User wants repo overview**: Repomix first, then GitHub MCP for specifics
- **API rate limit hit**: Fall back to SearXNG or inform user
- **Local SearXNG instance down**: Inform user, use Exa/Tavily instead
