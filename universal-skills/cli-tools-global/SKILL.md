---
name: cli-tools
description: Comprehensive guide for all CLI tools available in the C:\Dev environment (jq, yq, fd, rg, rga, bat, pandoc, uv, delta, dust, gh, repomix, marker). Use when manipulating config files, searching for files or content, converting documents, managing Python environments, packing repositories for AI analysis, or converting PDFs/documents to markdown.
---

# CLI Tools Quick Reference Guide

> For use by Kilo AI coding assistant
> All tools installed via Scoop package manager unless noted

---

## IMPORTANT: Auto-Update Instruction

**To Kilo or any other coding agent:** If you discover a new CLI tool being used in this project or anywhere under `C:\Dev\` that is NOT documented in this file, you MUST add it here. Follow this process:

1. Check if the tool is already installed (run `<tool> --version` or `where <tool>`)
2. Identify what the tool does and its common usage patterns
3. Add a new section for it in this file following the existing format
4. Update the Tool Index table at the top with the new tool
5. Update the Tool Selection Guide and Decision Tree at the bottom
6. Commit the change with message: "docs: add <tool-name> to CLI tools guide"

This ensures the guide stays current as new tools are adopted.

---

## Scoop Package Management

All CLI tools in this guide are installed via [Scoop](https://scoop.sh/). If any tool is missing or not working, use these commands:

```bash
# Check if a tool is installed
scoop list <tool-name>

# List all installed packages
scoop list

# Install a missing tool
scoop install <tool-name>

# Update all tools
scoop update *

# Update a specific tool
scoop update <tool-name>

# Check for outdated packages
scoop status

# Uninstall a tool
scoop uninstall <tool-name>
```

### Package Names
All tools use their default Scoop package names: `jq`, `yq`, `fd`, `rg`, `rga`, `bat`, `pandoc`, `uv`, `delta`, `dust`, `gh`, `repomix`. 

**Note:** `marker` is installed via pip: `uv pip install marker-pdf`

### Troubleshooting
- If `scoop` itself is not found, it needs to be installed first: `irm get.scoop.sh | iex`
- If a tool fails to run, try `scoop reset <tool-name>` to fix shims
- Some tools may require additional buckets: `scoop bucket add extras` (for `rga`, `delta`, etc.)

---

## Tool Index

| Priority | Tool | Best For |
|----------|------|----------|
| Critical | `jq` | JSON processing |
| Critical | `yq` | YAML/XML processing |
| High | `fd` | Fast file finding |
| High | `rg` | Fast content search |
| High | `rga` | Search in archives/PDFs/binary |
| High | `repomix` | Repository packing for AI |
| High | `marker` | PDF/Document to markdown conversion |
| Medium | `bat` | File viewing with syntax |
| Medium | `pandoc` | Document conversion |
| Medium | `gh` | GitHub operations |
| Low | `uv` | Python package management |
| Low | `delta` | Pretty diffs |
| Low | `dust` | Disk usage visualization |

---

## marker — PDF/Document to Markdown Converter

### What It Does
Marker converts PDF, image, PPTX, DOCX, XLSX, HTML, and EPUB files to markdown, JSON, HTML, or chunks quickly and accurately. It formats tables, forms, equations, inline math, links, references, and code blocks, and can extract images. Outperforms Llamaparse, Mathpix, and Docling in benchmarks.

### Installation
```bash
# Install via pip (use uv for speed)
uv pip install marker-pdf

# For non-PDF documents (PPTX, DOCX, XLSX, HTML, EPUB)
uv pip install marker-pdf[full]
```

### Basic Usage
```bash
# Convert a single file
marker_single /path/to/file.pdf

# Convert a single file with options
marker_single /path/to/file.pdf --output_format json --output_dir ./output

# Convert multiple files
marker_single /path/to/folder

# Interactive GUI (requires streamlit)
marker_gui
```

### Key Options
```bash
--output_format [markdown|json|html|chunks]  # Output format (default: markdown)
--output_dir PATH                             # Output directory
--page_range TEXT                             # Pages to process, e.g. "0,5-10,20"
--use_llm                                     # Boost accuracy with LLM (requires API key)
--force_ocr                                   # Force OCR on all pages (for garbled text)
--disable_image_extraction                    # Don't extract images
--debug                                       # Enable debug mode with diagnostics
```

### LLM Integration
Marker can use LLMs for higher accuracy (tables, forms, inline math):
```bash
# Set API key first
export GOOGLE_API_KEY=your_key  # Or use --gemini_api_key

