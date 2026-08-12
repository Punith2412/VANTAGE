"""Unit tests for Pydantic models – schema validation, defaults, and edge cases."""

from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from vantage.models import ResearchBrief, ResearchPlan, Signal, SourceType


class TestSignal:
    def test_minimal_creation(self):
        s = Signal(
            id="reddit:abc123",
            source=SourceType.REDDIT,
            title="Test post",
            url="https://reddit.com/r/test/comments/abc",
        )
        assert s.source == "reddit"
        assert s.engagement == 0.0
        assert s.snippet == ""
        assert s.author is None
        assert s.raw_metrics == {}

    def test_full_creation(self):
        now = datetime.now(timezone.utc)
        s = Signal(
            id="hn:42",
            source=SourceType.HACKERNEWS,
            title="Show HN: Something cool",
            url="https://news.ycombinator.com/item?id=42",
            snippet="A short description",
            author="pg",
            published_at=now,
            engagement=128.5,
            raw_metrics={"points": 100, "comments": 57},
            subreddit_or_repo=None,
        )
        assert s.engagement == 128.5
        assert s.raw_metrics["points"] == 100
        assert s.published_at == now

    def test_source_enum_values(self):
        for st in SourceType:
            s = Signal(id=f"{st.value}:1", source=st, title="t", url="https://x.com")
            assert s.source == st.value

    def test_missing_required_fields(self):
        with pytest.raises(ValidationError):
            Signal(id="x", source=SourceType.REDDIT)  # missing title & url


class TestResearchPlan:
    def test_defaults(self):
        p = ResearchPlan(topic="Cursor AI")
        assert p.days == 30
        assert p.max_results_per_source == 15
        assert p.min_engagement == 5.0
        assert SourceType.REDDIT in p.sources
        assert SourceType.HACKERNEWS in p.sources
        assert SourceType.GITHUB in p.sources
        assert SourceType.DEVTO in p.sources

    def test_custom_sources(self):
        p = ResearchPlan(
            topic="LLM evals",
            days=7,
            sources=[SourceType.HACKERNEWS, SourceType.GITHUB],
            max_results_per_source=5,
            min_engagement=10.0,
        )
        assert p.days == 7
        assert len(p.sources) == 2
        assert p.min_engagement == 10.0

    def test_empty_topic_allowed_by_model(self):
        # Model itself does not forbid empty topic; CLI should guard it.
        p = ResearchPlan(topic="")
        assert p.topic == ""


class TestResearchBrief:
    def test_brief_creation(self):
        now = datetime.now(timezone.utc)
        brief = ResearchBrief(
            topic="test topic",
            generated_at=now,
            days_covered=14,
            total_signals=3,
            top_signals=[],
            summary="No strong signals.",
            key_themes=["ai"],
            sources_queried=["reddit", "hackernews"],
        )
        assert brief.total_signals == 3
        assert brief.key_themes == ["ai"]
        assert brief.html_path is None
        assert brief.markdown_path is None
