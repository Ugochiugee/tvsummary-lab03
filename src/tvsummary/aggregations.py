"""Aggregations over a list of shows. Each subclass overrides compute."""
from collections import Counter


class Aggregation:
    """Base class. key is the name of the result in the summary."""

    key = "aggregation"

    def __init__(self, top_n=5):
        self.top_n = top_n

    def compute(self, shows):
        """Return the result for a list of Show objects."""
        raise NotImplementedError


class ShowCount(Aggregation):
    """How many shows there are."""

    key = "total_shows"

    def compute(self, shows):
        return len(shows)


class RatedCount(Aggregation):
    """How many shows have a rating."""

    key = "shows_with_rating"

    def compute(self, shows):
        return sum(1 for show in shows if show.rating is not None)


class AverageRating(Aggregation):
    """Mean rating of the rated shows, to two decimals."""

    key = "average_rating"

    def compute(self, shows):
        ratings = [show.rating for show in shows if show.rating is not None]
        if not ratings:
            return None
        return round(sum(ratings) / len(ratings), 2)


class GenreCounts(Aggregation):
    """The most common genres."""

    key = "top_genres"

    def compute(self, shows):
        counts = Counter(genre for show in shows for genre in show.genres)
        return dict(sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))[: self.top_n])


class LanguageCounts(Aggregation):
    """The most common languages."""

    key = "top_languages"

    def compute(self, shows):
        counts = Counter(show.language for show in shows if show.language)
        return dict(sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))[: self.top_n])


class StatusCounts(Aggregation):
    """How many shows have each status."""

    key = "status_counts"

    def compute(self, shows):
        counts = Counter(show.status for show in shows if show.status)
        return dict(sorted(counts.items()))


class TopRated(Aggregation):
    """Names of the highest rated shows."""

    key = "top_rated_shows"

    def compute(self, shows):
        rated = [show for show in shows if show.rating is not None]
        rated.sort(key=lambda show: (-show.rating, show.name))
        return [show.name for show in rated[: self.top_n]]
