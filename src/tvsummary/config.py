"""Settings for the program, kept in one place."""
from pathlib import Path

SOURCE_URL = "https://api.tvmaze.com/shows"
TIMEOUT = 10
OUTPUT_PATH = Path("data") / "processed" / "summary.json"
