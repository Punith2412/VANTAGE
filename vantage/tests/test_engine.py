"""Tests for ranking, diversification, and summary generation in the engine."""

from datetime import datetime, timedelta, timezone
from unittest.mock import AsyncMock, patch

import pytest

from vantage.engine import _template_summary, run_research
from vantage.models import ResearchPlan, Signal, SourceType


def _make_signal(
    id_: str,
    source: SourceType,
    title: str,
    engagement: float,
    author: str | None = None,
    days_ago: int = 5,
) -> Signal:
    return Signal(
        id=id_,
        source=source,
        title=title,
        url=f"https://example.com/{id_}",
        author=author or id_,
        published_at=datetime.now(timezone.utc) - timedelta(days=days_ago),
        engagement=engagement,
        raw_metrics={"score": engagement},
    )


class TestTemplateSummary:
    def test_empty_signals(self):
        summary, themes = _template_summary("obscure topic", [])
        assert "No strong engagement signals" in summary
        assert themes == []

    def test_with_signals_and_themes(self):
        signals = [
            _make_signal("1", SourceType.REDDIT, "New open source LLM release", 200),
            _make_signal("2", SourceType.HACKERNEWS, "AI performance benchmarks", 150),
            _make_signal("3", SourceType.GITHUB, "security fix for the API", 80),
        ]
        summary, themes = _template_summary("LLM tools", signals)
        assert "LLM tools" in summary
        assert "Top signals by engagement" in summary
        assert any(t in ("ai", "llm", "open source", "performance", "security", "api") for t in themes)
        assert len(themes) <= 6


class TestRankingAndDiversification:
    @pytest.mark.asyncio
    async def test_run_research_ranks_by_engagement(self):
        plan = ResearchPlan(topic="test", sources=[SourceType.HACKERNEWS], max_results_per_source=10)

        low = _make_signal("low", SourceType.HACKERNEWS, "Low engagement", 10, days_ago=2)
        high = _make_signal("high", SourceType.HACKERNEWS, "High engagement", 500, days_ago=10)
        mid = _make_signal("mid", SourceType.HACKERNEWS, "Mid engagement", 100, days_ago=1)

        mock_source = AsyncMock()
        mock_source.source_type = SourceType.HACKERNEWS
        mock_source.search = AsyncMock(return_value=[low, high, mid])

        with patch("vantage.engine.SOURCE_MAP", {SourceType.HACKERNEWS: lambda p: mock_source}):
            brief = await run_research(plan)

        assert brief.total_signals == 3
        assert brief.top_signals[0].id == "high"
        assert brief.top_signals[0].engagement == 500
        assert len(brief.top_signals) == 3

    @pytest.mark.asyncio
    async def test_author_diversification_cap(self):
        plan = ResearchPlan(topic="test", sources=[SourceType.REDDIT])

        # Same author produces 5 high-engagement posts – only 3 should survive
        same_author_signals = [
            _make_signal(f"s{i}", SourceType.REDDIT, f"Post {i}", 1000 - i, author="poweruser")
            for i in range(5)
        ]
        other = _make_signal("other", SourceType.REDDIT, "Different voice", 50, author="someoneelse")

        mock_source = AsyncMock()
        mock_source.source_type = SourceType.REDDIT
        mock_source.search = AsyncMock(return_value=same_author_signals + [other])

        with patch("vantage.engine.SOURCE_MAP", {SourceType.REDDIT: lambda p: mock_source}):
            brief = await run_research(plan)

        authors = [s.author for s in brief.top_signals]
        assert authors.count("poweruser") <= 3
        assert "someoneelse" in authors

    @pytest.mark.asyncio
    async def test_source_failure_is_graceful(self):
        plan = ResearchPlan(topic="test", sources=[SourceType.REDDIT, SourceType.HACKERNEWS])

        good = _make_signal("ok", SourceType.HACKERNEWS, "Works", 42)

        failing = AsyncMock()
        failing.source_type = SourceType.REDDIT
        failing.search = AsyncMock(side_effect=RuntimeError("403 Forbidden"))

        working = AsyncMock()
        working.source_type = SourceType.HACKERNEWS
        working.search = AsyncMock(return_value=[good])

        with patch(
            "vantage.engine.SOURCE_MAP",
            {
                SourceType.REDDIT: lambda p: failing,
                SourceType.HACKERNEWS: lambda p: working,
            },
        ):
            brief = await run_research(plan)

        assert brief.total_signals == 1
        assert brief.top_signals[0].id == "ok"
