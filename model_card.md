# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**MoodMatch 1.0**  

---

## 2. Intended Use  

This recommender generates song suggestions from a 20-song catalog based on a user's taste profile. It assumes the user has a single dominant mood preference, a favorite genre, an energy target, and a preference for acoustic or non-acoustic music. This is a classroom exploration project, not intended for production use.

**Non-intended use**: This system should not be used as a real music recommendation service. It lacks the data scale, user feedback loops, and contextual awareness needed for real-world recommendations. It should not be used to make assumptions about someone's personality or identity based on their music preferences.

---

## 3. How the Model Works  

The system compares each song in the catalog to what the user says they like. It checks four things:

1. **Mood** — Does the song's mood match what the user wants? This is the biggest factor (worth 3 points) because how music *feels* matters most.
2. **Acousticness** — Does the song's acoustic texture match the user's preference? Worth 2 points. An acoustic lover gets bonus points for acoustic songs; a non-acoustic listener gets points for electronic/produced tracks.
3. **Genre** — Does the song's genre match? Worth 1.5 points. Important, but less than mood because a user might enjoy multiple genres with the same vibe.
4. **Energy closeness** — How close is the song's energy level to the user's target? Worth up to 1 point. A song with energy 0.6 is a better match for a user who wants 0.65 than a song at 0.9.

The system scores every song, sorts them highest to lowest, and returns the top 5.

---

## 4. Data  

The catalog contains **20 songs** across these genres: pop, lofi, rock, ambient, jazz, synthwave, indie pop, r&b, alt-rock, reggaeton, corridos, hip-hop, prog-rock.

Moods represented include: happy, chill, intense, focused, relaxed, moody, heartbreak, dark, hype, romantic, melancholic, nostalgic, energetic, aggressive, warm, peaceful, euphoric, confident.

I added 10 songs from my own music taste (Lauryn Hill, Cold, Bad Bunny, Fuerza Regida, Michael Jackson, AFI, Thank You Scientist) to the original 10 starter songs. Missing from the dataset: K-pop, EDM subgenres, Afrobeats, gospel, and many other global genres. The catalog is too small to represent the full range of musical taste.

---

## 5. Strengths  

- **Users with a clear, single vibe** get excellent results. The "Chill Lofi Listener" profile scored a near-perfect 7.50 for "Library Rain" — matching on mood, genre, acousticness, and energy simultaneously.
- **The melancholic alt-rock profile** correctly surfaced AFI and Cold as the top 2 picks, which matches real-world intuition.
- **The explanation system** makes it transparent *why* each song was recommended, so a user can understand and trust the output.
- **Acoustic preference** successfully distinguishes organic/unplugged listeners from electronic/produced listeners, pulling in songs like Ex-Factor and Coffee Shop Stories for acoustic fans.

---

## 6. Limitations and Bias 

- **Edge case failure**: A user wanting "heartbreak" mood at high energy got "Gym Hero" (an intense pop workout song) ranked #1 instead of "Ex-Factor" (Lauryn Hill). This happened because genre match (pop, +1.5) and non-acoustic bonus (+2.0) together outweighed the mood match (+3.0) when combined with energy closeness. The system doesn't understand that heartbreak and intense are emotionally different.
- **Static profiles can't capture complex tastes**: A user who likes both "chill lofi" for studying and "intense rock" for the gym can't be represented by a single profile. Real apps like Spotify solve this with context-aware playlists.
- **Small catalog bias**: With only 20 songs, alt-rock is overrepresented (4 songs from Cold/AFI) while many genres have only 1 song. A user who likes hip-hop only has 1 option.
- **No mood similarity**: The system treats mood as all-or-nothing. "Heartbreak" and "melancholic" are very similar moods, but the system gives 0 points if they don't match exactly.
- **Acousticness threshold is rigid**: The 0.6 cutoff for "acoustic" is arbitrary. A song with 0.59 acousticness gets zero bonus for an acoustic fan, while 0.60 gets the full +2.0.

---

## 7. Evaluation  

I tested four user profiles:

1. **Melancholic Alt-Rock Fan (Acoustic)** — Top picks: Fainting Spells (AFI), Cure My Tragedy (Cold). These matched my real music taste perfectly.
2. **High-Energy Pop Lover** — Top pick: Sunrise City. Expected and reasonable.
3. **Chill Lofi Listener** — Top pick: Library Rain (7.50 score). Perfect match across all features.
4. **Edge Case: High Energy + Sad Mood** — Top pick: Gym Hero instead of Ex-Factor. This revealed that when mood and genre/acoustic pull in different directions, the non-mood features can override the mood signal despite mood having the highest individual weight.

**What surprised me**: The edge case profile showed that even though mood has the highest single weight (3.0), the combination of genre (1.5) + acoustic (2.0) = 3.5 can still override it. This means the system isn't truly "mood-first" in all cases — it's only mood-first when other features are neutral.

I also ran 3 automated pytest tests confirming the scoring logic works correctly for pop, acoustic, and melancholic profiles.

---

## 8. Future Work  

- **Mood similarity scoring**: Instead of exact match, use a similarity map so "heartbreak" and "melancholic" get partial credit (e.g., +2.0 instead of +3.0).
- **Multiple profiles per user**: Let users have different profiles for different contexts (study mode, workout mode, driving mode).
- **Diversity penalty**: Prevent the same artist from appearing more than once in the top 5 (Cold has 3 songs that could dominate).
- **Popularity signal**: Add a simulated play count to create a basic hybrid recommender that blends content-based with collaborative-style signals.
- **Larger catalog**: 20 songs is too small — expand to 50+ with better genre coverage.

---

## 9. Personal Reflection  

**Biggest learning moment**: Realizing that even with mood weighted as the highest single factor (3.0), the *combination* of other features (genre + acoustic = 3.5) can still override it. Designing fair weights is harder than it seems — every choice creates tradeoffs for different user types.

**How AI tools helped**: I used an AI coding assistant throughout the project to brainstorm scoring strategies, generate the initial song attributes for my personal music picks, implement the CSV loading and scoring functions, and design edge-case test profiles. I had to double-check the attribute values it suggested for my songs (genre, mood, energy) since I know those songs personally and could verify whether the numbers felt right.

**What surprised me**: A simple weighted scoring formula with just 4 features can produce recommendations that genuinely "feel" right. When the system recommended Fainting Spells (AFI) and Cure My Tragedy (Cold) as my top picks, those are songs I actually love. It's surprising how far basic math can go in mimicking taste.

**What I'd try next**: Adding mood similarity scoring so that related moods (heartbreak ↔ melancholic, energetic ↔ hype) get partial credit instead of zero. That single change would fix the biggest weakness in the current system.
