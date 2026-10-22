# TV Summary

An installable package that downloads the first page of shows from the TVMaze API and summarizes them: how many are rated, the average rating, the most common genres and languages, status counts and the top rated shows.

## Data source
`https://api.tvmaze.com/shows` returns the first page of the TVMaze catalogue. One record is one TV show. The page holds about 240 shows.

## Setup
```
conda env create -f environment.yml
conda activate tvsummary
pip install -r requirements.txt
pip install -e .
```

## Run
```
python main.py
```

The summary is written to `data/processed/summary.json`.

## Test
```
python -m unittest discover -s tests
```

## Layout
- `main.py`: thin entry point. Wires the pieces together and prints the result or the error message.
- `src/tvsummary/config.py`: the source URL, timeout and output path, so settings live in one place.
- `src/tvsummary/models.py`: the `Show` record class, so cleaning of one record happens in one place.
- `src/tvsummary/sources.py`: `TvMazeSource`, the only module that imports `requests`, so network code is kept apart from the logic.
- `src/tvsummary/aggregations.py`: the `Aggregation` base class and one subclass per result in the summary.
- `src/tvsummary/report.py`: builds the summary from a list of aggregations and writes it to JSON.
- `tests/test_models.py`: unittest tests on hand-made shows, with no network.

## What moved where

| Lab 02 function (records.py) | Where it lives now |
|---|---|
| `fetch_records` | `sources.TvMazeSource.fetch` |
| `clean_records` | `sources.TvMazeSource.fetch` (skips records with no name and repeated ids) |
| `get_rating` | `models.Show.__init__` (sets `show.rating`) |
| `top_counts` | the sorting inside `GenreCounts.compute` and `LanguageCounts.compute` |
| `count_rated` | `aggregations.RatedCount.compute` |
| `average_rating` | `aggregations.AverageRating.compute` |
| `shows_per_genre` | `aggregations.GenreCounts.compute` |
| `shows_per_language` | `aggregations.LanguageCounts.compute` |
| `shows_per_status` | `aggregations.StatusCounts.compute` |
| `top_rated` | `aggregations.TopRated.compute` |
| `len(records)` in `build_summary` | `aggregations.ShowCount.compute` |
| `build_summary` | `report.build_summary` |
| `write_summary` | `report.write_summary` |
| `main` | `main.py` `main()` |
| `SOURCE_URL`, `TIMEOUT`, `OUTPUT` | `config.py` |

## Design choices
- **Show** exists so that every check for missing or malformed values (no genres, no rating, an empty name, a blank language) happens once, when the record is created. The aggregations can then trust that `show.genres` is a list and `show.rating` is a float or `None`.
- **TvMazeSource** exists so that downloading is in one class. It turns raw dicts into `Show` objects and turns any request or JSON failure into one `RuntimeError` with a clear message, so `main.py` never sees a `requests` exception.
- **Aggregation** is the base class. It holds the summary key and `top_n`, and defines `compute`. Each subclass overrides `compute`. `report.build_summary` loops over a list of aggregation objects and calls `compute` on each without checking which subclass it is.
- **Adding one more aggregation** means writing a subclass with a `key` and a `compute` method, and adding an instance to `default_aggregations()` in `report.py`. Nothing else changes.

## Known limitations
- Only the first page of shows is downloaded.
- TVMaze can add or edit shows, so the numbers may change between runs.
- Tests cover the record class and three aggregations only. A fuller suite is planned for Lab 04.
