# Vantage

**Engagement-ranked social research.**  
Reddit upvotes · Hacker News points · GitHub stars · Dev.to reactions — scored by real attention, not SEO.

<p align="center">
  <img src="https://raw.githubusercontent.com/Punith2412/VANTAGE/2ee226b51c5aeaddca19d7e60eca3ddfac731ef9/vantage/docs/vantage-banner.svg" alt="Vantage – Engagement-ranked social research" width="720" />
</p>

<p align="center">
  <img src="https://img.shields.io/badge/python-3.11%2B-blue?logo=python&logoColor=white" alt="Python 3.11+" />
  <img src="https://img.shields.io/badge/license-MIT-green" alt="MIT License" />
  <img src="https://img.shields.io/badge/tests-pytest-orange" alt="pytest" />
  <img src="https://img.shields.io/badge/style-ruff-black" alt="Ruff" />
</p>

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