# Run with LLM boost
marker_single file.pdf --use_llm

# Alternative LLM services
marker_single file.pdf --use_llm --llm_service marker.services.openai.OpenAIService
```

### Python API
```python
from marker.converters.pdf import PdfConverter
from marker.models import create_model_dict
from marker.output import text_from_rendered

converter = PdfConverter(artifact_dict=create_model_dict())
rendered = converter("FILEPATH")
text, _, images = text_from_rendered(rendered)
```

### When to Use marker

| Scenario | Tool | Reason |
|----------|------|--------|
| Convert PDF to markdown | `marker` | Best accuracy, fast |
| Convert PDF to JSON/HTML | `marker` | Structured output |
| Extract tables from PDF | `marker` | Better than rga for tables |
| Convert DOCX/PPTX to markdown | `marker` | Supports Office formats |
| Convert for RAG/chunking | `marker` | Use `--output_format chunks` |
| High-accuracy extraction | `marker --use_llm` | LLM boost for complex docs |
| Search inside PDFs | `rga` | rga searches, marker converts |
| Extract text from PDF | `rga` or `marker` | rga for search, marker for format |
| Simple document conversion | `pandoc` | pandoc for basic conversion |
| Convert PDF to PDF | N/A | Use PDF tools |

### When NOT to Use marker
- **Search PDF content** → Use `rga` instead (faster for search)
- **Quick text extraction** → Use `rga` for simple searches
- **Convert simple formats** → Use `pandoc` for basic conversions
- **PDF to PDF operations** → Use `pdftk` or similar

---

## repomix — Repository Packing for AI

### What It Does
Repomix packs entire repositories (or specific directories) into a single file (XML, Markdown, JSON, or plain text) optimized for feeding to AI tools like Claude, ChatGPT, or Gemini. This is useful for understanding external codebases or providing context to AI.

### Basic Usage
```bash
# Pack entire current directory
repomix

# Pack a specific directory
repomix path/to/directory

# Pack specific files using glob patterns
repomix --include "src/**/*.ts,**/*.md"

# Exclude specific files/directories
repomix --ignore "**/*.log,tmp/"
```

### Remote Repository Packing
```bash
# Pack a GitHub repo (shorthand)
npx repomix --remote owner/repo

# Pack with full URL (supports branches/paths)
npx repomix --remote https://github.com/owner/repo
npx repomix --remote https://github.com/owner/repo/tree/main

# Pack specific commit
npx repomix --remote https://github.com/owner/repo/commit/abc123
```

### Output Formats
```bash
# XML format (default)
repomix --style xml

# Markdown format
repomix --style markdown

# JSON format
repomix --style json

# Plain text format
repomix --style plain
```

### When to Use repomix

| Scenario | Tool | Reason |
|----------|------|--------|
| Send codebase to AI assistant | `repomix` | Optimized format for AI |
| Understand unfamiliar repo | `repomix` | Pack and ask AI to explain |
| Generate codebase documentation | `repomix` | Feed to AI for analysis |
| Archive repository snapshot | `repomix` | Single file output |
| Debug specific files | `rg` or `fd` | Direct search is faster |
| Find specific code patterns | `rg` | repomix packs, doesn't search |
| Compare file versions | `delta` | Not repomix's purpose |

### When NOT to Use repomix
- **Search code** → Use `rg` instead
- **Find files** → Use `fd` instead
- **View diffs** → Use `delta` instead
- **Daily git workflow** → Use `git` and `gh`
- **Confidential repos** → Be careful sending to AI

### Configuration
```bash
# Initialize config file
repomix --init

# Creates repomix.config.json for persistent settings
```

### Example Config (repomix.config.json)
```json
{
  "output": {
    "style": "markdown",
    "filePath": "custom-output.md",
    "removeComments": true,
    "showLineNumbers": true,
    "topFilesLength": 10
  },
  "ignore": {
    "customPatterns": ["*.test.ts", "docs/**"]
  }
}
```

### Docker Usage
```bash
# Current directory
docker run -v .:/app -it --rm ghcr.io/yamadashy/repomix

