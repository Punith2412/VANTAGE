<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Vantage — Engagement-ranked social research</title>
<meta name="description" content="A lightweight Python CLI that searches Reddit, Hacker News, GitHub and Dev.to in parallel, ranks results by real engagement, and produces a shareable Markdown + dark-mode HTML brief.">
<style>
  :root{
    --ink:#0d1117;
    --ink-2:#161b22;
    --panel:#0f141c;
    --panel-2:#161b22;
    --line:#21262d;
    --line-soft:#1c212b;
    --text:#e6edf3;
    --text-dim:#8b949e;
    --text-faint:#586069;
    --blue:#58a6ff;
    --green:#3fb950;
    --amber:#d29922;
    --purple:#c297ff;
    --mono: 'IBM Plex Mono', ui-monospace, 'SF Mono', Menlo, Consolas, monospace;
    --sans: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  }
  @media (prefers-reduced-motion: reduce){
    *{ animation-duration:0.01ms !important; animation-iteration-count:1 !important; transition-duration:0.01ms !important; }
  }
  *{ box-sizing:border-box; margin:0; padding:0; }
  html{ scroll-behavior:smooth; }
  body{
    background:var(--ink);
    color:var(--text);
    font-family:var(--sans);
    line-height:1.6;
    -webkit-font-smoothing:antialiased;
  }
  a{ color:inherit; }
  ::selection{ background:var(--blue); color:#031222; }
  :focus-visible{ outline:2px solid var(--blue); outline-offset:3px; border-radius:4px; }
  code{ font-family:var(--mono); }

  .wrap{ max-width:1080px; margin:0 auto; padding:0 28px; }

  /* NAV */
  nav{
    position:sticky; top:0; z-index:20;
    background:rgba(13,17,23,0.85);
    backdrop-filter:blur(10px);
    border-bottom:1px solid var(--line-soft);
  }
  nav .wrap{ display:flex; align-items:center; justify-content:space-between; height:64px; }
  .brand{ display:flex; align-items:center; gap:10px; font-family:var(--mono); font-weight:600; font-size:16px; letter-spacing:-0.02em; }
  .brand .dot{ width:8px; height:8px; border-radius:50%; background:var(--green); box-shadow:0 0 0 3px rgba(63,185,80,0.15); }
  .navlinks{ display:flex; gap:26px; font-size:14px; color:var(--text-dim); }
  .navlinks a{ text-decoration:none; transition:color .15s; }
  .navlinks a:hover{ color:var(--text); }
  .navcta{
    font-size:13px; font-family:var(--mono); color:var(--text);
    border:1px solid var(--line); padding:7px 14px; border-radius:6px;
    text-decoration:none; transition:border-color .15s, background .15s;
  }
  .navcta:hover{ border-color:var(--blue); background:rgba(88,166,255,0.08); }

  /* HERO */
  .hero{ padding:80px 0 56px; }
  .hero-grid{ display:grid; grid-template-columns:1fr 1fr; gap:56px; align-items:center; }
  .eyebrow{
    font-family:var(--mono); font-size:12.5px; color:var(--amber);
    display:inline-flex; align-items:center; gap:8px; margin-bottom:20px;
    border:1px solid rgba(210,153,34,0.3); background:rgba(210,153,34,0.08);
    padding:5px 10px; border-radius:20px;
  }
  h1{
    font-family:var(--mono); font-size:42px; font-weight:700; letter-spacing:-0.02em;
    line-height:1.15; margin-bottom:18px;
  }
  .grad-underline{
    background:linear-gradient(90deg,var(--blue),var(--green));
    -webkit-background-clip:text; background-clip:text; color:transparent;
  }
  .lede{ font-size:17px; color:var(--text-dim); max-width:480px; margin-bottom:14px; }
  .lede-sub{ font-size:14px; color:var(--text-faint); max-width:480px; margin-bottom:30px; }
  .cta-row{ display:flex; gap:12px; flex-wrap:wrap; }
  .btn{
    font-family:var(--sans); font-size:14.5px; font-weight:600;
    padding:12px 20px; border-radius:8px; text-decoration:none;
    display:inline-flex; align-items:center; gap:8px; transition:transform .15s, opacity .15s;
  }
  .btn:hover{ transform:translateY(-1px); }
  .btn-primary{ background:var(--text); color:var(--ink); }
  .btn-primary:hover{ opacity:0.9; }
  .btn-ghost{ border:1px solid var(--line); color:var(--text); }
  .btn-ghost:hover{ border-color:var(--text-faint); }

  .badges{ display:flex; gap:8px; margin-top:24px; flex-wrap:wrap; }
  .badge{
    font-family:var(--mono); font-size:11.5px; color:var(--text-faint);
    border:1px solid var(--line-soft); padding:4px 9px; border-radius:5px;
  }

  /* TERMINAL */
  .term{
    background:var(--panel); border:1px solid var(--line); border-radius:10px;
    overflow:hidden; box-shadow:0 24px 60px -20px rgba(0,0,0,0.6);
  }
  .term-bar{
    display:flex; align-items:center; gap:7px; padding:12px 14px;
    border-bottom:1px solid var(--line-soft); background:var(--panel-2);
  }
  .term-bar span{ width:10px; height:10px; border-radius:50%; }
  .term-bar span:nth-child(1){ background:#ff5f57; }
  .term-bar span:nth-child(2){ background:#febc2e; }
  .term-bar span:nth-child(3){ background:#28c840; }
  .term-title{ font-family:var(--mono); font-size:12px; color:var(--text-faint); margin-left:8px; }
  .term-body{ padding:20px 18px; font-family:var(--mono); font-size:13px; min-height:300px; }
  .prompt{ color:var(--green); }
  .cmd{ color:var(--text); }
  .out-dim{ color:var(--text-faint); }
  .out-title{ color:var(--text-dim); }
  .tag-reddit{ color:var(--amber); }
  .tag-hn{ color:var(--blue); }
  .tag-gh{ color:var(--green); }
  .cursor{
    display:inline-block; width:7px; height:14px; background:var(--green);
    vertical-align:middle; animation:blink 1s steps(1) infinite;
  }
  @keyframes blink{ 50%{ opacity:0; } }

  /* SECTIONS */
  section{ padding:60px 0; border-top:1px solid var(--line-soft); }
  .section-head{ margin-bottom:34px; max-width:600px; }
  .section-label{ font-family:var(--mono); font-size:12px; color:var(--text-faint); text-transform:uppercase; letter-spacing:0.08em; margin-bottom:10px; }
  h2{ font-family:var(--mono); font-size:25px; font-weight:700; letter-spacing:-0.02em; margin-bottom:10px; }
  .section-desc{ color:var(--text-dim); font-size:15px; }

  /* WHY TABLE */
  .why-table{ display:grid; grid-template-columns:1fr 1fr; border:1px solid var(--line); border-radius:10px; overflow:hidden; margin-bottom:28px; }
  .why-col-head{ font-family:var(--mono); font-size:12.5px; padding:14px 18px; border-bottom:1px solid var(--line); }
  .why-col:first-child{ background:var(--panel); }
  .why-col:first-child .why-col-head{ color:var(--text-faint); }
  .why-col:last-child{ background:rgba(63,185,80,0.05); }
  .why-col:last-child .why-col-head{ color:var(--green); }
  .why-row{ padding:14px 18px; font-size:14px; border-bottom:1px solid var(--line-soft); }
  .why-col:first-child .why-row{ color:var(--text-faint); }
  .why-col:last-child .why-row{ color:var(--text); }
  .why-row:last-child{ border-bottom:none; }

  .usecases{ display:grid; grid-template-columns:repeat(4,1fr); gap:12px; }
  .usecase{ background:var(--panel); border:1px solid var(--line); border-radius:10px; padding:16px 18px; font-size:13.5px; color:var(--text-dim); }
  .usecase b{ color:var(--text); display:block; margin-bottom:4px; font-size:13px; }

  /* SOURCES */
  .sources-grid{ display:grid; grid-template-columns:repeat(4, 1fr); gap:14px; }
  .source-card{ background:var(--panel); border:1px solid var(--line); border-radius:10px; padding:20px; }
  .source-name{ font-family:var(--mono); font-size:14px; font-weight:600; margin-bottom:8px; }
  .source-card:nth-child(1) .source-name{ color:var(--amber); }
  .source-card:nth-child(2) .source-name{ color:var(--blue); }
  .source-card:nth-child(3) .source-name{ color:var(--green); }
  .source-card:nth-child(4) .source-name{ color:var(--purple); }
  .source-formula{ font-family:var(--mono); font-size:12.5px; color:var(--text-dim); background:var(--panel-2); border-radius:6px; padding:8px 10px; }

  /* CODE BLOCKS */
  .code-block{
    background:var(--panel); border:1px solid var(--line); border-radius:10px;
    padding:20px 22px; font-family:var(--mono); font-size:13.5px; color:var(--text-dim);
    overflow-x:auto;
  }
  .code-block div{ margin-bottom:8px; white-space:pre; }
  .code-block div:last-child{ margin-bottom:0; }
  .code-block .cmd{ color:var(--text); }
  .code-block .comment{ color:var(--text-faint); }
  .code-block .prompt{ margin-right:6px; }

  .two-col{ display:grid; grid-template-columns:1fr 1fr; gap:20px; align-items:start; }

  /* TREE */
  .tree{
    background:var(--panel); border:1px solid var(--line); border-radius:10px;
    padding:20px 22px; font-family:var(--mono); font-size:12.8px; color:var(--text-dim);
    overflow-x:auto; line-height:1.75;
  }
  .tree .dir{ color:var(--blue); }
  .tree .comment{ color:var(--text-faint); }

  /* OPTIONS TABLE */
  .opt-table{ width:100%; border-collapse:collapse; font-size:13.5px; }
  .opt-table th{ text-align:left; font-family:var(--mono); font-size:11.5px; color:var(--text-faint); text-transform:uppercase; letter-spacing:0.05em; padding:10px 14px; border-bottom:1px solid var(--line); }
  .opt-table td{ padding:12px 14px; border-bottom:1px solid var(--line-soft); color:var(--text-dim); }
  .opt-table td:first-child{ font-family:var(--mono); color:var(--text); white-space:nowrap; }
  .opt-table tr:last-child td{ border-bottom:none; }
  .opt-wrap{ background:var(--panel); border:1px solid var(--line); border-radius:10px; overflow:hidden; }

  /* NOTES */
  .notes{ list-style:none; }
  .notes li{ position:relative; padding-left:22px; margin-bottom:12px; color:var(--text-dim); font-size:14.5px; }
  .notes li::before{ content:"—"; position:absolute; left:0; color:var(--text-faint); }

  /* FOOTER */
  footer{ border-top:1px solid var(--line-soft); padding:36px 0; }
  footer .wrap{ display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px; }
  .foot-text{ font-size:13px; color:var(--text-faint); font-family:var(--mono); }
  .foot-links{ display:flex; gap:20px; font-size:13px; }
  .foot-links a{ text-decoration:none; color:var(--text-dim); transition:color .15s; }
  .foot-links a:hover{ color:var(--text); }

  @media (max-width: 860px){
    .hero-grid{ grid-template-columns:1fr; }
    .why-table{ grid-template-columns:1fr; }
    .sources-grid{ grid-template-columns:1fr 1fr; }
    .usecases{ grid-template-columns:1fr 1fr; }
    .two-col{ grid-template-columns:1fr; }
    h1{ font-size:32px; }
    .navlinks{ display:none; }
  }
  @media (max-width: 520px){
    .sources-grid{ grid-template-columns:1fr; }
    .usecases{ grid-template-columns:1fr; }
  }
</style>
</head>
<body>

<nav>
  <div class="wrap">
    <div class="brand"><span class="dot"></span>vantage</div>
    <div class="navlinks">
      <a href="#why">Why</a>
      <a href="#sources">Sources</a>
      <a href="#quickstart">Quick start</a>
      <a href="#internals">Internals</a>
      <a href="#testing">Testing</a>
    </div>
    <a class="navcta" href="https://github.com/Punith2412/VANTAGE" target="_blank" rel="noopener">GitHub ↗</a>
  </div>
</nav>

<header class="hero">
  <div class="wrap hero-grid">
    <div>
      <div class="eyebrow">● no API keys required</div>
      <h1>Engagement-ranked<br><span class="grad-underline">social research.</span></h1>
      <p class="lede">Reddit upvotes · Hacker News points · GitHub stars · Dev.to reactions — scored by real attention, not SEO.</p>
      <p class="lede-sub">A lightweight, fully readable Python CLI (~1,000 lines). No black-box agent skill, no heavy frameworks, no code you didn't write.</p>
      <div class="cta-row">
        <a class="btn btn-primary" href="https://github.com/Punith2412/VANTAGE" target="_blank" rel="noopener">View on GitHub</a>
        <a class="btn btn-ghost" href="#quickstart">Quick start →</a>
      </div>
      <div class="badges">
        <span class="badge">python 3.11+</span>
        <span class="badge">mit license</span>
        <span class="badge">pytest · 25 passing</span>
        <span class="badge">ruff</span>
      </div>
    </div>

    <div class="term">
      <div class="term-bar">
        <span></span><span></span><span></span>
        <span class="term-title">~/vantage</span>
      </div>
      <div class="term-body" id="termBody"></div>
    </div>
  </div>
</header>

<section id="why">
  <div class="wrap">
    <div class="section-head">
      <div class="section-label">Why vantage</div>
      <h2>Ranked by attention, not algorithms</h2>
    </div>
    <div class="why-table">
      <div class="why-col">
        <div class="why-col-head">Traditional search</div>
        <div class="why-row">SEO + editor ranking</div>
        <div class="why-row">Single platform silos</div>
        <div class="why-row">Opaque ranking</div>
        <div class="why-row">Heavy agent frameworks</div>
      </div>
      <div class="why-col">
        <div class="why-col-head">Vantage</div>
        <div class="why-row">Upvotes, points, stars, reactions</div>
        <div class="why-row">Parallel multi-source</div>
        <div class="why-row">Transparent engagement score</div>
        <div class="why-row">Clear, reviewable Python</div>
      </div>
    </div>
    <div class="usecases">
      <div class="usecase"><b>Competitive research</b>Quick product or competitor scans across platforms.</div>
      <div class="usecase"><b>Trend tracking</b>What the community actually cared about in the last N days.</div>
      <div class="usecase"><b>Shareable briefs</b>Generate a brief for yourself or a team in seconds.</div>
      <div class="usecase"><b>QA portfolio piece</b>Clean architecture + a real automated test suite.</div>
    </div>
  </div>
</section>

<section id="sources">
  <div class="wrap">
    <div class="section-head">
      <div class="section-label">Sources</div>
      <h2>Four platforms, one score</h2>
      <p class="section-desc">Every result becomes a <code>Signal</code> with a common engagement score, using a simple published formula per source.</p>
    </div>
    <div class="sources-grid">
      <div class="source-card">
        <div class="source-name">reddit</div>
        <div class="source-formula">score + 0.3 × comments</div>
      </div>
      <div class="source-card">
        <div class="source-name">hacker news</div>
        <div class="source-formula">points + 0.5 × comments</div>
      </div>
      <div class="source-card">
        <div class="source-name">github</div>
        <div class="source-formula">stars + 0.4 × forks</div>
      </div>
      <div class="source-card">
        <div class="source-name">dev.to</div>
        <div class="source-formula">reactions + 0.4 × comments</div>
      </div>
    </div>
  </div>
</section>

<section id="quickstart">
  <div class="wrap">
    <div class="section-head">
      <div class="section-label">Quick start</div>
      <h2>Running in under a minute</h2>
      <p class="section-desc">No API keys required for the default sources (Reddit public JSON, HN Algolia, GitHub unauthenticated search, Dev.to public API).</p>
    </div>
    <div class="code-block">
      <div><span class="comment"># requires Python 3.11+</span></div>
      <div><span class="prompt">$</span><span class="cmd">pip install -e ".[dev]"   </span><span class="comment"># includes pytest, ruff</span></div>
      <div>&nbsp;</div>
      <div><span class="comment"># research anything</span></div>
      <div><span class="prompt">$</span><span class="cmd">vantage research "Cursor AI editor" --days 30</span></div>
      <div>&nbsp;</div>
      <div><span class="comment"># only reddit</span></div>
      <div><span class="prompt">$</span><span class="cmd">vantage research "open source LLM" -s reddit --days 14</span></div>
      <div>&nbsp;</div>
      <div><span class="comment"># all sources, custom output folder</span></div>
      <div><span class="prompt">$</span><span class="cmd">vantage research "Anthropic Claude" -s all -o ./briefs</span></div>
    </div>
    <p class="section-desc" style="margin-top:16px;">Outputs two files: <code>vantage-&lt;topic&gt;-&lt;timestamp&gt;.md</code> and <code>vantage-&lt;topic&gt;-&lt;timestamp&gt;.html</code> — a self-contained dark-mode shareable brief.</p>
  </div>
</section>

<section id="internals">
  <div class="wrap">
    <div class="section-head">
      <div class="section-label">Under the hood</div>
      <h2>Fan-out → normalize → rank → diversify → render</h2>
    </div>
    <div class="two-col">
      <div class="code-block">
        <div><span class="comment">1. Fan-out</span>  query 4 sources concurrently</div>
        <div><span class="comment">2. Normalize</span> every result → a Signal</div>
        <div><span class="comment">3. Rank</span>     engagement + recency boost</div>
        <div><span class="comment">4. Diversify</span> soft per-author cap</div>
        <div><span class="comment">5. Render</span>   Markdown + dark HTML</div>
      </div>
      <div class="tree">
<span class="dir">vantage/src/vantage/</span><br>
├── cli.py <span class="comment"># Typer CLI</span><br>
├── engine.py <span class="comment"># orchestration + ranking</span><br>
├── models.py <span class="comment"># Pydantic models</span><br>
├── render.py <span class="comment"># Markdown + dark HTML</span><br>
└── sources/<br>
&nbsp;&nbsp;&nbsp;&nbsp;├── base.py<br>
&nbsp;&nbsp;&nbsp;&nbsp;├── reddit.py<br>
&nbsp;&nbsp;&nbsp;&nbsp;├── hackernews.py<br>
&nbsp;&nbsp;&nbsp;&nbsp;├── github.py<br>
&nbsp;&nbsp;&nbsp;&nbsp;└── devto.py
      </div>
    </div>

    <div style="margin-top:28px;" class="opt-wrap">
      <table class="opt-table">
        <thead><tr><th>Option</th><th>Description</th></tr></thead>
        <tbody>
          <tr><td>-d, --days</td><td>Look-back window in days (default 30)</td></tr>
          <tr><td>-s, --sources</td><td>reddit | hackernews | github | devto | all</td></tr>
          <tr><td>--max</td><td>Max results per source (default 12)</td></tr>
          <tr><td>--min-eng</td><td>Minimum engagement threshold</td></tr>
          <tr><td>-o, --out</td><td>Output directory for markdown/html</td></tr>
          <tr><td>--open</td><td>Print HTML path reminder</td></tr>
        </tbody>
      </table>
    </div>
  </div>
</section>

<section id="testing">
  <div class="wrap">
    <div class="section-head">
      <div class="section-label">Testing &amp; quality</div>
      <h2>Built to be audited</h2>
      <p class="section-desc">Models — schema validation &amp; defaults. Engine — ranking order, author diversification, graceful source failure. Render — Markdown/HTML output. Sources — mocked HTTP, no network in CI. Runs on every push against Python 3.11 and 3.12.</p>
    </div>
    <div class="code-block">
      <div><span class="prompt">$</span><span class="cmd">pytest -v</span></div>
      <div><span class="out-dim">tests/test_models.py   .........</span> <span style="color:var(--green)">PASSED</span></div>
      <div><span class="out-dim">tests/test_engine.py   .....    </span> <span style="color:var(--green)">PASSED</span></div>
      <div><span class="out-dim">tests/test_render.py   ......   </span> <span style="color:var(--green)">PASSED</span></div>
      <div><span class="out-dim">tests/test_sources.py  ......   </span> <span style="color:var(--green)">PASSED</span></div>
      <div>&nbsp;</div>
      <div><span class="out-dim">======================== 25 passed in 0.30s ========================</span></div>
    </div>
  </div>
</section>

<section id="extending">
  <div class="wrap">
    <div class="section-head">
      <div class="section-label">Extending</div>
      <h2>Add a new source in one file</h2>
      <p class="section-desc">Want YouTube, X, Lobsters, or Polymarket? Inherit <code>BaseSource</code>, implement <code>async def search()</code>, register it in <code>engine.SOURCE_MAP</code> and add the enum value in <code>models.SourceType</code>. That's it.</p>
    </div>
    <div class="code-block">
      <div><span class="comment">from vantage.sources.base import BaseSource</span></div>
      <div><span class="comment">from vantage.models import Signal, SourceType</span></div>
      <div>&nbsp;</div>
      <div><span class="cmd">class YouTubeSource(BaseSource):</span></div>
      <div><span class="cmd">    source_type = SourceType.YOUTUBE</span></div>
      <div>&nbsp;</div>
      <div><span class="cmd">    async def search(self) -> list[Signal]:</span></div>
      <div><span class="comment">        # implement with public endpoints or your API key</span></div>
      <div><span class="cmd">        return []</span></div>
    </div>
  </div>
</section>

<section id="notes">
  <div class="wrap">
    <div class="section-head">
      <div class="section-label">Notes</div>
      <h2>Good to know</h2>
    </div>
    <ul class="notes">
      <li>Reddit sometimes returns 403 from datacenter IPs — that's expected and handled gracefully; the other sources still run. On a normal machine it usually works fine.</li>
      <li>GitHub unauthenticated search has a low rate limit; for heavier use, set a <code>GITHUB_TOKEN</code> env var (future enhancement).</li>
      <li>Every line is yours — easy to audit, extend, and test.</li>
    </ul>
  </div>
</section>

<footer>
  <div class="wrap">
    <div class="foot-text">MIT © 2026 Punith Patil — clean-room implementation, built for clarity, testability, and ownership of every line.</div>
    <div class="foot-links">
      <a href="https://github.com/Punith2412/VANTAGE" target="_blank" rel="noopener">GitHub</a>
      <a href="https://github.com/Punith2412" target="_blank" rel="noopener">Punith2412</a>
      <a href="mailto:punithpatil2412@gmail.com">Contact</a>
    </div>
  </div>
</footer>

<script>
(function(){
  var body = document.getElementById('termBody');
  var lines = [
    {t:'prompt', v:'$ '},{t:'cmd', v:'vantage research "AI coding agents" --days 30\n'},
    {t:'dim', v:'Querying reddit, hackernews, github, devto…\n\n'},
    {t:'title', v:'Top signals by engagement\n'},
    {t:'reddit', v:'1. '},{t:'dim',v:'[Why every AI agent breaks on long tasks] '},{t:'reddit',v:'reddit '},{t:'dim',v:'(score=842)\n'},
    {t:'hn', v:'2. '},{t:'dim',v:'[Show HN: I built a coding agent in 400 lines] '},{t:'hn',v:'hackernews '},{t:'dim',v:'(points=511)\n'},
    {t:'gh', v:'3. '},{t:'dim',v:'[agent-eval-suite] '},{t:'gh',v:'github '},{t:'dim',v:'(stars=1204)\n'},
    {t:'reddit', v:'4. '},{t:'dim',v:'[Claude vs GPT for agentic workflows, 3mo later] '},{t:'reddit',v:'reddit '},{t:'dim',v:'(score=396)\n\n'},
    {t:'title', v:'Recurring themes\n'},
    {t:'dim', v:'`ai` `agents` `open source` `performance` `release`\n\n'},
    {t:'dim', v:'Markdown → vantage-ai-coding-agents-20260812.md\n'},
    {t:'dim', v:'HTML     → vantage-ai-coding-agents-20260812.html\n'}
  ];
  var out = '';
  var i = 0;
  function classFor(t){
    if(t==='prompt') return 'prompt';
    if(t==='cmd') return 'cmd';
    if(t==='dim') return 'out-dim';
    if(t==='title') return 'out-title';
    if(t==='reddit') return 'tag-reddit';
    if(t==='hn') return 'tag-hn';
    if(t==='gh') return 'tag-gh';
    return '';
  }
  function step(){
    if(i >= lines.length){
      body.innerHTML = out + '<span class="cursor"></span>';
      return;
    }
    var seg = lines[i];
    out += '<span class="'+classFor(seg.t)+'">'+seg.v.replace(/\n/g,'<br>')+'</span>';
    body.innerHTML = out + '<span class="cursor"></span>';
    i++;
    setTimeout(step, seg.t === 'cmd' ? 400 : 90);
  }
  step();
})();
</script>

</body>
</html>
