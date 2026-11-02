# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

My version, **VibeFinder 1.0**, is a content-based recommender that runs in the terminal. It loads a 19-song catalog from a CSV, scores every song against a listener's favorite genre, favorite mood, and target energy, and prints the top five with the reasons behind each score. I tested it on six listener profiles, including three tricky ones, and ran one weight experiment.

---

## How Real-World Recommenders Work

Apps like Spotify and YouTube combine three kinds of information. It helps to keep them separate.

**1. Input data: what the system knows about the songs and about behavior.**

- *Song features.* Genre and mood tags, plus audio measurements such as tempo, energy, valence (how positive it sounds), danceability, and acousticness. Some systems also analyze lyrics, titles, and descriptions.
- *Behavior signals.* What people play, skip, replay, save, and add to playlists, and at what time of day. Skipping a song after ten seconds is a signal too.

**2. User preferences: a picture of what one listener likes.** This is built from their history (what they replay and skip), sometimes together with things they choose directly, such as followed artists. It is stored as a "taste profile".

**3. Ranking and selection: turning all of that into a short list.** The system scores a very large set of candidate songs, sorts them, and shows the top few. Real systems often add a final step that mixes in variety, so the list isn't ten near-identical songs.

There are two main ways to score a song:

- **Content-based filtering** compares a song's own features to what the listener likes: "you like high-energy pop, so here is more high-energy pop".
- **Collaborative filtering** uses other people's behavior: "listeners with a history like yours also loved this song", even when the song looks different on paper.

Real products blend both. Collaborative filtering needs lots of user data, but it can find surprises that feature matching can't.

**What this project does.** It uses only content-based filtering, with three features (genre, mood, energy) and a profile typed in by hand. It has no listening history and no other users, which is the biggest difference from a real app. The same steps still apply: song data goes in, a taste profile defines what to look for, and a scoring rule plus a sort produce the final list.

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

## Profile Evaluation

Output of `python -m src.main` for six user profiles: three typical listeners and three adversarial or edge-case profiles designed to try to trick the scoring logic.

### 1. High-Energy Pop (typical)

```
============================================================
 PROFILE: High-Energy Pop
 genre=pop, mood=happy, energy=0.9
============================================================

1. Sunrise City - Neon Echo (pop, happy)
   Score: 4.34 / 4.50
   Why:
     * genre match: pop (+1.0)
     * mood match: happy (+1.5)
     * energy 0.82 vs target 0.90 (+1.84)

2. Rooftop Lights - Indigo Parade (indie pop, happy)
   Score: 3.22 / 4.50
   Why:
     * mood match: happy (+1.5)
     * energy 0.76 vs target 0.90 (+1.72)

3. Gym Hero - Max Pulse (pop, intense)
   Score: 2.94 / 4.50
   Why:
     * genre match: pop (+1.0)
     * energy 0.93 vs target 0.90 (+1.94)

4. Storm Runner - Voltline (rock, intense)
   Score: 1.98 / 4.50
   Why:
     * energy 0.91 vs target 0.90 (+1.98)

5. Bass Cathedral - Pulse Theory (edm, euphoric)
   Score: 1.92 / 4.50
   Why:
     * energy 0.94 vs target 0.90 (+1.92)

============================================================
```

**Observation:** The top three feel right. Slots 4 and 5 are chosen on energy alone, so a rock song and an EDM track fill them.

### 2. Chill Lofi (typical)

```
============================================================
 PROFILE: Chill Lofi
 genre=lofi, mood=chill, energy=0.4
============================================================

1. Midnight Coding - LoRoom (lofi, chill)
   Score: 4.46 / 4.50
   Why:
     * genre match: lofi (+1.0)
     * mood match: chill (+1.5)
     * energy 0.42 vs target 0.40 (+1.96)

2. Library Rain - Paper Lanterns (lofi, chill)
   Score: 4.40 / 4.50
   Why:
     * genre match: lofi (+1.0)
     * mood match: chill (+1.5)
     * energy 0.35 vs target 0.40 (+1.90)

3. Spacewalk Thoughts - Orbit Bloom (ambient, chill)
   Score: 3.26 / 4.50
   Why:
     * mood match: chill (+1.5)
     * energy 0.28 vs target 0.40 (+1.76)

4. Focus Flow - LoRoom (lofi, focused)
   Score: 3.00 / 4.50
   Why:
     * genre match: lofi (+1.0)
     * energy 0.40 vs target 0.40 (+2.00)

5. Coffee Shop Stories - Slow Stereo (jazz, relaxed)
   Score: 1.94 / 4.50
   Why:
     * energy 0.37 vs target 0.40 (+1.94)

============================================================
```

