"""Source-level unit tests with mocked HTTP – no network required."""

from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from vantage.models import ResearchPlan, SourceType
from vantage.sources.base import BaseSource
from vantage.sources.devto import DevToSource
from vantage.sources.github import GitHubSource
from vantage.sources.hackernews import HackerNewsSource
from vantage.sources.reddit import RedditSource


@pytest.fixture
def plan() -> ResearchPlan:
    return ResearchPlan(
        topic="pytest",
        days=30,
        max_results_per_source=5,
        min_engagement=1.0,
    )


class TestBaseSource:
    def test_cutoff_calculation(self, plan):
        class Dummy(BaseSource):
            source_type = SourceType.REDDIT

            async def search(self):
                return []

        src = Dummy(plan)
        assert src.cutoff < datetime.now(timezone.utc)
        assert (datetime.now(timezone.utc) - src.cutoff).days >= 29

    def test_within_window_none_date(self, plan):
        class Dummy(BaseSource):
            source_type = SourceType.REDDIT

            async def search(self):
                return []

        src = Dummy(plan)
        assert src._within_window(None) is True


class TestRedditSource:
    @pytest.mark.asyncio
    async def test_parses_mock_response(self, plan):
        mock_json = {
            "data": {
                "children": [
                    {
                        "data": {
                            "id": "abc",
                            "title": "How we use pytest at scale",
                            "url": "https://reddit.com/r/Python/comments/abc",
                            "permalink": "/r/Python/comments/abc",
                            "selftext": "Long post about fixtures…",
                            "author": "tester",
                            "score": 250,
                            "num_comments": 40,
                            "created_utc": datetime.now(timezone.utc).timestamp() - 86400,
                            "subreddit": "Python",
                        }
                    }
                ]
            }
        }

        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = mock_json
        mock_resp.raise_for_status = MagicMock()

        with patch("httpx.AsyncClient") as client_cls:
            client = AsyncMock()
            client.__aenter__.return_value = client
            client.get = AsyncMock(return_value=mock_resp)
            client_cls.return_value = client

            src = RedditSource(plan)
            signals = await src.search()

        assert len(signals) >= 1
        s = signals[0]
        assert s.source == "reddit"
        assert "pytest" in s.title.lower() or "pytest" in plan.topic.lower()
        assert s.engagement > 0
        assert "score" in s.raw_metrics or s.engagement > 0


class TestHackerNewsSource:
    @pytest.mark.asyncio
    async def test_empty_hits(self, plan):
        mock_json = {"hits": []}

        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = mock_json
        mock_resp.raise_for_status = MagicMock()

        with patch("httpx.AsyncClient") as client_cls:
            client = AsyncMock()
            client.__aenter__.return_value = client
            client.get = AsyncMock(return_value=mock_resp)
            client_cls.return_value = client

            src = HackerNewsSource(plan)
            signals = await src.search()

        assert signals == []


class TestGitHubSource:
    @pytest.mark.asyncio
    async def test_parses_repo_items(self, plan):
        mock_json = {
            "items": [
                {
                    "id": 123,
                    "full_name": "pytest-dev/pytest",
                    "html_url": "https://github.com/pytest-dev/pytest",
                    "description": "The pytest framework",
                    "stargazers_count": 12000,
                    "forks_count": 2500,
                    "updated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
                    "owner": {"login": "pytest-dev"},
                }
            ]
        }

        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = mock_json
        mock_resp.raise_for_status = MagicMock()

        with patch("httpx.AsyncClient") as client_cls:
            client = AsyncMock()
            client.__aenter__.return_value = client
            client.get = AsyncMock(return_value=mock_resp)
            client_cls.return_value = client

            src = GitHubSource(plan)
            signals = await src.search()

        assert len(signals) == 1
        assert signals[0].source == "github"
        assert signals[0].engagement > 0
        assert "stars" in signals[0].raw_metrics or signals[0].engagement > 1000


class TestDevToSource:
    @pytest.mark.asyncio
    async def test_parses_articles(self, plan):
        mock_json = [
            {
                "id": 99,
                "title": "Writing better pytest fixtures",
                "url": "https://dev.to/author/writing-better-pytest-fixtures",
                "description": "Tips for maintainable tests",
                "user": {"username": "qa_writer"},
                "positive_reactions_count": 80,
                "comments_count": 12,
                "published_at": datetime.now(timezone.utc).isoformat(),
                "tag_list": ["python", "testing"],
            }
        ]

        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = mock_json
        mock_resp.raise_for_status = MagicMock()

        with patch("httpx.AsyncClient") as client_cls:
            client = AsyncMock()
            client.__aenter__.return_value = client
            client.get = AsyncMock(return_value=mock_resp)
            client_cls.return_value = client

            src = DevToSource(plan)
            signals = await src.search()

        assert len(signals) == 1
        assert signals[0].source == "devto"
        assert signals[0].engagement > 0
