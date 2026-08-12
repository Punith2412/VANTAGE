"""GitHub repository + issue search via public REST API (unauthenticated rate limit applies)."""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any

import httpx

from vantage.models import ResearchPlan, Signal, SourceType
from vantage.sources.base import BaseSource

logger = logging.getLogger(__name__)

USER_AGENT = "VantageResearch/0.1.0 (+https://github.com/punithpatil/vantage)"


class GitHubSource(BaseSource):
    source_type = SourceType.GITHUB

    async def search(self) -> list[Signal]:
        signals: list[Signal] = []
        # Search recent repos that mention the topic
        date_str = self.cutoff.strftime("%Y-%m-%d")
        query = f"{self.plan.topic} created:>{date_str}"

        headers = {
            "Accept": "application/vnd.github+json",
            "User-Agent": USER_AGENT,
            "X-GitHub-Api-Version": "2022-11-28",
        }

        async with httpx.AsyncClient(headers=headers, timeout=20.0) as client:
            try:
                resp = await client.get(
                    "https://api.github.com/search/repositories",
                    params={
                        "q": query,
                        "sort": "stars",
                        "order": "desc",
                        "per_page": min(self.plan.max_results_per_source, 30),
                    },
                )
                if resp.status_code == 403:
                    logger.warning("GitHub rate limited (unauthenticated). Skipping.")
                    return []
                resp.raise_for_status()
                data = resp.json()
                for item in data.get("items", []):
                    sig = self._repo_to_signal(item)
                    if sig:
                        signals.append(sig)
            except Exception as e:
                logger.warning("GitHub search failed: %s", e)

        return sorted(signals, key=lambda x: x.engagement, reverse=True)[
            : self.plan.max_results_per_source
        ]

    def _repo_to_signal(self, repo: dict[str, Any]) -> Signal | None:
        created = repo.get("created_at")
        published = None
        if created:
            try:
                published = datetime.fromisoformat(created.replace("Z", "+00:00"))
            except Exception:
                pass
        if not self._within_window(published):
            return None

        stars = float(repo.get("stargazers_count") or 0)
        forks = float(repo.get("forks_count") or 0)
        engagement = stars + (forks * 0.4)

        if engagement < self.plan.min_engagement:
            return None

        full_name = repo.get("full_name") or ""
        return Signal(
            id=f"github:{repo.get('id')}",
            source=SourceType.GITHUB,
            title=full_name or (repo.get("name") or "unknown"),
            url=repo.get("html_url") or "",
            snippet=(repo.get("description") or "")[:400],
            author=repo.get("owner", {}).get("login"),
            published_at=published,
            engagement=engagement,
            raw_metrics={
                "stars": stars,
                "forks": forks,
                "language": repo.get("language"),
                "open_issues": repo.get("open_issues_count"),
            },
            subreddit_or_repo=full_name,
        )
