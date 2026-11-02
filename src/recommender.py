import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool
    taste_profile: Dict[str, float]  # e.g., {'energy': 0.8, 'valence': 0.5, ...}

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """Read songs from a CSV file into dicts, converting numeric columns to numbers."""
    print(f"Loading songs from {csv_path}...")
    float_fields = ("energy", "tempo_bpm", "valence", "danceability", "acousticness")
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            row["id"] = int(row["id"])
            for field in float_fields:
                row[field] = float(row[field])
            songs.append(row)
    return songs

GENRE_POINTS = 1.0
MOOD_POINTS = 1.5
ENERGY_POINTS = 2.0  # maximum, for a perfect energy match

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score one song against the user's preferences and return (score, reasons)."""
    score = 0.0
    reasons = []

    if "genre" in user_prefs and song["genre"] == user_prefs["genre"]:
        score += GENRE_POINTS
        reasons.append(f"genre match: {song['genre']} (+{GENRE_POINTS:.1f})")

    if "mood" in user_prefs and song["mood"] == user_prefs["mood"]:
        score += MOOD_POINTS
        reasons.append(f"mood match: {song['mood']} (+{MOOD_POINTS:.1f})")

    if "energy" in user_prefs:
        # Closeness to the target, not "higher is better".
        points = ENERGY_POINTS * (1 - abs(song["energy"] - user_prefs["energy"]))
        score += points
        reasons.append(
            f"energy {song['energy']:.2f} vs target {user_prefs['energy']:.2f} (+{points:.2f})"
        )

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score every song, then return the top k as (song, score, explanation), best first."""
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        scored.append((song, score, "; ".join(reasons)))

    # sorted() returns a new list, so the caller's `songs` and `scored` stay untouched.
    # Sorting is stable, so tied scores keep their CSV order.
    ranked = sorted(scored, key=lambda item: item[1], reverse=True)
    return ranked[:k]
