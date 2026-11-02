# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**VibeFinder 1.0**

A small recommender that finds songs to match your vibe.

---

## 2. Intended Use  

**Goal.** VibeFinder suggests the top five songs from a small catalog. It picks them to match a listener's favorite genre, favorite mood, and target energy.

**Who it is for.** It is a classroom project. It is for learning how recommenders work, not for real listeners.

**What it assumes.**

- The user can name one genre, one mood, and one energy level.
- Those tastes stay the same from song to song.
- Exact label matches are what count.

**Intended use.**

- Learning how scoring and ranking turn data into suggestions.
- Testing what happens when you change the weights.
- Showing why each song was picked, with simple reasons.

**Not intended for.**

- Real music apps or real users.
- Judging how good or bad a song is.
- Decisions that affect artists, such as pay or promotion. The catalog is tiny and hand-made, so it would be unfair.
- Understanding lyrics, language, or culture. It does not look at any of them.

---

## 3. How the Model Works  

Think of it as a judge who gives every song in the catalog points for how well it fits what you asked for, then shows you the songs with the most points.

**What you tell it.** Three things: a favorite genre (like pop), a favorite mood (like happy), and how energetic you want the music to feel, on a scale from calm (0) to intense (1).

**How a song earns points.**

- **Genre:** a song gets 1 point if its genre is exactly the one you picked.
- **Mood:** a song gets 1.5 points if its mood is exactly the one you picked. Mood counts a little more than genre because only a few songs share a genre in this small catalog, while moods overlap across more songs.
- **Energy:** up to 2 points, depending on how *close* the song's energy is to your target. A perfect match earns the full 2 points, and the further away it is, the fewer points it earns. Closeness matters here, not "more is better": someone who wants calm music is not rewarded for a loud song.

The most a song can score is 4.5 points. Every song also gets a short list of reasons, such as "mood match: happy (+1.5)", so you can see exactly why it scored what it did.

**How the final list is chosen.** Scoring and picking are two separate steps. First, every song is scored on its own. Then all the scores are lined up from highest to lowest, and the top five are shown. Scoring alone would leave you with a pile of numbers, and picking alone would have nothing to sort by.

**What changed from the starter.** The starter code returned the first few songs in the file without judging them. This version loads the song data and turns the numbers into real numbers, then scores each song with the rules above and sorts the results. It also explains each recommendation.

**Where it falls short.** Genre and mood must match exactly, so "indie pop" gets no credit for being close to "pop". Only energy is measured on a sliding scale, so two songs with the same energy but a different feel (bright versus dark) look the same to it. Other song details in the data, such as tempo, how bright the song sounds, and how acoustic it is, are not used yet.

---

## 4. Data  

- **Size:** 19 songs in `data/songs.csv`.
- **Where it came from:** 10 came with the starter. I added 9 more (hip hop, r&b, country, classical, metal, reggae, edm, folk, blues) to widen the range.
- **Features per song:** genre, mood, energy, tempo, valence, danceability, and acousticness.
- **Used in scoring:** only genre, mood, and energy. The rest are loaded but not used yet.
- **Variety:** 16 genres and 15 moods. Most appear once. Lofi is the only genre with three songs.

**Limits.**

- The numbers are made up by hand, not measured from real audio.
- It is very small. Most genres have just one song.
- There are no songs with energy between 0.56 and 0.74. A listener who wants medium energy gets a thin, odd list.
- No lyrics, language, artist popularity, or listening history.
- Western pop-style genres dominate. Many kinds of music are missing.

---

## 5. Strengths  

- **Calm and loud listeners get clearly different lists.** Pop and lofi fans share no songs at all.
- **Lofi works best.** The top four songs for a chill lofi fan were all lofi or ambient, with almost perfect energy.
- **Energy is scored by closeness, not "more is better".** Calm listeners are not given loud songs.
- **Every pick comes with reasons.** For example: "mood match: happy (+1.5)". It is easy to see why a song ranked where it did.
- **The top pick usually matches my gut.** Sunrise City for happy pop, Midnight Coding for lofi, and Storm Runner for rock all felt right.

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