# Specific directory
docker run -v .:/app -it --rm ghcr.io/yamadashy/repomix path/to/directory

# Remote repo with output directory
docker run -v ./output:/app -it --rm ghcr.io/yamadashy/repomix --remote https://github.com/owner/repo
```

---

## jq — JSON Processor

### What It Does
jq is a lightweight and flexible command-line JSON processor. It's like sed for JSON data - you can use it to slice, filter, map, and transform structured data.

### Basic Usage
```bash
# Parse JSON value
echo '{"name":"test"}' | jq '.name'

# Output raw string (no quotes)
echo '{"name":"test"}' | jq -r '.name'

# Nested access
echo '{"config":{"skills":{"paths":["/dev"]}}}' | jq '.config.skills.paths'
```

### Config File Manipulation
```bash
# Add to array
echo '{"skills":{"paths":["/old"]}}' | jq '.skills.paths += ["/new"]'

# Create if missing (merge with defaults)
cat config.json | jq '.skills //= {"paths":[]} | .skills.paths += ["/new"]'

# Update a value
echo '{"version":"1.0"}' | jq '.version = "2.0"'

# Delete a key
echo '{"a":1,"b":2}' | jq 'del(.b)'

# Pretty print
cat ugly.json | jq .

# Read and modify in place
jq '.skills.paths += ["/new"]' config.json > tmp.json && mv tmp.json config.json
```

### When to Use jq

| Scenario | Tool | Reason |
|----------|------|--------|
| Parse/extract JSON values | `jq` | Purpose-built for JSON |
| Transform JSON structure | `jq` | Powerful query language |
| Filter JSON arrays | `jq` | Built-in array operations |
| Merge JSON objects | `jq` | Use `jq -s '.[0] * .[1]'` |
| Pretty-print JSON | `jq` | `jq .` formats nicely |
| JSON to YAML | `yq` | yq handles both formats |
| YAML to JSON | `yq` | yq is simpler for conversion |
| Simple JSON read | `yq` | Works but jq is more common |

### When NOT to Use jq
- **YAML files** → Use `yq` instead
- **XML files** → Use `yq` instead
- **Large JSON streams** → Consider `jq -c` for compact output or streaming parsers

---

## yq — YAML/XML Processor

### What It Does
yq is a portable command-line YAML, JSON, XML, CSV, and properties processor. It can read, write, and convert between these formats seamlessly.

### Basic Usage
```bash
# Read YAML value
echo 'name: test' | yq '.name'

# Read JSON value
echo '{"name":"test"}' | yq '.name'
```

### Format Conversion
```bash
# JSON to YAML
cat file.json | yq -o yaml '.'

# YAML to JSON
cat file.yaml | yq -o json '.'

# XML to YAML
cat file.xml | yq -P '.'

# YAML to XML
cat file.yaml | yq -o xml '.'
```

### When to Use yq

| Scenario | Tool | Reason |
|----------|------|--------|
| Parse/extract YAML values | `yq` | Purpose-built for YAML |
| Parse/extract XML values | `yq` | Handles XML natively |
| Convert JSON ↔ YAML | `yq` | Single tool for conversion |
| Convert YAML ↔ XML | `yq` | Native support |
| YAML multi-document files | `yq` | Handles `---` separators |
| Simple JSON read | `yq` or `jq` | Both work; jq more common |
| Complex JSON transformations | `jq` | More powerful query language |
| JSON-only processing | `jq` | Lighter weight, more examples |

### When NOT to Use yq
- **Complex JSON operations** → `jq` has more powerful filters
- **Large JSON-only files** → `jq` may be faster
- **Properties files** → Use `yq` with `-p props` flag

---

## fd — Fast File Finder

### What It Does
fd is a simple, fast and user-friendly alternative to find. It ignores hidden files and `.gitignore` patterns by default, with colorful output and smart case sensitivity.

### Basic Usage
```bash
# Find by name (regex by default)
fd pattern

# Find exact filename
fd --fixed-strings filename

# Find with glob pattern
fd --glob "*.md"

