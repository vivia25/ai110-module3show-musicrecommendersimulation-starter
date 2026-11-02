"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import (
    ENERGY_POINTS,
    GENRE_POINTS,
    MOOD_POINTS,
    load_songs,
    recommend_songs,
)

MAX_SCORE = GENRE_POINTS + MOOD_POINTS + ENERGY_POINTS


PROFILES = {
    # Typical listeners
    "High-Energy Pop": {"genre": "pop", "mood": "happy", "energy": 0.9},
    "Chill Lofi": {"genre": "lofi", "mood": "chill", "energy": 0.4},
    "Deep Intense Rock": {"genre": "rock", "mood": "intense", "energy": 0.92},
    # Adversarial / edge cases
    "Conflicting: sad but energetic": {"genre": "folk", "mood": "sad", "energy": 0.9},
    "Unknown tastes (no label matches)": {"genre": "k-pop", "mood": "dreamy", "energy": 0.6},
    "Mismatched genre vs mood": {"genre": "classical", "mood": "aggressive", "energy": 0.2},
}


def print_recommendations(name: str, user_prefs: dict, songs: list) -> None:
    recommendations = recommend_songs(user_prefs, songs, k=5)

    width = 60
    print("\n" + "=" * width)
    print(f" PROFILE: {name}")
    print(" " + ", ".join(f"{key}={value}" for key, value in user_prefs.items()))
    print("=" * width)

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n{rank}. {song['title']} - {song['artist']} ({song['genre']}, {song['mood']})")
        print(f"   Score: {score:.2f} / {MAX_SCORE:.2f}")
        print("   Why:")
        for reason in explanation.split("; "):
            print(f"     * {reason}")

    print("\n" + "=" * width)


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    for name, user_prefs in PROFILES.items():
        print_recommendations(name, user_prefs, songs)


if __name__ == "__main__":
    main()