The biggest weakness I found is that a matching label can outweigh a very large mismatch in energy. For a user who asked for classical, aggressive music at a low energy of 0.2, the metal song Iron Tide (energy 0.97) ranked second, because the 1.5-point mood match was worth more than the energy penalty. Labels that aren't in the catalog are also silently ignored, so a "sad" or "k-pop" listener gets recommendations based on energy alone, with no warning that their taste wasn't understood. Because energy is the only graded feature and the catalog is small, the same loud songs (Storm Runner, Gym Hero, Bass Cathedral) show up in the top five for almost any high-energy request, which creates a mild filter bubble. People who like quiet, acoustic or niche music are better served than people with unusual tastes, since the catalog has only a few songs per genre.

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

### Profiles tested

I ran six made-up listeners and looked at each one's top five songs (full output is in the README under "Profile Evaluation"):

| Label | What they asked for | Type |
|---|---|---|
| **A. High-Energy Pop** | pop, happy, very energetic (0.9) | typical |
| **B. Chill Lofi** | lofi, chill, calm (0.4) | typical |
| **C. Deep Intense Rock** | rock, intense, very energetic (0.92) | typical |
| **D. Sad but Energetic** | folk, sad, very energetic (0.9) | trick profile: the two wishes pull against each other |
| **E. Unknown Tastes** | k-pop, dreamy, medium energy (0.6) | trick profile: neither label exists in the catalog |
| **F. Classical but Aggressive** | classical, aggressive, very calm (0.2) | trick profile: genre and mood point in opposite directions |

For each one I checked three things: does the top song match what I would pick by hand, does the list move in a sensible direction when the energy target moves, and does the explanation for each song add up.

### What surprised me

- **"Gym Hero" keeps showing up, and it isn't a bug.** For someone who wants happy pop, Gym Hero (a pop song, but an intense workout track) lands in third place. The system can't hear the difference between a cheerful pop song and a pumped-up gym song. It only checks three things: is the genre pop, is the mood "happy", and how close is the energy to what you asked for. Gym Hero is pop (a point) and almost exactly as energetic as the user wanted, so it scores well. It only misses the "happy" bonus, because its mood is "intense". It also appears for the rock fan (its mood is "intense", which is a match) and the sad-but-energetic listener (it is simply very energetic). That is three of the six lists, for three different reasons.
- **The rock fan and the sad folk fan got the same five songs in the same order.** Only the scores differed. The sad folk listener asked for a mood the catalog doesn't have and a genre with only one quiet song, so the system fell back on "who is loud?", and loud songs are what the rock fan got too.
- **A metal song showed up for a calm-music request.** For listener F, Iron Tide (energy 0.97) took second place for someone who wanted energy 0.2, because its "aggressive" mood matched, and that bonus was worth more than being far off on energy.
- **Lofi worked best, mainly because the catalog has three lofi songs.** Having several songs of the same style is what lets the system look smart.

### Comparing each pair of profiles