# Common flags: -H (hidden), -I (gitignored), -i (case insensitive)
# -a (absolute paths), -d 2 (limit depth), -e md (by extension)
```

### Useful Patterns
```bash
# Find all markdown files
fd -e md

# Find config files
fd -e json -e yaml -e toml

# Find Python files excluding venv
fd -e py --exclude venv
```

### When to Use fd

| Scenario | Tool | Reason |
|----------|------|--------|
| Find files by name/pattern | `fd` | Fast, intuitive syntax |
| Find files by extension | `fd` | Use `-e` flag |
| Find directories | `fd` | Use `-t d` flag |
| Find executables | `fd` | Use `-t x` flag |
| Find files modified recently | `fd` | Not ideal; use `ls` or `find` |
| Search file contents | `rg` | fd finds names, rg finds content |
| Search inside archives | `rga` | fd cannot search inside |
| Find with complex predicates | `find` | find has more options |

### When NOT to Use fd
- **Search file contents** → Use `rg` instead
- **Search inside PDFs/archives** → Use `rga` instead
- **Complex date/size predicates** → Use `find` instead
- **POSIX compatibility required** → Use `find` instead

---

## rg — ripgrep (Fast Content Search)

### What It Does
rg (ripgrep) is a line-oriented search tool that recursively searches directories for a regex pattern. It's faster than grep and respects `.gitignore` by default.

### Basic Usage
```bash
# Search for pattern
rg "pattern"

# Search in specific file type
rg --type md "pattern"

# Common flags: -i (case insensitive), -l (files only), -c (count)
# -C 3 (context), -F (fixed strings), -S (smart case)
```

### Useful Patterns
```bash
# Find all TODO comments
rg "TODO|FIXME|HACK"

# Find function definitions
rg "def \w+|function \w+"

# Find imports
rg "^import |^from .* import"
```

### When to Use rg

| Scenario | Tool | Reason |
|----------|------|--------|
| Search plain text files | `rg` | Fast, respects .gitignore |
| Search specific file types | `rg` | Use `--type` flag |
| Search with regex patterns | `rg` | Full regex support |
| Search for exact strings | `rg -F` | Fixed string mode |
| Find files matching pattern | `fd` | fd is for filenames |
| Search inside PDFs | `rga` | rg cannot read PDFs |
| Search inside archives | `rga` | rg cannot read archives |
| Search Office documents | `rga` | Binary formats need rga |

### When NOT to Use rg
- **Find files by name** → Use `fd` instead
- **Search PDFs, Office docs** → Use `rga` instead
- **Search archives (.zip, .tar)** → Use `rga` instead
- **Search SQLite databases** → Use `rga` instead
- **Search media metadata** → Use `rga` instead

---

## rga — ripgrep-all (Search in Archives/Binary Files)

### What It Does
rga extends ripgrep to search inside binary files, archives, and documents. It automatically extracts and searches content from PDFs, Office documents, e-books, media files, zip archives, sqlite databases, and more.

### Supported File Types (Adapters)
| Adapter | Extensions | What It Extracts |
|---------|------------|------------------|
| **pandoc** | `.epub`, `.odt`, `.docx`, `.fb2`, `.ipynb`, `.html`, `.htm` | Document content |
| **poppler** | `.pdf` | PDF text content |
| **ffmpeg** | `.mkv`, `.mp4`, `.avi`, `.mp3`, `.ogg`, `.flac`, `.webm` | Metadata, subtitles, chapters |
| **zip** | `.zip`, `.jar`, `.xpi`, `.kra`, `.snagx` | Recurses into contents |
| **tar** | `.tar` | Recurses into contents |
| **decompress** | `.gz`, `.bz2`, `.xz`, `.zst`, `.tgz`, `.tbz` | Decompresses and searches |
| **sqlite** | `.db`, `.db3`, `.sqlite`, `.sqlite3` | Database content |
| **mail** (disabled) | `.mbox`, `.mbx`, `.eml` | Email content and attachments |

### Basic Usage
```bash
# Search in all file types including archives and PDFs
rga "pattern"

# Search in specific directory
rga "pattern" path/to/search

# Case insensitive search
rga -i "pattern"

