"""Abstract base for all research sources."""

from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime, timedelta, timezone

from vantage.models import ResearchPlan, Signal, SourceType


class BaseSource(ABC):
    source_type: SourceType

    def __init__(self, plan: ResearchPlan):
        self.plan = plan
        self.cutoff = datetime.now(timezone.utc) - timedelta(days=plan.days)

    @abstractmethod
    async def search(self) -> list[Signal]:
        """Return signals for the plan.topic within the time window."""
        ...

    def _within_window(self, dt: datetime | None) -> bool:
        if dt is None:
            return True  # keep if no date
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt >= self.cutoff