| Pair | What changed in the results, and why it makes sense |
|---|---|
| A vs B | Zero songs in common. Pop-happy-energetic gives bright, loud songs, and lofi-chill-calm gives soft, quiet ones. This is the cleanest sign that energy and the labels work. |
| A vs C | Four of five songs are shared (Sunrise City, Gym Hero, Storm Runner, Bass Cathedral), since both want very energetic music. Only the top slots differ: the pop fan gets happy pop first, and the rock fan gets Storm Runner first, because the labels broke the tie. |
| A vs D | Four songs are shared again, since both want energy 0.9. A gets Rooftop Lights because it matches "happy". D has no label matches, so Iron Tide takes its place. |
| A vs E | No overlap. E wants middle energy (0.6), so it gets mid-tempo songs from many genres, none of them loud pop. Sensible, but there are no label matches to make it feel personal. |
| A vs F | No overlap. A wants loud, F wants quiet. F also gets its one classical song at the top, a genre match that A can't use. |
| B vs C | No overlap. These are the two opposite ends: the calm lofi listener and the loud rock listener. |
| B vs D | No overlap, with the same reasoning as above. D's folk label barely helps, because folk songs in this catalog are quiet and D wants loud. |
| B vs E | No overlap. B wants 0.4 and E wants 0.6. That gap is enough to move to a different set of songs, which shows how sensitive the energy score is. |
| B vs F | Two songs are shared (Spacewalk Thoughts, Library Rain), since both want calm music. B gets lofi first and F gets classical first, because the genre label is the tiebreaker. The best "same direction, different taste" comparison. |
| C vs D | The same five songs in the same order. This is the least sensible result. A rock fan and a sad folk fan are very different people, and the system can't tell, because folk and "sad" have no good match here. |
| C vs E | No overlap. C is loud and E is middle, so nothing carries over. |
| C vs F | Only Iron Tide is shared, for opposite reasons. C gets it because of the high energy, and F gets it because of the "aggressive" mood. It is a good example of a label overriding energy. |
| D vs E | No overlap, but they behave alike: neither has a working label, so both are pure "closest energy" lists. D's list is loud (target 0.9) and E's is middle-of-the-road (target 0.6). |
| D vs F | Only Iron Tide in common. D wants loud songs and gets them, and F wants quiet ones but gets one loud song by mood. This shows the mood bonus is large. |
| E vs F | No overlap. F finds a classical song through its genre label and E finds nothing, so F's list has some personality and E's doesn't. |

### Do the results make sense?

For the three normal profiles, yes: each one's top pick is what I'd choose by hand, and the lists move in the right direction as energy goes up or down. The trick profiles exposed the weak spots: labels that don't exist are ignored, and a label match can beat a big energy mismatch. A doubled-energy experiment fixed the classical-aggressive case but left the others unchanged, so the real issue is that the system only matches labels exactly (details in the README under "Experiments You Tried").

---

## 8. Future Work  

1. **Give partial credit for close labels.** "Aggressive" is near "intense", and "indie pop" is near "pop". Right now they get zero. This would fix the metal-versus-pop mix-up for rock fans.
2. **Use more song features.** Valence and acousticness would tell bright songs from dark ones at the same energy. Danceability and tempo could help too.
3. **Warn and diversify.** Say so when a genre or mood is not in the catalog, instead of quietly ignoring it. Also stop the same loud songs from filling every top five, and add more songs to the catalog.

---

## 9. Personal Reflection  

**Biggest learning moment.** Scoring and ranking are two different jobs. Scoring judges one song. Ranking sorts all the scores. I also learned that the weights are really opinions. Changing a 1.5 to a 1.0 can change who gets recommended.

**How AI helped, and where I double-checked.** AI helped me plan the scoring rule, write the code, and draft the write-ups. I still checked its work. It left a hardcoded "4.50" in the output that would have been wrong after a weight change, and I caught a wrong claim in my own notes (I said folk had two songs, but it has one). The import that worked in one way of running the program failed in another. Running the code and checking the numbers against the real output was how I caught these. Several times, editor warnings were out of date and the program was fine.

**What surprised me.** A few simple rules can feel like a real recommendation, especially when the top song matches your taste and comes with a reason. But the same rules also failed in odd ways. Gym Hero kept showing up for people who wanted happy pop, because the system only sees labels and one energy number, not what a song feels like. It made me think about how much real apps must hide behind a confident-looking list.

**What I would try next.** Add valence and acousticness to the score, give partial credit for related moods and genres, and write a few tests for the odd profiles. I would also grow the catalog, so more than one song represents each genre.
