"""Summarize TV shows from the TVMaze API."""

from tvsummary.aggregations import (
    Aggregation,
    AverageRating,
    GenreCounts,
    LanguageCounts,
    RatedCount,
    ShowCount,
    StatusCounts,
    TopRated,
)
from tvsummary.models import Show
from tvsummary.report import build_summary, write_summary
from tvsummary.sources import TvMazeSource

__all__ = [
    "Aggregation",
    "AverageRating",
    "GenreCounts",
    "LanguageCounts",
    "RatedCount",
    "Show",
    "ShowCount",
    "StatusCounts",
    "TopRated",
    "TvMazeSource",
    "build_summary",
    "write_summary",
]
