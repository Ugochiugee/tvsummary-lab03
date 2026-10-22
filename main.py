"""Thin entry point: fetch shows, summarize them, write the summary."""
import sys

from tvsummary import TvMazeSource, build_summary, write_summary
from tvsummary.config import OUTPUT_PATH, SOURCE_URL, TIMEOUT


def main():
    """Fetch, summarize and write, with a clear message on failure."""
    try:
        shows = TvMazeSource(SOURCE_URL, TIMEOUT).fetch()
    except RuntimeError as error:
        print(f"Error: {error}.")
        print("Check your internet connection and try again.")
        sys.exit(1)
    summary = build_summary(shows, SOURCE_URL)
    write_summary(summary, OUTPUT_PATH)
    print(f"Wrote a summary of {len(shows)} shows to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