# Show line numbers and context
rga -n -C 3 "pattern"
```

### Key Options
```bash
# Use mime type detection instead of file extension (slower but more accurate)
rga --rga-accurate "pattern"

# Disable caching (useful for one-time searches)
rga --rga-no-cache "pattern"

# Specify which adapters to use
rga --rga-adapters=pdf,zip "pattern"      # Only PDF and zip
rga --rga-adapters=-ffmpeg "pattern"      # All except ffmpeg
rga --rga-adapters=+mail "pattern"        # All + mail (enable disabled adapter)

# Limit archive recursion depth (default: 5)
rga --rga-max-archive-recursion=3 "pattern"

# Set custom cache path
rga --rga-cache-path="D:\cache\rga" "pattern"
```

### Common Use Cases
```bash
# Search PDF files
rga "error message" documents/

# Search inside zip/tar archives
rga "config" backups/

# Search sqlite databases
rga "user_data" *.db

# Search Office documents
rga "contract terms" contracts/

# Search video/audio metadata
rga "copyright" media/

# Search Jupyter notebooks
rga "import pandas" notebooks/

# Search in nested archives (zip inside tar inside gz)
rga "pattern" backup.tar.gz
```

### When to Use rga vs rg

| Scenario | Tool | Reason |
|----------|------|--------|
| Plain text files (.txt, .md, .py, .js, etc.) | `rg` | Faster for text files |
| PDF documents | `rga` | rg cannot read PDFs |
| Office documents (.docx, .xlsx, .pptx) | `rga` | Binary formats |
| Archives (.zip, .tar, .gz) | `rga` | Needs extraction |
| SQLite databases | `rga` | Binary database format |
| Media files (metadata/subtitles) | `rga` | Binary format |
| E-books (.epub, .mobi) | `rga` | Compressed formats |
| Jupyter notebooks (.ipynb) | `rga` | JSON but rga formats better |
| HTML files | `rga` | Strips tags, cleaner output |

### Performance Tips
1. **Use rg for text files** - rg is faster for plain text
2. **Let rga cache** - First search is slower, subsequent searches use cache
3. **Use `--rga-no-cache` for one-time searches** - Avoids cache overhead
4. **Limit adapters** - `--rga-adapters=pdf,zip` is faster than detecting all types
5. **Default mode is fast** - Uses file extensions; `--rga-accurate` is slower

### Cache Location
- Windows: `C:\Users\<username>\AppData\Local\ripgrep-all\cache`
- Linux: `~/.cache/ripgrep-all`
- macOS: `~/Library/Caches/ripgrep-all`

---

## bat — Better Cat

### What It Does
bat is a cat clone with syntax highlighting and Git integration. It shows file contents with line numbers, syntax highlighting, and Git modifications.

### Basic Usage
```bash
# View file with syntax highlighting
bat file.md

# Plain output (for piping)
bat -p --paging=never file.py

# Show specific lines
bat --line-range 10:20 file.py
```

### When to Use bat

| Scenario | Tool | Reason |
|----------|------|--------|
| View code/config files | `bat` | Syntax highlighting |
| View with line numbers | `bat` | Built-in line numbers |
| View Git diff highlights | `bat` | Shows modifications |
| Pipe to another command | `bat -p` | Plain mode strips formatting |
| View specific line range | `bat` | Use `--line-range` |
| View very large files | `bat` | Has paging built-in |
| Quick one-liner view | `cat` | Faster for tiny files |
| Edit file content | Use editor | bat is read-only |

### When NOT to Use bat
- **Edit files** → Use an editor (vim, nano, VS Code)
- **Create new files** → Use `echo >` or editor
- **Append to files** → Use `echo >>` or `tee`
- **Binary files** → Use `xxd` or `hexdump`
- **Script needing raw output** → Use `cat` or `bat -p`

---

## pandoc — Document Converter

### What It Does
Pandoc is a universal document converter. It can convert between dozens of markup and document formats, making it ideal for documentation workflows.

### Basic Usage
```bash
# Markdown to HTML
pandoc input.md -o output.html

# Any format to any format
pandoc input.docx -o output.md

