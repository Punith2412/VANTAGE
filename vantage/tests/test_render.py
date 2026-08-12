"""Tests for Markdown / HTML rendering and file output."""

from datetime import datetime, timezone
from pathlib import Path

import pytest

from vantage.models import ResearchBrief, Signal, SourceType
from vantage.render import save_brief, to_html, to_markdown


@pytest.fixture
def sample_brief() -> ResearchBrief:
    now = datetime(2026, 8, 12, 12, 0, 0, tzinfo=timezone.utc)
    signals = [
        Signal(
            id="reddit:1",
            source=SourceType.REDDIT,
            title="Great discussion about testing",
            url="https://reddit.com/r/QualityAssurance/1",
            snippet="How we improved coverage…",
            author="qa_lead",
            published_at=now,
            engagement=120.0,
            raw_metrics={"score": 100, "comments": 40},
            subreddit_or_repo="r/QualityAssurance",
        ),
        Signal(
            id="hn:2",
            source=SourceType.HACKERNEWS,
            title="Show HN: Open-source test runner",
            url="https://news.ycombinator.com/item?id=2",
            engagement=85.0,
            raw_metrics={"points": 70, "comments": 30},
        ),
    ]
    return ResearchBrief(
        topic="software testing practices",
        generated_at=now,
        days_covered=30,
        total_signals=2,
        top_signals=signals,
        summary="Community is talking about coverage and open-source runners.",
        key_themes=["testing", "coverage"],
        sources_queried=["reddit", "hackernews"],
    )


class TestMarkdown:
    def test_contains_title_and_signals(self, sample_brief):
        md = to_markdown(sample_brief)
        assert "# Vantage Brief: software testing practices" in md
        assert "Great discussion about testing" in md
        assert "Show HN: Open-source test runner" in md
        assert "testing" in md
        assert "coverage" in md

    def test_empty_themes_ok(self, sample_brief):
        sample_brief.key_themes = []
        md = to_markdown(sample_brief)
        assert "## Themes" not in md


class TestHTML:
    def test_dark_mode_structure(self, sample_brief):
        html = to_html(sample_brief)
        assert "<!DOCTYPE html>" in html
        assert "software testing practices" in html
        assert "--bg: #0d1117" in html  # dark theme
        assert "engagement 120" in html
        assert "r/QualityAssurance" in html

    def test_themes_rendered(self, sample_brief):
        html = to_html(sample_brief)
        assert "Themes" in html
        assert "testing" in html


class TestSaveBrief:
    def test_writes_both_files(self, sample_brief, tmp_path: Path):
        md_path, html_path = save_brief(sample_brief, tmp_path)
        assert md_path.exists()
        assert html_path.exists()
        assert md_path.suffix == ".md"
        assert html_path.suffix == ".html"
        assert "software-testing-practices" in md_path.name
        content = md_path.read_text(encoding="utf-8")
        assert "Vantage Brief" in content

    def test_paths_attached_to_brief(self, sample_brief, tmp_path: Path):
        md_path, html_path = save_brief(sample_brief, tmp_path)
        assert sample_brief.markdown_path == str(md_path)
        assert sample_brief.html_path == str(html_path)
