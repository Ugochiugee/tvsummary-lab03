"""Build the summary and write it to disk."""
import json

from tvsummary.aggregations import (
    AverageRating,
    GenreCounts,
    LanguageCounts,
    RatedCount,
    ShowCount,
    StatusCounts,
    TopRated,
)


def default_aggregations():
    """The aggregations that make up the summary, in output order."""
    return [
        ShowCount(),
        RatedCount(),
        AverageRating(),
        GenreCounts(),
        LanguageCounts(),
        StatusCounts(),
        TopRated(),
    ]


def build_summary(shows, source_url, aggregations=None):
    """Run each aggregation and combine the results with the source URL."""
    aggregations = aggregations or default_aggregations()
    summary = {"source_url": source_url}
    summary.update({agg.key: agg.compute(shows) for agg in aggregations})
    return summary


def write_summary(summary, path):
    """Write the summary to a JSON file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
