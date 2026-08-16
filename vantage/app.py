"""
Vantage Web App – FastAPI frontend for live deployment (Render, Railway, etc.)
"""

from __future__ import annotations

import asyncio
from typing import Optional

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from vantage.engine import run_research
from vantage.models import ResearchPlan, SourceType
from vantage.render import to_html

app = FastAPI(
    title="Vantage",
    description="Engagement-ranked social research across Reddit, HN, GitHub & Dev.to",
    version="0.1.0",
)

# ---------- Landing page (dark form) ----------
LANDING_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Vantage – Engagement-ranked research</title>
  <style>
    :root {
      --bg: #0d1117;
      --surface: #161b22;
      --border: #30363d;
      --text: #e6edf3;
      --muted: #8b949e;
      --accent: #58a6ff;
      --green: #3fb950;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
      background: var(--bg);
      color: var(--text);
      min-height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 1.5rem;
    }
    .card {
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 2rem;
      width: 100%;
      max-width: 520px;
      box-shadow: 0 8px 32px rgba(0,0,0,0.4);
    }
    h1 {
      font-size: 1.6rem;
      font-weight: 600;
      margin-bottom: 0.35rem;
      letter-spacing: -0.02em;
    }
    .subtitle {
      color: var(--muted);
      font-size: 0.9rem;
      margin-bottom: 1.75rem;
      line-height: 1.5;
    }
    label {
      display: block;
      font-size: 0.8rem;
      color: var(--muted);
      margin-bottom: 0.35rem;
      font-weight: 500;
    }
    input[type="text"], input[type="number"], select {
      width: 100%;
      background: var(--bg);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 0.7rem 0.9rem;
      color: var(--text);
      font-size: 0.95rem;
      margin-bottom: 1.1rem;
      outline: none;
      transition: border-color 0.15s;
    }
    input:focus, select:focus { border-color: var(--accent); }
    .row {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 0.9rem;
    }
    .sources {
      display: flex;
      flex-wrap: wrap;
      gap: 0.6rem;
      margin-bottom: 1.4rem;
    }
    .sources label {
      display: flex;
      align-items: center;
      gap: 0.35rem;
      background: var(--bg);
      border: 1px solid var(--border);
      border-radius: 999px;
      padding: 0.35rem 0.75rem;
      font-size: 0.8rem;
      cursor: pointer;
      margin: 0;
      color: var(--text);
    }
    .sources input { margin: 0; width: auto; }
    button {
      width: 100%;
      background: var(--accent);
      color: #fff;
      border: none;
      border-radius: 8px;
      padding: 0.85rem;
      font-size: 1rem;
      font-weight: 600;
      cursor: pointer;
      transition: opacity 0.15s;
    }
    button:hover { opacity: 0.9; }
    button:disabled {
      opacity: 0.5;
      cursor: not-allowed;
    }
    .footer {
      text-align: center;
      margin-top: 1.5rem;
      font-size: 0.75rem;
      color: var(--muted);
    }
    .spinner {
      display: none;
      text-align: center;
      margin-top: 1rem;
      color: var(--muted);
      font-size: 0.9rem;
    }
  </style>
</head>
<body>
  <div class="card">
    <h1>Vantage</h1>
    <p class="subtitle">
      Engagement-ranked social research.<br>
      Reddit · Hacker News · GitHub · Dev.to
    </p>

    <form method="post" action="/research" id="form">
      <label for="topic">Topic / product / person</label>
      <input type="text" id="topic" name="topic" placeholder="e.g. Cursor AI editor" required autofocus />

      <div class="row">
        <div>
          <label for="days">Look-back (days)</label>
          <input type="number" id="days" name="days" value="30" min="1" max="365" />
        </div>
        <div>
          <label for="max_results">Max per source</label>
          <input type="number" id="max_results" name="max_results" value="12" min="3" max="30" />
        </div>
      </div>

      <label>Sources</label>
      <div class="sources">
        <label><input type="checkbox" name="sources" value="reddit" checked /> Reddit</label>
        <label><input type="checkbox" name="sources" value="hackernews" checked /> Hacker News</label>
        <label><input type="checkbox" name="sources" value="github" checked /> GitHub</label>
        <label><input type="checkbox" name="sources" value="devto" checked /> Dev.to</label>
      </div>

      <button type="submit" id="btn">Generate Brief</button>
      <div class="spinner" id="spinner">Searching sources in parallel… this can take 10–30 seconds</div>
    </form>

    <p class="footer">No API keys required · Real community attention, not SEO</p>
  </div>

  <script>
    document.getElementById('form').addEventListener('submit', function() {
      document.getElementById('btn').disabled = true;
      document.getElementById('spinner').style.display = 'block';
    });
  </script>
</body>
</html>
"""


@app.get("/", response_class=HTMLResponse)
async def home():
    return LANDING_HTML


@app.post("/research", response_class=HTMLResponse)
async def research(
    topic: str = Form(...),
    days: int = Form(30),
    max_results: int = Form(12),
    sources: list[str] = Form(default=["reddit", "hackernews", "github", "devto"]),
):
    # Map form values → SourceType
    source_map = {
        "reddit": SourceType.REDDIT,
        "hackernews": SourceType.HACKERNEWS,
        "github": SourceType.GITHUB,
        "devto": SourceType.DEVTO,
    }
    selected = [source_map[s] for s in sources if s in source_map]
    if not selected:
        selected = list(source_map.values())

    plan = ResearchPlan(
        topic=topic.strip(),
        days=max(1, min(days, 365)),
        sources=selected,
        max_results_per_source=max(3, min(max_results, 30)),
        min_engagement=5.0,
    )

    try:
        brief = await run_research(plan)
        html = to_html(brief)

        # Inject a small "Back" button at the top of the generated brief
        back_btn = """
        <div style="max-width:820px;margin:0 auto 1.5rem;padding:0 1rem;">
          <a href="/" style="color:#58a6ff;text-decoration:none;font-size:0.9rem;">← New search</a>
        </div>
        """
        # Insert after <body>
        html = html.replace("<body>", f"<body>{back_btn}", 1)
        return HTMLResponse(content=html)

    except Exception as e:
        error_html = f"""<!DOCTYPE html>
<html><head><title>Error</title>
<style>
  body {{ background:#0d1117; color:#e6edf3; font-family:system-ui; padding:3rem; text-align:center; }}
  a {{ color:#58a6ff; }}
</style></head>
<body>
  <h1>Something went wrong</h1>
  <p style="color:#8b949e;margin:1rem 0;">{e}</p>
  <a href="/">← Try again</a>
</body></html>"""
        return HTMLResponse(content=error_html, status_code=500)


@app.get("/health")
async def health():
    return {"status": "ok", "service": "vantage"}