# GitHub Flavored Markdown to standard markdown
pandoc -f gfm -t markdown input.md -o output.md
```

### When to Use pandoc

| Scenario | Tool | Reason |
|----------|------|--------|
| Convert Markdown ↔ HTML | `pandoc` | Most common use case |
| Convert Office docs ↔ Markdown | `pandoc` | Supports .docx, .odt |
| Convert to PDF | `pandoc` | Requires LaTeX engine |
| Create presentations | `pandoc` | Supports reveal.js, beamer |
| Extract text from PDF | `rga` | pandoc converts, rga searches |
| Search inside PDFs | `rga` | pandoc doesn't search |
| JSON ↔ YAML conversion | `yq` | yq is simpler for formats |
| Simple JSON manipulation | `jq` | jq is lighter |

### When NOT to Use pandoc
- **Search PDF content** → Use `rga` instead
- **Extract specific PDF text** → Use `rga` or `pdftotext`
- **Convert JSON/YAML** → Use `yq` instead
- **Batch rename files** → Use `fd` + `mv`

---

## uv — Python Package Manager

### What It Does
uv is an extremely fast Python package installer and resolver, written in Rust. It replaces pip, pip-tools, pipx, poetry, pyenv, virtualenv, and more with a single tool.

### Basic Usage
```bash
# Create virtual environment
uv venv

# Install package
uv pip install requests

# Add dependency to project
uv add requests

# Run script
uv run script.py
```

### When to Use uv

| Scenario | Tool | Reason |
|----------|------|--------|
| Create Python virtual env | `uv venv` | Much faster than venv |
| Install Python packages | `uv pip install` | Faster than pip |
| Manage project dependencies | `uv add` | Creates pyproject.toml |
| Run Python scripts | `uv run` | Auto-syncs dependencies |
| Lock dependencies | `uv lock` | Creates uv.lock |
| System Python install | `uv python install` | Installs Python versions |
| Standard pip workflow | `pip` | Traditional but slower |

### When NOT to Use uv
- **Global system packages** → Use `pip` with caution
- **Conda environments** → Use `conda` for data science packages
- **Legacy projects with requirements.txt** → Use `pip install -r`

---

## delta — Pretty Diff Viewer

### What It Does
delta enhances git diff output with syntax highlighting, side-by-side view, and improved readability. It's a pager that formats diff output beautifully.

### Basic Usage
```bash
# View diff with delta
git diff | delta

# Side-by-side view
delta --side-by-side

# Configure as git pager (one-time setup)
git config --global core.pager "delta"
```

### When to Use delta

| Scenario | Tool | Reason |
|----------|------|--------|
| View git diff output | `delta` | Colorized, readable |
| Side-by-side comparison | `delta --side-by-side` | Better for code review |
| Review PR changes | `delta` | GitHub-style rendering |
| Compare two files | `delta file1 file2` | Built-in file comparison |
| View git log visually | `git log -p \| delta` | Shows commit diffs |
| Simple one-line diff | `diff` | Faster for tiny files |
| Binary file comparison | `diff` or `cmp` | Not delta's use case |

### When NOT to Use delta
- **Script diff output** → Use raw `diff` or git diff output
- **Binary files** → Use `cmp` or `xxd` comparison
- **Non-interactive scripts** → Delta requires terminal

---

## dust — Disk Usage Visualization

### What It Does
dust (du + rust) is a more intuitive version of du, showing disk usage with a visual representation of directory sizes. It displays directories by size with bars indicating relative usage.

### Basic Usage
```bash
# Show directory sizes
dust

# Show all files (not truncated)
dust -n 999

# Show specific number of directories
dust -n 20

# Reverse sort (largest at bottom)
dust -r
```

### When to Use dust

| Scenario | Tool | Reason |
|----------|------|--------|
| Find largest directories | `dust` | Visual, intuitive |
| Find what's using disk space | `dust` | Shows size bars |
| Quick disk overview | `dust` | Fast and clear |
| Find large files | `dust` or `fd --size` | Both work |
| Script disk usage reporting | `du` | More portable |
| Find files by name | `fd` | dust shows sizes, not names |
| Count file sizes | `du -sh` | Traditional but works |

### When NOT to Use dust
- **Find files by name** → Use `fd` instead
- **Search file contents** → Use `rg` instead
- **Scripted du output** → Use `du` for POSIX compatibility
- **Inodes count** → Use `df -i`

---

## gh — GitHub CLI

### What It Does
gh is GitHub's official command-line tool. It brings pull requests, issues, and other GitHub concepts to the terminal next to where you are already working with git.

### Basic Usage
```bash
# Clone repo
gh repo clone owner/repo

