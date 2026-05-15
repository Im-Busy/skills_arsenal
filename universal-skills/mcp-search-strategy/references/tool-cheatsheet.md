# MCP Search Tool Quick Reference

## Tool at a Glance

| Tool | Best For | Key Parameter | Fallback |
|------|----------|--------------|----------|
| `memory` | Prior session recall | `search_nodes(query)` | Web search |
| `context7` | Library docs | `resolve-library-id` + `query-docs` | Exa |
| `repomix` | Codebase overview | `repomix` or `npx repomix --remote user/repo` | GitHub MCP |
| `exa` (code) | Code examples | `get_code_context_exa(query)` | Exa web + crawl |
| `exa` (web) | Semantic web search | `web_search_exa(query)` | Tavily |
| `firecrawl` | URL scraping/crawling | `scrape(url)`, `crawl(url)` | Tavily extract |
| `tavily` | Deep research, news | `tavily-search(query, search_depth="advanced")` | SearXNG |
| `searxng` | Quick facts, privacy | `searxng_web_search(query)` | — |
| `github` | Repo/issue content | GitHub MCP tools | Exa web |

---

## Repomix — Codebase Packing

## Storage Convention

All Repomix outputs are stored in the project's `useful_resources/managed_by_AI/` directory.

**Naming:** `repomix-output-<source>.<ext>`

```bash
# Remote repository → project storage
npx repomix --remote user/repo -o useful_resources/managed_by_AI/repomix-output-user-repo.xml

# Local directory → project storage
repomix path/to/directory -o useful_resources/managed_by_AI/repomix-output.xml

# Markdown format
repomix --style markdown -o useful_resources/managed_by_AI/repomix-output-user-repo.md

# With config file
repomix --init             # creates repomix.config.json
```

---

## Firecrawl — Web Scraping

### Scrape a single URL

```
scrape(
    url="https://example.com/docs/page",
    formats=["markdown"],
    onlyMainContent=true
)
```

### Crawl a website

```
crawl(
    url="https://docs.example.com",
    maxDepth=2,
    maxPages=20,
    includePaths=["/docs/.*"],
    excludePaths=["/blog/.*"]
)
```

### Search the web

```
search(
    query="your search query",
    limit=5,
    country="us"
)
```

### Map a website structure

```
map(
    url="https://example.com",
    search="docs"  # optional filter
)
```

### Extract structured data

```
extract(
    urls=["https://example.com/page1", "https://example.com/page2"],
    prompt="Extract product name, price, and rating from each page"
)
```

---

## Exa — Code Search

```
get_code_context_exa(
    query="descriptive query, not keywords",
    numResults=8
)
```

Good queries:
- "Python requests library POST with JSON body"
- "React useState hook examples with cleanup"
- "Express.js middleware error handling pattern"

Bad queries:
- "python http" (too vague)
- "react state" (not specific enough)

---

## Exa — Web Search

```
web_search_exa(
    query="blog post describing the topic in detail",
    type="auto",
    freshness="month"  # only when recency matters
)
```

Follow up with crawling if highlights are insufficient:
```
crawling_exa(
    urls=["https://best-result-url.com"],
    maxCharacters=5000
)
```

---

## Tavily — Deep Research

```
tavily-search(
    query="comprehensive research query",
    search_depth="advanced",  # or "basic" for quick
    topic="general",          # or "news"
    max_results=10,
    time_range="month",       # optional
    include_domains=["docs.example.com"],  # optional filter
    exclude_domains=["spam.com"]           # optional filter
)
```

### Tavily — URL Extraction

```
tavily-extract(
    urls=["https://url1.com", "https://url2.com"],
    extract_depth="advanced",
    format="markdown"
)
```

---

## SearXNG — Quick Search

```
searxng_web_search(
    query="simple factual query",
    language="all",
    safesearch=0,
    pageno=1
)
```

Read specific URL content:
```
web_url_read(
    url="https://example.com/article",
    maxLength=3000,
    paragraphRange="1-10"
)
```

---

## Context7 — Library Docs

Step 1: Resolve library
```
resolve-library-id(
    query="how to set up JWT authentication",
    libraryName="Express.js"
)
```

Step 2: Query docs (use returned libraryId)
```
query-docs(
    libraryId="/expressjs/express",
    query="JWT authentication middleware setup"
)
```

---

## Decision Flowchart (Text)

```
Query
  │
  ├─ Prior context needed? → memory
  │
  ├─ Known library/package? → context7 → (fail) → exa code
  │
  ├─ Understand codebase? → repomix
  │
  ├─ GitHub content? → github
  │
  ├─ Code examples needed? → exa (get_code_context_exa)
  │
  ├─ Scrape specific URL(s)? → firecrawl
  │
  ├─ Simple fact? → searxng
  │
  ├─ News/recent events? → tavily (topic="news")
  │
  └─ Deep research? → tavily (search_depth="advanced")
```
