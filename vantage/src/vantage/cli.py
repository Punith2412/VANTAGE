"""Vantage CLI entrypoint."""

from __future__ import annotations

import asyncio
from enum import Enum
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

from vantage.engine import run_research
from vantage.models import ResearchPlan, SourceType
from vantage.render import save_brief

app = typer.Typer(
    name="vantage",
    help="Vantage – engagement-ranked social research across Reddit, HN, GitHub, Dev.to.",
    add_completion=False,
)
console = Console()


class SourceChoice(str, Enum):
    reddit = "reddit"
    hackernews = "hackernews"
    github = "github"
    devto = "devto"
    all = "all"


@app.command()
def research(
    topic: str = typer.Argument(..., help="Person, company, product, or topic to research"),
    days: int = typer.Option(30, "--days", "-d", help="Look-back window in days"),
    sources: SourceChoice = typer.Option(
        SourceChoice.all, "--sources", "-s", help="Which sources to query"
    ),
    max_per_source: int = typer.Option(12, "--max", help="Max results per source"),
    min_engagement: float = typer.Option(5.0, "--min-eng", help="Minimum engagement threshold"),
    out_dir: Path = typer.Option(Path("."), "--out", "-o", help="Directory for markdown/html output"),
    open_html: bool = typer.Option(False, "--open", help="Print HTML path (open manually)"),
):
    """
    Run a multi-source engagement-ranked research brief for TOPIC.
    """
    source_list: list[SourceType]
    if sources == SourceChoice.all:
        source_list = [
            SourceType.REDDIT,
            SourceType.HACKERNEWS,
            SourceType.GITHUB,
            SourceType.DEVTO,
        ]
    else:
        source_list = [SourceType(sources.value)]

    plan = ResearchPlan(
        topic=topic,
        days=days,
        sources=source_list,
        max_results_per_source=max_per_source,
        min_engagement=min_engagement,
    )

    console.print(
        Panel.fit(
            f"[bold]Vantage[/] researching [cyan]{topic}[/]\n"
            f"Window: last {days} days · Sources: {', '.join(s.value for s in source_list)}",
            border_style="blue",
        )
    )

    brief = asyncio.run(run_research(plan))
    md_path, html_path = save_brief(brief, out_dir)

    console.print()
    console.print(Markdown(brief.summary))
    console.print()
    console.print(f"[green]Markdown[/] → {md_path}")
    console.print(f"[green]HTML[/]     → {html_path}")
    if open_html:
        console.print(f"Open the HTML file in a browser for the dark-mode brief.")


@app.command()
def version():
    """Show version."""
    from vantage import __version__
    console.print(f"vantage {__version__}")


if __name__ == "__main__":
    app()
