# 🎵 Music Recommender Simulation

## Project Summary

This is a content-based music recommender that matches songs to a user's taste profile. It scores each song in a 20-song catalog based on how well it fits the user's preferred mood, acoustic preference, genre, and energy level — then returns the top recommendations with explanations.

---

## How The System Works

The recommender uses **content-based filtering** — it looks at each song's attributes and compares them to what the user likes. Unlike collaborative filtering (which relies on other users' behavior), this approach only needs the song data and a user profile.

### Song Features

Each `Song` has these attributes: `genre`, `mood`, `energy`, `tempo_bpm`, `valence`, `danceability`, and `acousticness`.

### User Profile

A `UserProfile` stores: `favorite_genre`, `favorite_mood`, `target_energy`, and `likes_acoustic`.

### Scoring Algorithm

Each song gets a score based on this formula:

```
score = (mood_match × 3) + (acoustic_bonus × 2) + (genre_match × 1.5) + (1 - |energy_diff|)
```

- **Mood match (×3)**: Highest weight because the emotional feel of the music matters most
- **Acousticness bonus (×2)**: The sound texture — acoustic vs electronic — is the second priority
- **Genre match (×1.5)**: The musical category matters, but less than how the song feels
- **Energy closeness (×1)**: Rewards songs with energy levels close to the user's target

### How Recommendations Are Chosen

Every song in the catalog is scored against the user profile. Songs are sorted by score (highest first), and the top-k are returned.

### Data Flow

```
User Profile (mood, acoustic pref, genre, energy)
        │
        ▼
  ┌─────────────┐
  │  Score each  │ ← Loop through all 18 songs
  │  song in CSV │
  └──────┬──────┘
         │
         ▼
  Sort by score (highest first)
         │
         ▼
  Return top-k recommendations with explanations
```

### Potential Biases

This system might over-prioritize mood, causing it to ignore songs from a user's favorite genre if the mood doesn't match exactly. It also has no way to learn or adapt — a user who likes both "chill lofi" and "intense rock" depending on context can't be fully represented by a single static profile.

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

```
Loaded songs: 20

User profile: genre=alt-rock, mood=melancholic, energy=0.65, likes_acoustic=True
======================================================================

Top recommendations:

  1. Fainting Spells by AFI
     Genre: alt-rock | Mood: melancholic | Energy: 0.65
     Score: 5.50
     Because: mood match: 'melancholic' (+3.0); genre match: 'alt-rock' (+1.5); energy closeness: 1.00 (+1.00)

  2. Cure My Tragedy by Cold
     Genre: alt-rock | Mood: melancholic | Energy: 0.6
     Score: 5.45
     Because: mood match: 'melancholic' (+3.0); genre match: 'alt-rock' (+1.5); energy closeness: 0.95 (+0.95)

  3. Ex-Factor by Lauryn Hill
     Genre: r&b | Mood: heartbreak | Energy: 0.45
     Score: 2.80
     Because: acoustic fit: acousticness=0.60 (+2.0); energy closeness: 0.80 (+0.80)

  4. Midnight Coding by LoRoom
     Genre: lofi | Mood: chill | Energy: 0.42
     Score: 2.77
     Because: acoustic fit: acousticness=0.71 (+2.0); energy closeness: 0.77 (+0.77)

  5. Focus Flow by LoRoom
     Genre: lofi | Mood: focused | Energy: 0.4
     Score: 2.75
     Because: acoustic fit: acousticness=0.78 (+2.0); energy closeness: 0.75 (+0.75)
```

---

## Experiments You Tried

- **Tested 4 diverse user profiles**: Melancholic Alt-Rock (acoustic), High-Energy Pop, Chill Lofi, and an Edge Case (high energy + heartbreak mood). Each profile produced meaningfully different top-5 rankings.
- **Edge case discovery**: A user wanting heartbreak mood at high energy got "Gym Hero" (intense pop) ranked above "Ex-Factor" (Lauryn Hill, actual heartbreak). This revealed that genre+acoustic bonuses (1.5+2.0=3.5) can outweigh even the highest-weighted mood match (3.0) when combined with energy closeness.
- **Weight choices matter**: Mood at ×3 works great for single-vibe users but breaks down for conflicting preferences. Increasing mood weight to ×4 would fix the edge case but might over-restrict variety for normal profiles.

---

## Limitations and Risks

- It only works on a 20-song catalog — too small for real-world use
- It does not understand lyrics, language, or cultural context
- Alt-rock is overrepresented (4 songs) while most genres have only 1 song
- Mood matching is exact-only — "heartbreak" and "melancholic" get zero credit for being similar
- A single static user profile can't capture someone who likes different music in different contexts
- The acousticness threshold (0.6) is a hard cutoff that creates unfair jumps in scoring

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Building this recommender taught me that turning music taste into numbers and rules is harder than it looks. The scoring formula seems simple — just add up points for matching features — but the *weights* you choose determine who the system works for and who it fails. My mood-first design was great for users with a clear emotional preference, but it struggled when mood and genre pulled in opposite directions.

Bias in recommender systems isn't always obvious. My system has a small dataset bias (alt-rock gets 4 songs, hip-hop gets 1) and a structural bias (exact mood matching means similar moods like "heartbreak" and "melancholic" get no partial credit). In real apps like Spotify, these subtle biases at scale can create filter bubbles where users never discover music outside their established patterns — reinforcing existing preferences rather than expanding tastes.
