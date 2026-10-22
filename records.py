"""Download TV shows from TVMaze, summarize them, and write summary.json."""

import json
import sys
from collections import Counter
from pathlib import Path

import requests

SOURCE_URL = "https://api.tvmaze.com/shows"
TIMEOUT = 10
OUTPUT = Path("data") / "processed" / "summary.json"
TOP_N = 5


def fetch_records(url, timeout=TIMEOUT):
    """Download the shows and return them as a list of dicts."""
    response = requests.get(url, timeout=timeout)
    response.raise_for_status()
    data = response.json()
    if not isinstance(data, list):
        raise ValueError("expected a list of shows")
    return data


def clean_records(records):
    """Keep records that have a name, dropping repeated show ids."""
    seen_ids = set()
    cleaned = []
    for record in records:
        if not isinstance(record, dict) or not record.get("name"):
            continue
        if record.get("id") in seen_ids:
            continue
        seen_ids.add(record.get("id"))
        cleaned.append(record)
    return cleaned


def get_rating(record):
    """Return the average rating as a float, or None if it is missing."""
    rating = record.get("rating")
    average = rating.get("average") if isinstance(rating, dict) else None
    return float(average) if isinstance(average, (int, float)) else None


def top_counts(counts, top_n=TOP_N):
    """The top_n entries of a Counter, ties broken by name."""
    ranked = sorted(counts.items(), key=lambda pair: (-pair[1], pair[0]))
    return dict(ranked[:top_n])


def count_rated(records):
    """How many shows have a rating."""
    return sum(1 for record in records if get_rating(record) is not None)


def average_rating(records):
    """Mean rating of the rated shows, to two decimals, or None."""
    ratings = [r for r in (get_rating(record) for record in records) if r is not None]
    if not ratings:
        return None
    return round(sum(ratings) / len(ratings), 2)


def shows_per_genre(records):
    """The most common genres. A show with several genres counts once in each."""
    counts = Counter()
    for record in records:
        genres = record.get("genres")
        if not isinstance(genres, list):
            continue
        for genre in genres:
            if isinstance(genre, str) and genre:
                counts[genre] += 1
    return top_counts(counts)


def shows_per_language(records):
    """The most common languages, skipping shows with no language."""
    counts = Counter(
        record["language"]
        for record in records
        if isinstance(record.get("language"), str) and record["language"]
    )
    return top_counts(counts)


def shows_per_status(records):
    """How many shows have each status, such as Ended or Running."""
    counts = Counter(
        record["status"]
        for record in records
        if isinstance(record.get("status"), str) and record["status"]
    )
    return dict(sorted(counts.items()))


def top_rated(records, top_n=TOP_N):
    """Names of the highest rated shows."""
    rated = [
        (get_rating(record), record["name"].strip())
        for record in records
        if get_rating(record) is not None
    ]
    rated.sort(key=lambda pair: (-pair[0], pair[1]))
    return [name for _, name in rated[:top_n]]


def build_summary(records, url):
    """Combine the aggregations into one dict ready to write."""
    return {
        "source_url": url,
        "total_shows": len(records),
        "shows_with_rating": count_rated(records),
        "average_rating": average_rating(records),
        "top_genres": shows_per_genre(records),
        "top_languages": shows_per_language(records),
        "status_counts": shows_per_status(records),
        "top_rated_shows": top_rated(records),
    }


def write_summary(summary, path):
    """Write the summary to a JSON file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")


def main():
    """Fetch, summarize and write, with a clear message if the download fails."""
    try:
        raw = fetch_records(SOURCE_URL)
    except (requests.RequestException, ValueError) as error:
        print(f"Error: could not download shows from {SOURCE_URL} ({error}).")
        print("Check your internet connection and try again.")
        sys.exit(1)
    records = clean_records(raw)
    summary = build_summary(records, SOURCE_URL)
    write_summary(summary, OUTPUT)
    print(f"Wrote a summary of {len(records)} shows to {OUTPUT}")


if __name__ == "__main__":
    main()
