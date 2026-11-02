# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

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

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  
