"""Hacker News via Algolia public API (no key required)."""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any

import httpx

from vantage.models import ResearchPlan, Signal, SourceType
from vantage.sources.base import BaseSource

logger = logging.getLogger(__name__)


class HackerNewsSource(BaseSource):
    source_type = SourceType.HACKERNEWS

    async def search(self) -> list[Signal]:
        signals: list[Signal] = []
        cutoff_ts = int(self.cutoff.timestamp())

        params = {
            "query": self.plan.topic,
            "tags": "story",
            "numericFilters": f"created_at_i>{cutoff_ts}",
            "hitsPerPage": self.plan.max_results_per_source * 2,
        }

        async with httpx.AsyncClient(timeout=15.0) as client:
            try:
                resp = await client.get(
                    "https://hn.algolia.com/api/v1/search",
                    params=params,
                )
                resp.raise_for_status()
                data = resp.json()
                for hit in data.get("hits", []):
                    sig = self._to_signal(hit)
                    if sig and sig.engagement >= self.plan.min_engagement:
                        signals.append(sig)
            except Exception as e:
                logger.warning("Hacker News search failed: %s", e)

        return sorted(signals, key=lambda x: x.engagement, reverse=True)[
            : self.plan.max_results_per_source
        ]

    def _to_signal(self, hit: dict[str, Any]) -> Signal | None:
        created = hit.get("created_at")
        published = None
        if created:
            try:
                published = datetime.fromisoformat(created.replace("Z", "+00:00"))
            except Exception:
                pass
        if not self._within_window(published):
            return None

        points = float(hit.get("points") or 0)
        comments = float(hit.get("num_comments") or 0)
        engagement = points + (comments * 0.5)

        title = (hit.get("title") or "").strip()
        if not title:
            return None

        object_id = hit.get("objectID", "")
        url = hit.get("url") or f"https://news.ycombinator.com/item?id={object_id}"

        return Signal(
            id=f"hn:{object_id}",
            source=SourceType.HACKERNEWS,
            title=title,
            url=url,
            snippet=(hit.get("story_text") or hit.get("comment_text") or "")[:400],
            author=hit.get("author"),
            published_at=published,
            engagement=engagement,
            raw_metrics={"points": points, "comments": comments},
            subreddit_or_repo=None,
        )