**Observation:** This is the strongest result. The top four are all lofi or ambient, with near-perfect energy.

### 3. Deep Intense Rock (typical)

```
============================================================
 PROFILE: Deep Intense Rock
 genre=rock, mood=intense, energy=0.92
============================================================

1. Storm Runner - Voltline (rock, intense)
   Score: 4.48 / 4.50
   Why:
     * genre match: rock (+1.0)
     * mood match: intense (+1.5)
     * energy 0.91 vs target 0.92 (+1.98)

2. Gym Hero - Max Pulse (pop, intense)
   Score: 3.48 / 4.50
   Why:
     * mood match: intense (+1.5)
     * energy 0.93 vs target 0.92 (+1.98)

3. Bass Cathedral - Pulse Theory (edm, euphoric)
   Score: 1.96 / 4.50
   Why:
     * energy 0.94 vs target 0.92 (+1.96)

4. Iron Tide - Black Anvil (metal, aggressive)
   Score: 1.90 / 4.50
   Why:
     * energy 0.97 vs target 0.92 (+1.90)

5. Sunrise City - Neon Echo (pop, happy)
   Score: 1.80 / 4.50
   Why:
     * energy 0.82 vs target 0.92 (+1.80)

============================================================
```

**Observation:** There is only one rock song, so after Storm Runner the list is a pop song that shares the "intense" label. Iron Tide (metal) is the more natural second pick but is ranked fourth, because "aggressive" does not equal "intense". Sunrise City (a happy pop song) still reaches the top five.

### 4. Adversarial: sad but energetic (conflicting preferences)

```
============================================================
 PROFILE: Conflicting: sad but energetic
 genre=folk, mood=sad, energy=0.9
============================================================

1. Storm Runner - Voltline (rock, intense)
   Score: 1.98 / 4.50
   Why:
     * energy 0.91 vs target 0.90 (+1.98)

2. Gym Hero - Max Pulse (pop, intense)
   Score: 1.94 / 4.50
   Why:
     * energy 0.93 vs target 0.90 (+1.94)

3. Bass Cathedral - Pulse Theory (edm, euphoric)
   Score: 1.92 / 4.50
   Why:
     * energy 0.94 vs target 0.90 (+1.92)

4. Iron Tide - Black Anvil (metal, aggressive)
   Score: 1.86 / 4.50
   Why:
     * energy 0.97 vs target 0.90 (+1.86)

5. Sunrise City - Neon Echo (pop, happy)
   Score: 1.84 / 4.50
   Why:
     * energy 0.82 vs target 0.90 (+1.84)

============================================================
```

**Observation:** The mood "sad" does not exist in the catalog, so it is ignored. Energy decides everything, and the user gets loud, upbeat songs, including a happy pop song, even though they asked for sad folk. The folk song Willow Creek earns its genre point but loses on energy (0.30 vs 0.9), so it falls out of the top five.

### 5. Adversarial: unknown tastes (no label matches)

```
============================================================
 PROFILE: Unknown tastes (no label matches)
 genre=k-pop, mood=dreamy, energy=0.6
============================================================

1. Island Breeze - Coral Sun (reggae, laid-back)
   Score: 1.90 / 4.50
   Why:
     * energy 0.55 vs target 0.60 (+1.90)

2. Velvet Hours - Satin Gray (r&b, romantic)
   Score: 1.84 / 4.50
   Why:
     * energy 0.52 vs target 0.60 (+1.84)

3. Dust Road Home - Cedar Hollow (country, nostalgic)
   Score: 1.76 / 4.50
   Why:
     * energy 0.48 vs target 0.60 (+1.76)

4. Night Drive Loop - Neon Echo (synthwave, moody)
   Score: 1.70 / 4.50
   Why:
     * energy 0.75 vs target 0.60 (+1.70)

5. Smoky Back Room - Lou Delmar (blues, wistful)
   Score: 1.68 / 4.50
   Why:
     * energy 0.44 vs target 0.60 (+1.68)

============================================================
```

**Observation:** With no genre or mood match, the system reduces to "closest energy". The results are a mix of unrelated genres, and nothing in the output warns the user that their tastes weren't understood.

### 6. Adversarial: mismatched genre vs mood

