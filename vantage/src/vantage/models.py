"""Shared data models for Vantage research results."""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class SourceType(str, Enum):
    REDDIT = "reddit"
    HACKERNEWS = "hackernews"
    GITHUB = "github"
    DEVTO = "devto"
    YOUTUBE = "youtube"  # reserved for future
    X = "x"  # reserved


class Signal(BaseModel):
    """A single engagement signal from any source."""

    model_config = ConfigDict(use_enum_values=True)

    id: str
    source: SourceType
    title: str
    url: str
    snippet: str = ""
    author: Optional[str] = None
    published_at: Optional[datetime] = None
    engagement: float = Field(
        default=0.0,
        description="Normalized engagement score (upvotes, points, stars, etc.)",
    )
    raw_metrics: dict = Field(default_factory=dict)
    subreddit_or_repo: Optional[str] = None


class ResearchPlan(BaseModel):
    """What the user asked for."""

    topic: str
    days: int = 30
    sources: list[SourceType] = Field(
        default_factory=lambda: [
            SourceType.REDDIT,
            SourceType.HACKERNEWS,
            SourceType.GITHUB,
            SourceType.DEVTO,
        ]
    )
    max_results_per_source: int = 15
    min_engagement: float = 5.0


class ResearchBrief(BaseModel):
    """Final synthesized output."""

    topic: str
    generated_at: datetime
    days_covered: int
    total_signals: int
    top_signals: list[Signal]
    summary: str
    key_themes: list[str] = Field(default_factory=list)
    sources_queried: list[str] = Field(default_factory=list)
    html_path: Optional[str] = None
    markdown_path: Optional[str] = None
