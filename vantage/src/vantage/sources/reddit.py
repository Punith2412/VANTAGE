"""Reddit search via public JSON endpoints (no API key required)."""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any

import httpx

from vantage.models import ResearchPlan, Signal, SourceType
from vantage.sources.base import BaseSource

logger = logging.getLogger(__name__)

USER_AGENT = (
    "Mozilla/5.0 (compatible; VantageResearch/0.1.0; +https://github.com/punithpatil/vantage) "
    "AppleWebKit/537.36 (KHTML, like Gecko)"
)


class RedditSource(BaseSource):
    source_type = SourceType.REDDIT

    async def search(self) -> list[Signal]:
        signals: list[Signal] = []
        # Two strategies: top of last month + relevance search limited to recent
        queries = [
            {
                "q": self.plan.topic,
                "sort": "top",
                "t": "month" if self.plan.days <= 31 else "year",
                "limit": self.plan.max_results_per_source,
            },
            {
                "q": self.plan.topic,
                "sort": "relevance",
                "t": "month",
                "limit": self.plan.max_results_per_source // 2,
            },
        ]

        async with httpx.AsyncClient(
            headers={"User-Agent": USER_AGENT},
            timeout=20.0,
            follow_redirects=True,
        ) as client:
            for params in queries:
                try:
                    resp = await client.get(
                        "https://www.reddit.com/search.json",
                        params={**params, "type": "link"},
                    )
                    resp.raise_for_status()
                    data = resp.json()
                    children = data.get("data", {}).get("children", [])
                    for child in children:
                        post = child.get("data", {})
                        sig = self._to_signal(post)
                        if sig and sig.engagement >= self.plan.min_engagement:
                            signals.append(sig)
                except Exception as e:
                    logger.warning("Reddit query failed: %s", e)

        # Deduplicate by id
        seen = set()
        unique: list[Signal] = []
        for s in signals:
            if s.id not in seen:
                seen.add(s.id)
                unique.append(s)
        return sorted(unique, key=lambda x: x.engagement, reverse=True)[
            : self.plan.max_results_per_source
        ]

    def _to_signal(self, post: dict[str, Any]) -> Signal | None:
        created = post.get("created_utc")
        published = None
        if created:
            published = datetime.fromtimestamp(created, tz=timezone.utc)
            if not self._within_window(published):
                return None

        score = float(post.get("score") or 0)
        comments = float(post.get("num_comments") or 0)
        # Simple engagement: score + weighted comments
        engagement = score + (comments * 0.3)

        title = (post.get("title") or "").strip()
        if not title:
            return None

        permalink = post.get("permalink") or ""
        url = f"https://www.reddit.com{permalink}" if permalink else post.get("url", "")

        return Signal(
            id=f"reddit:{post.get('id', '')}",
            source=SourceType.REDDIT,
            title=title,
            url=url,
            snippet=(post.get("selftext") or "")[:400],
            author=post.get("author"),
            published_at=published,
            engagement=engagement,
            raw_metrics={"score": score, "comments": comments, "upvote_ratio": post.get("upvote_ratio")},
            subreddit_or_repo=post.get("subreddit"),
        )