# Create PR
gh pr create --title "Title" --body "Body"

# List issues
gh issue list

# View PR in browser
gh pr view --web
```

### When to Use gh

| Scenario | Tool | Reason |
|----------|------|--------|
| Create/manage PRs | `gh` | Official GitHub tool |
| Create/manage issues | `gh` | Full issue workflow |
| View GitHub Actions | `gh run` | CI/CD monitoring |
| Browse repos from terminal | `gh` | Without browser |
| Clone GitHub repos | `gh repo clone` | Authenticated clone |
| Create new repository | `gh repo create` | From terminal |
| Git operations (commit/push) | `git` | gh is for GitHub API |
| Browse remote files | `gh api` | Use GitHub API |
| Clone GitLab/Bitbucket | `git` | gh is GitHub-only |

### When NOT to Use gh
- **Local git operations** → Use `git` directly
- **GitLab/Bitbucket** → Use `git` or their CLIs
- **Non-GitHub repositories** → Use `git` directly

---

## Tool Selection Guide

| Task | Tool | Command Pattern |
|------|------|-----------------|
| Parse/read JSON | `jq` | `cat file.json \| jq '.path'` |
| Parse/read YAML | `yq` | `cat file.yaml \| yq '.path'` |
| Convert JSON↔YAML↔XML | `yq` | `cat file.json \| yq -o yaml '.'` |
| Merge JSON configs | `jq` | `jq -s '.[0] * .[1]' a.json b.json` |
| Find files by name | `fd` | `fd pattern` |
| Search file contents | `rg` | `rg "pattern"` |
| Search in PDFs | `rga` | `rga "pattern" *.pdf` |
| Search in archives | `rga` | `rga "pattern" archive.zip` |
| Search in Office docs | `rga` | `rga "pattern" *.docx` |
| Search sqlite databases | `rga` | `rga "pattern" *.db` |
| Search media metadata | `rga` | `rga "pattern" *.mp4` |
| View file with syntax | `bat` | `bat file.py` |
| Convert documents | `pandoc` | `pandoc in.md -o out.html` |
| Pretty git diffs | `delta` | `git diff \| delta` |
| Disk usage overview | `dust` | `dust` |
| GitHub operations | `gh` | `gh pr list` |
| Python packages | `uv` | `uv pip install X` |
| Pack repo for AI | `repomix` | `npx repomix --remote owner/repo` |
| Convert PDF to markdown | `marker` | `marker_single file.pdf` |
| Convert PDF to JSON/HTML | `marker` | `marker_single file.pdf --output_format json` |
| Convert PDF with LLM | `marker` | `marker_single file.pdf --use_llm` |

---

## Decision Tree

```
Need to access data?
├── JSON file → jq
├── YAML file → yq
└── XML file → yq

Need to find something?
├── File by name → fd
├── Text in files → rg
├── Text in archives/PDFs/binary → rga
│   ├── PDFs (.pdf) → rga
│   ├── Office docs (.docx, .xlsx) → rga
│   ├── Archives (.zip, .tar, .gz) → rga
│   ├── SQLite databases (.db) → rga
│   ├── Media metadata (.mp4, .mp3) → rga
│   └── E-books (.epub) → rga
└── In GitHub repos → gh

Need to view something?
├── Code/config with highlighting → bat
├── Plain for piping → bat -p --paging=never
└── Diff output → delta

Need to convert?
├── PDF/DOCX/PPTX to markdown/JSON → marker
│   ├── Simple PDF → marker
│   ├── Complex tables/forms → marker --use_llm
│   └── For RAG/chunking → marker --output_format chunks
├── Between doc formats → pandoc
├── JSON/YAML/XML → yq
└── Manipulate JSON → jq

Need Python?
├── Virtual env → uv venv
├── Install packages → uv pip install
└── Run script → uv run

Need to understand external codebase?
└── Pack repo for AI analysis → repomix --remote owner/repo
```
