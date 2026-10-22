import unittest

from tvsummary import AverageRating, GenreCounts, Show, TopRated


def sample_shows():
    return [
        Show({"id": 1, "name": "Alpha", "genres": ["Drama"], "rating": {"average": 8}}),
        Show({"id": 2, "name": "Beta", "genres": ["Drama", "Comedy"]}),
        Show({"id": 3, "name": "Gamma", "rating": {"average": 6}}),
    ]


class ShowTests(unittest.TestCase):
    def test_missing_genres_and_rating(self):
        show = Show({"id": 1, "name": "Test"})
        self.assertEqual(show.genres, [])
        self.assertIsNone(show.rating)

    def test_str(self):
        show = Show({"id": 2, "name": "Drama", "rating": {"average": 8.5}})
        self.assertEqual(str(show), "Drama (rated 8.5)")


class AggregationTests(unittest.TestCase):
    def test_average_rating_skips_missing(self):
        self.assertEqual(AverageRating().compute(sample_shows()), 7.0)

    def test_genre_counts(self):
        self.assertEqual(
            GenreCounts().compute(sample_shows()), {"Drama": 2, "Comedy": 1}
        )

    def test_top_rated(self):
        self.assertEqual(TopRated().compute(sample_shows()), ["Alpha", "Gamma"])


if __name__ == "__main__":
    unittest.main()
