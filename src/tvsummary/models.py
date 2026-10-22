"""The record class: one TV show."""


class Show:
    """One TV show from TVMaze, with its values cleaned when it is created."""

    def __init__(self, data):
        self.id = int(data.get("id") or 0)
        name = data.get("name")
        self.name = name.strip() if isinstance(name, str) and name.strip() else "Unknown"
        genres = data.get("genres")
        if isinstance(genres, list):
            self.genres = [g for g in genres if isinstance(g, str) and g]
        else:
            self.genres = []
        rating = data.get("rating")
        average = rating.get("average") if isinstance(rating, dict) else None
        self.rating = float(average) if isinstance(average, (int, float)) else None
        language = data.get("language")
        self.language = language if isinstance(language, str) and language else None
        status = data.get("status")
        self.status = status if isinstance(status, str) and status else None

    def __str__(self):
        rating = "no rating" if self.rating is None else f"rated {self.rating}"
        return f"{self.name} ({rating})"
