"""Download shows from TVMaze. The only module that uses requests."""
import requests

from tvsummary.models import Show


class TvMazeSource:
    """Fetches the list of shows and turns it into Show objects."""

    def __init__(self, url, timeout):
        self.url = url
        self.timeout = timeout

    def fetch(self):
        """Download the shows and return them as Show objects."""
        try:
            response = requests.get(self.url, timeout=self.timeout)
            response.raise_for_status()
            data = response.json()
        except (requests.RequestException, ValueError) as error:
            raise RuntimeError(f"Could not download shows from {self.url}") from error
        if not isinstance(data, list):
            raise RuntimeError(f"Expected a list of shows from {self.url}")
        shows = []
        seen_ids = set()
        for item in data:
            if not isinstance(item, dict) or not item.get("name"):
                continue
            if item.get("id") in seen_ids:
                continue
            seen_ids.add(item.get("id"))
            shows.append(Show(item))
        return shows
