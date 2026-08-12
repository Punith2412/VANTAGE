# Vantage

**Engagement-ranked social research.**  
Reddit upvotes · Hacker News points · GitHub stars · Dev.to reactions — scored by real attention, not SEO.

<p align="center">
  <img src="<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="400" viewBox="0 0 1280 400">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#0E1013"/>
      <stop offset="100%" style="stop-color:#171A21"/>
    </linearGradient>
    <linearGradient id="signal" x1="0%" y1="100%" x2="0%" y2="0%">
      <stop offset="0%" style="stop-color:#7A5A2A"/>
      <stop offset="100%" style="stop-color:#FFB13D"/>
    </linearGradient>
    <radialGradient id="glow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" style="stop-color:#FFB13D" stop-opacity="0.16"/>
      <stop offset="100%" style="stop-color:#FFB13D" stop-opacity="0"/>
    </radialGradient>
    <clipPath id="clip"><rect width="1280" height="400" rx="18"/></clipPath>
  </defs>

  <g clip-path="url(#clip)">
    <rect width="1280" height="400" fill="url(#bg)"/>

    <!-- topographic contour rings, top-right (the "vantage point" motif) -->
    <g fill="none" stroke="#FFB13D" stroke-opacity="0.12">
      <circle cx="1080" cy="90" r="60"/>
      <circle cx="1080" cy="90" r="105"/>
      <circle cx="1080" cy="90" r="150"/>
      <circle cx="1080" cy="90" r="195"/>
      <circle cx="1080" cy="90" r="240"/>
    </g>
    <g fill="none" stroke="#6FD6C8" stroke-opacity="0.08">
      <circle cx="150" cy="340" r="50"/>
      <circle cx="150" cy="340" r="95"/>
      <circle cx="150" cy="340" r="140"/>
    </g>
    <rect width="1280" height="400" fill="url(#glow)"/>

    <!-- hairline baseline -->
    <line x1="72" y1="330" x2="1208" y2="330" stroke="#2A2F3A" stroke-width="1"/>

    <!-- eyebrow -->
    <text x="74" y="118" font-family="JetBrains Mono, Consolas, monospace" font-size="15" letter-spacing="3" fill="#FFB13D">MULTI-SOURCE RESEARCH ENGINE</text>

    <!-- wordmark -->
    <text x="72" y="205" font-family="Space Grotesk, Segoe UI, Helvetica, sans-serif" font-size="88" font-weight="700" fill="#E7E9EE">VANTAGE</text>

    <!-- tagline -->
    <text x="74" y="250" font-family="IBM Plex Sans, Segoe UI, sans-serif" font-size="21" fill="#9BA1AE">Engagement-ranked social research — Reddit, Hacker News, GitHub, Dev.to</text>

    <!-- signal meter cluster, echoes the app's ranked-list meters -->
    <g transform="translate(950, 260)">
      <rect x="0"  y="30" width="14" height="40" rx="3" fill="url(#signal)"/>
      <rect x="24" y="10" width="14" height="60" rx="3" fill="url(#signal)"/>
      <rect x="48" y="42" width="14" height="28" rx="3" fill="#FF6A3D" opacity="0.85"/>
      <rect x="72" y="0"  width="14" height="70" rx="3" fill="url(#signal)"/>
      <rect x="96" y="34" width="14" height="36" rx="3" fill="#6FD6C8" opacity="0.85"/>
      <rect x="120" y="20" width="14" height="50" rx="3" fill="url(#signal)"/>
      <rect x="144" y="46" width="14" height="24" rx="3" fill="#FF6A3D" opacity="0.7"/>
      <rect x="168" y="8"  width="14" height="62" rx="3" fill="url(#signal)"/>
    </g>

    <!-- source strip -->
    <g font-family="JetBrains Mono, Consolas, monospace" font-size="13" fill="#656B78">
      <circle cx="80" cy="365" r="4" fill="#FF6A3D"/>
      <text x="92" y="370">reddit</text>
      <circle cx="170" cy="365" r="4" fill="#FF9B3D"/>
      <text x="182" y="370">hackernews</text>
      <circle cx="288" cy="365" r="4" fill="#6FD6C8"/>
      <text x="300" y="370">github</text>
      <circle cx="380" cy="365" r="4" fill="#9BA1AE"/>
      <text x="392" y="370">dev.to</text>
      <text x="1208" y="370" text-anchor="end" fill="#656B78">no api keys required</text>
    </g>
  </g>
</svg>" alt="Vantage – Engagement-ranked social research" width="720" />
</p>

<p align="center">
  <img src="https://img.shields.io/badge/python-3.11%2B-blue?logo=python&logoColor=white" alt="Python 3.11+" />
  <img src="https://img.shields.io/badge/license-MIT-green" alt="MIT License" />
  <img src="https://img.shields.io/badge/tests-pytest-orange" alt="pytest" />
  <img src="https://img.shields.io/badge/style-ruff-black" alt="Ruff" />
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/Punith2412/VANTAGE/main/docs/vantage-screenshot.svg" alt="A generated Vantage brief — ranked signals with source badges and engagement meters" width="820" />
</p>
<p align="center"><sub>The self-contained dark-mode HTML brief Vantage generates for every search.</sub></p>

Vantage is a lightweight, fully readable Python CLI that searches multiple public platforms **in parallel**, ranks results by actual community engagement, and produces a clean **Markdown + dark-mode HTML** brief.

