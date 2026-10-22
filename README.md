# TV Show Summary

Downloads the first page of shows from the TVMaze API and summarizes them: how many are rated, the average rating, the most common genres and languages, how many shows have each status, and the top rated shows. It gives a quick picture of what the catalogue contains.

## Data source
`https://api.tvmaze.com/shows` returns the first page of the TVMaze catalogue. One record is one TV show, with its name, genres, language, status and rating. The page holds about 240 shows.

## Setup
```
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Run
```
python records.py
```

The summary is written to `data/processed/summary.json`.

## Example output
See `data/processed/summary.json`. It records the source URL, the number of shows processed, how many have a rating and their average, the five most common genres and languages, the count of shows per status, and the five top rated shows.

## Data quirks
- **A show can have several genres, or none.** `shows_per_genre` loops over each show's genre list and counts the show once in each genre. An empty or missing list adds nothing, rather than being counted as a genre such as "None".
- **Some shows have no rating.** The rating is nested as `rating.average` and can be null. `get_rating` returns `None` for those, and they are left out of the average and the top rated list instead of being counted as 0.
- **Some shows have no language or status.** These are skipped in those counts rather than being grouped under an empty label.
- **Records without a name** cannot be reported, so `clean_records` drops them. It also drops a repeated show id so a show is never counted twice.

## Design choices
- **list**: the records arrive as a list, and the top rated shows are an ordered list, because order matters there.
- **dict**: each grouping (genres, languages, statuses) is a dictionary from a label to a count, built with `Counter`, which is a dict subclass. The summary itself is a dict because it maps to a JSON object.
- **set**: `seen_ids` in `clean_records` tracks show ids already kept. Checking membership in a set is fast and the order does not matter.
- **tuple**: `(rating, name)` pairs in `top_rated` and `(count, label)` sort keys. A tuple sorts by its first item, then its second, which breaks ties by name.
- Comprehensions build the rating list in `average_rating`, the rated pairs in `top_rated` and the counts in `shows_per_language` and `shows_per_status`.

## Known limitations
- Only the first page of shows is downloaded, not the whole catalogue.
- TVMaze can add or edit shows, so the numbers may change between runs.
