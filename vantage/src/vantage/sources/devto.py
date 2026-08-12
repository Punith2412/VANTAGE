"""Dev.to article search via public API (no key required)."""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any
from urllib.parse import quote

import httpx

from vantage.models import ResearchPlan, Signal, SourceType
from vantage.sources.base import BaseSource

logger = logging.getLogger(__name__)

USER_AGENT = (
    "Mozilla/5.0 (compatible; VantageResearch/0.1.0; +https://github.com/punithpatil/vantage) "
    "AppleWebKit/537.36"
)


class DevToSource(BaseSource):
    source_type = SourceType.DEVTO

    async def search(self) -> list[Signal]:
        signals: list[Signal] = []
        # Dev.to supports tag or free-text q. Prefer q for general topics.
        params = {
            "per_page": min(self.plan.max_results_per_source * 2, 30),
            "q": self.plan.topic,
        }

        async with httpx.AsyncClient(
            headers={"User-Agent": USER_AGENT, "Accept": "application/json"},
            timeout=15.0,
        ) as client:
            try:
                resp = await client.get("https://dev.to/api/articles", params=params)
                resp.raise_for_status()
                articles = resp.json()
                for art in articles:
                    sig = self._to_signal(art)
                    if sig and sig.engagement >= self.plan.min_engagement:
                        signals.append(sig)
            except Exception as e:
                logger.warning("Dev.to search failed: %s", e)

        return sorted(signals, key=lambda x: x.engagement, reverse=True)[
            : self.plan.max_results_per_source
        ]

    def _to_signal(self, art: dict[str, Any]) -> Signal | None:
        published = None
        ts = art.get("published_at") or art.get("created_at")
        if ts:
            try:
                published = datetime.fromisoformat(ts.replace("Z", "+00:00"))
            except Exception:
                pass
        if not self._within_window(published):
            return None

        reactions = float(art.get("public_reactions_count") or art.get("positive_reactions_count") or 0)
        comments = float(art.get("comments_count") or 0)
        engagement = reactions + (comments * 0.4)

        title = (art.get("title") or "").strip()
        if not title:
            return None

        url = art.get("url") or art.get("canonical_url") or ""
        tags = art.get("tag_list") or art.get("tags") or []
        if isinstance(tags, str):
            tags = [t.strip() for t in tags.split(",") if t.strip()]

        return Signal(
            id=f"devto:{art.get('id', '')}",
            source=SourceType.DEVTO,
            title=title,
            url=url,
            snippet=(art.get("description") or "")[:400],
            author=(art.get("user") or {}).get("username") or (art.get("user") or {}).get("name"),
            published_at=published,
            engagement=engagement,
            raw_metrics={
                "reactions": reactions,
                "comments": comments,
                "reading_time": art.get("reading_time_minutes"),
            },
            subreddit_or_repo=", ".join(tags[:4]) if tags else None,
        )