It is intentionally small (~1 000 lines), testable, and fully under your control — no black-box agent skill, no heavy frameworks, no code you didn’t write.

---

## Why Vantage?

| Traditional search | Vantage |
|--------------------|---------|
| SEO + editor ranking | Upvotes, points, stars, reactions |
| Single platform silos | Parallel multi-source |
| Opaque ranking | Transparent engagement score |
| Heavy agent frameworks | Clear, reviewable Python |

**Perfect for**
- Quick competitive or product research
- Tracking what the community actually cares about in the last N days
- Generating shareable briefs for yourself or a team
- Demonstrating clean architecture + solid automated testing (ideal portfolio project for Software Testing / QA roles)

---

## Quick start

```bash
# Requires Python 3.11+
pip install -e ".[dev]"   # includes pytest, ruff

# Research anything
vantage research "Cursor AI editor" --days 30

# Only Reddit + HN
vantage research "open source LLM" -s reddit --days 14

# All sources, custom output folder
vantage research "Anthropic Claude" -s all -o ./briefs
```

You get two files:
- `vantage-<topic>-<timestamp>.md` — ready for notes / PR descriptions
- `vantage-<topic>-<timestamp>.html` — self-contained dark-mode shareable brief

**No API keys required** for the default sources (Reddit public JSON, HN Algolia, GitHub unauthenticated search, Dev.to public API).

---

## What it does under the hood

1. **Fan-out** – queries Reddit, Hacker News, GitHub and Dev.to concurrently  
2. **Normalize** – every result becomes a `Signal` with a common engagement score  
3. **Rank** – primary sort by engagement + mild recency boost  
4. **Diversify** – soft per-author cap so one voice doesn’t dominate  
5. **Render** – Markdown summary + self-contained dark HTML  

**Engagement formulas** (simple & transparent):

| Source       | Formula                          |
|--------------|----------------------------------|
| Reddit       | `score + 0.3 × comments`         |
| Hacker News  | `points + 0.5 × comments`        |
| GitHub       | `stars + 0.4 × forks`            |
| Dev.to       | `reactions + 0.4 × comments`     |

---

## Project layout

```
vantage/
├── src/vantage/
│   ├── cli.py          # Typer CLI
│   ├── engine.py       # Orchestration + ranking + summary
│   ├── models.py       # Pydantic models
│   ├── render.py       # Markdown + dark HTML
│   └── sources/
│       ├── base.py
│       ├── reddit.py
│       ├── hackernews.py
│       ├── github.py
│       └── devto.py
├── tests/              # Unit + integration-style tests (mocked HTTP)
│   ├── test_models.py
│   ├── test_engine.py
│   ├── test_render.py
│   └── test_sources.py
├── docs/
│   └── vantage-banner.svg
├── .github/workflows/ci.yml
├── pyproject.toml
└── README.md
```

---

## Testing & Quality (QA-friendly)

This project is designed to showcase practical testing skills:

```bash
# Install with dev extras
pip install -e ".[dev]"

# Run the full suite
pytest -v

# With coverage (optional)
pip install pytest-cov
pytest --cov=vantage --cov-report=term-missing

# Lint
ruff check src tests
```

**What the tests cover**
- **Models** – schema validation, defaults, required fields, enum values
- **Engine** – ranking order, author diversification (max 3 per author), graceful source failure
- **Render** – Markdown structure, dark HTML output, file writing
- **Sources** – mocked HTTP responses for Reddit / HN / GitHub / Dev.to (no network in CI)

CI runs on every push/PR against Python 3.11 and 3.12 (see `.github/workflows/ci.yml`).

---

## Configuration & options

```
vantage research TOPIC [OPTIONS]

Options:
  -d, --days INTEGER       Look-back window (default 30)
  -s, --sources            reddit | hackernews | github | devto | all
  --max INTEGER            Max results per source (default 12)
  --min-eng FLOAT          Minimum engagement threshold
  -o, --out PATH           Output directory
  --open                   Print HTML path reminder
```

```bash
vantage version
```

---

## Extending

Want YouTube, X (Twitter), Lobsters, or Polymarket later?  
Add a new class under `sources/` that inherits `BaseSource` and implements `async def search() -> list[Signal]`.  
Register it in `engine.SOURCE_MAP` and add the enum value in `models.SourceType`. That’s it.

Optional LLM synthesis can be layered on top of the existing template summary (see `engine._template_summary`) when you add an API key.

Example skeleton:

```python
from vantage.sources.base import BaseSource
from vantage.models import Signal, SourceType

class YouTubeSource(BaseSource):
    source_type = SourceType.YOUTUBE

    async def search(self) -> list[Signal]:
        # implement with public endpoints or your API key
        return []
```

---

## Notes

- Reddit sometimes returns 403 from datacenter IPs — that is normal and already handled gracefully (the other sources still run). On a normal machine it usually works fine.
- GitHub unauthenticated search has a low rate limit; for heavier use set a `GITHUB_TOKEN` env var (future enhancement).
- Every line is yours. Easy to audit, extend, and test.

---

## License

MIT. Copyright (c) 2026 Punith Patil.

Use it, fork it, learn from it, ship with it.

---

Built as a clean-room implementation focused on **clarity, testability, and ownership of every line**.  

Author: [Punith Patil](mailto:punithpatil2412@gmail.com)