```
============================================================
 PROFILE: Mismatched genre vs mood
 genre=classical, mood=aggressive, energy=0.2
============================================================

1. Moonlit Sonata - Elara Voss (classical, peaceful)
   Score: 2.96 / 4.50
   Why:
     * genre match: classical (+1.0)
     * energy 0.18 vs target 0.20 (+1.96)

2. Iron Tide - Black Anvil (metal, aggressive)
   Score: 1.96 / 4.50
   Why:
     * mood match: aggressive (+1.5)
     * energy 0.97 vs target 0.20 (+0.46)

3. Spacewalk Thoughts - Orbit Bloom (ambient, chill)
   Score: 1.84 / 4.50
   Why:
     * energy 0.28 vs target 0.20 (+1.84)

4. Willow Creek - Fern & Ash (folk, melancholy)
   Score: 1.80 / 4.50
   Why:
     * energy 0.30 vs target 0.20 (+1.80)

5. Library Rain - Paper Lanterns (lofi, chill)
   Score: 1.70 / 4.50
   Why:
     * energy 0.35 vs target 0.20 (+1.70)

============================================================
```

**Observation:** Iron Tide (energy 0.97, metal) ranks second for a user who wants energy 0.2. The 1.5-point mood match outweighs a 0.77 energy gap, because a label match pays more than the energy penalty costs. The scoring has no way to say "this song contradicts what you asked for".

### Summary of what the profiles showed

- **Typical profiles work well.** Pop, lofi and rock users each get a sensible top result.
- **Labels that don't exist are ignored.** A mood or genre the catalog lacks gives no match and no warning. The system falls back to energy only.
- **A label match can outweigh a large energy mismatch.** Profile 6 shows mood (+1.5) pulling in a song far from the requested energy.
- **Near-miss labels get no credit.** "aggressive" is not "intense" and "indie pop" is not "pop", which is the main limit of exact-match scoring.

---

## Experiments You Tried

### Weight shift: double energy, halve genre

**Change:** `ENERGY_POINTS` 2.0 → 4.0 and `GENRE_POINTS` 1.0 → 0.5, with mood unchanged at 1.5. The maximum score moves from 4.5 to 6.0, so scores are not directly comparable between runs. I ran it against all six profiles above and compared the top five with the baseline.

**Result:** five of the six profiles returned the same songs in the same order, and only the scores went up. The one profile that changed was the mismatched genre vs mood case (`classical`, `aggressive`, energy 0.2):

| Rank | Baseline | Weight shift |
|---|---|---|
| 1 | Moonlit Sonata (2.96) | Moonlit Sonata (4.42) |
| 2 | Iron Tide, energy 0.97 (1.96) | Spacewalk Thoughts, energy 0.28 (3.68) |
| 3 | Spacewalk Thoughts (1.84) | Willow Creek (3.60) |
| 4 | Willow Creek (1.80) | Library Rain (3.40) |
| 5 | Library Rain (1.70) | Coffee Shop Stories (3.32) |

**Was it more accurate or just different?** For that profile it was more accurate: Iron Tide, a loud metal song for a user who wanted energy 0.2, dropped out of the top five. For the other five it made no difference to the ranking, so the change is a safe improvement here. The cost is that energy now dominates more, which strengthens the pattern where the same loud songs fill the top five for any high-energy request. Doubling energy fixed the symptom but not the cause (exact-match labels).

The change was tested without editing the weights in `recommender.py`, so the Algorithm Recipe above is still the one the program uses.

### Other ideas not yet tried

- Partial credit for related moods and genres ("aggressive" near "intense", "indie pop" near "pop").
- Adding `valence` or `acousticness` so songs with the same energy but a different feel can be told apart.
- A warning when the user's genre or mood does not exist in the catalog.

---

## Limitations and Risks

- **Tiny catalog.** Only 19 songs, and most genres have just one. There is also a gap with no songs between energy 0.56 and 0.74.
- **Exact-match labels.** "Aggressive" does not match "intense", and "indie pop" does not match "pop", so close neighbors get no credit.
- **Labels that don't exist are silently ignored.** A "sad" or "k-pop" listener gets energy-only results, with no warning.
- **A label can outweigh a big energy mismatch.** A metal song (energy 0.97) ranked second for a listener who wanted energy 0.2.
- **Same loud songs repeat.** Energy is the only graded feature, so high-energy requests keep pulling the same few songs.
- **No lyrics, language, or listening history.**

The model card goes deeper: [Model Card](model_card.md).

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

**How recommenders turn data into predictions.** A recommender doesn't understand music. It turns songs and tastes into numbers, scores each song with a rule, and sorts the scores. Scoring (judging one song) and ranking (ordering all of them) are separate jobs, and both are needed. The weights are really opinions: a mood match is worth 1.5 points only because I decided so, and changing it changes who gets recommended.

**Where bias and unfairness can show up.** The scoring rule treats labels as exact matches, so listeners with common tastes are served well and listeners with unusual tastes are not. A small catalog adds to this, since the same few songs fill many lists. In a real app, the same effect could mean some artists and genres rarely get heard. The full discussion is in the [model card](model_card.md).



