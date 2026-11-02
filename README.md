# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

This is a content-based recommender: it compares each song's attributes to what the user says they like, and never looks at other users.

### Features and profile

- **`Song`** (19 songs in `data/songs.csv`): `genre`, `mood`, `energy`, `tempo_bpm`, `valence`, `danceability`, `acousticness`. Only `genre`, `mood`, and `energy` are scored in this version. The rest are loaded for later experiments.
- **`UserProfile`** stores a favorite genre, a favorite mood, and a target energy (0 to 1). Example: `{"genre": "pop", "mood": "happy", "energy": 0.8}`.

### Algorithm Recipe

Every song gets points, and the points are added up:

| Rule | Points |
|---|---|
| Song's genre equals the user's favorite genre | +1.0 |
| Song's mood equals the user's favorite mood | +1.5 |
| Energy closeness: `2.0 × (1 − abs(song.energy − user.energy))` | 0 to +2.0 |

The maximum score is 4.5. Energy uses *closeness to the target*, not "higher is better", so a user who wants calm music (0.4) is not pushed toward loud songs (0.9).

Mood is weighted above genre because genre labels are sparse in this catalog (most genres appear on one song), so an exact genre match is nearly a coin flip, while mood overlaps across several songs.

### Scoring versus ranking

- **Scoring rule:** `score_song` judges one song against the profile and returns a score plus the reasons for it.
- **Ranking rule:** `recommend_songs` loops over every song in the CSV, scores each one, sorts by score from highest to lowest, and returns the top `k` with an explanation.

```
User prefs ──► for each song in songs.csv ──► score_song() ──► sort by score ──► top k
```

### Expected biases and limitations

- **Exact-match labels are brittle.** "indie pop" does not equal "pop", and "aggressive" does not equal "intense", so close neighbors get no credit. A pop fan could see an intense pop song outrank a happy indie pop one.
- **Genre can still dominate when it matches.** A song that matches genre and mood gets 2.5 points before energy, so one lucky label match can outrank a song that fits the user's energy better.
- **Energy is the only graded signal.** Songs with similar energy but different feel (dark versus bright, for example `valence` 0.49 versus 0.81) look alike to this system.
- **Tiny, hand-made catalog.** Most genres have one song, so many users will get the same few results, and styles not in the file are never recommended.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Output of `python -m src.main` for the starter profile (`genre=pop`, `mood=happy`, `energy=0.8`):

```
Loading songs from data/songs.csv...
Loaded songs: 19

============================================================
 TOP RECOMMENDATIONS
 Profile: genre=pop, mood=happy, energy=0.8
============================================================

1. Sunrise City - Neon Echo
   Score: 4.46 / 4.50
   Why:
     * genre match: pop (+1.0)
     * mood match: happy (+1.5)
     * energy 0.82 vs target 0.80 (+1.96)

2. Rooftop Lights - Indigo Parade
   Score: 3.42 / 4.50
   Why:
     * mood match: happy (+1.5)
     * energy 0.76 vs target 0.80 (+1.92)

3. Gym Hero - Max Pulse
   Score: 2.74 / 4.50
   Why:
     * genre match: pop (+1.0)
     * energy 0.93 vs target 0.80 (+1.74)

4. Concrete Crown - Metro Verse
   Score: 1.96 / 4.50
   Why:
     * energy 0.78 vs target 0.80 (+1.96)

5. Night Drive Loop - Neon Echo
   Score: 1.90 / 4.50
   Why:
     * energy 0.75 vs target 0.80 (+1.90)

============================================================
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



