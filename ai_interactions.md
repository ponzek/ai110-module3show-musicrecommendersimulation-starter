# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agentic Workflow (SF8)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

I asked the AI coding assistant to explain all 4 optional extension challenges and how to approach them. It said all challenges were feasible and easy: the 5 advanced song features (popularity, release_decade, sub_mood, language, duration_sec), which I used, create a Strategy pattern with 3 scoring modes (Mood-First, Genre-First, Energy-Focused) which was my recipe for the algothrim I primarly used, implement a diversity penalty for repeat artists/genres, and format the output as ASCII tables.

**Prompts used:**

I screenshot the optional extensions and said "based off the image and my code what would be easy and feasible to accomplish. If so, walk me through how to implement it, step by step"

**What did the agent generate or change?**

- `data/songs.csv` — added 5 new columns (popularity, release_decade, sub_mood, language, duration_sec) to all 20 songs
- `src/recommender.py` — added `ScoringStrategy` abstract class, `MoodFirstStrategy`, `GenreFirstStrategy`, `EnergyFocusedStrategy`, `apply_diversity_penalty()` function, popularity bonus in all strategies, expanded `load_songs()` for new CSV fields
- `src/main.py` — added `print_table()` for ASCII formatted output, multi-strategy comparison runner

**What did you verify or fix manually?**

- Verified that the song attribute values (popularity, release_decade) made sense for the real songs I added (example, Ex-Factor is from the 1990s, Human Nature from the 1980s)
- Checked that the diversity penalty correctly prevented Cold from dominating the top 5 (there are 3 Cold songs in the catalog)
- Confirmed all 3 pytest tests still pass after the refactor
- Fixed Windows encoding issues with Unicode characters (×, ─, ▓) that the agent originally used.

---

## Design Pattern (SF10)

> Document how AI helped you choose or implement a design pattern.

**Which design pattern did you use?**

Strategy pattern — each scoring mode (Mood-First, Genre-First, Energy-Focused) is a separate class that implements the same `ScoringStrategy` interface.

**How did AI help you brainstorm or implement it?**

The assignment prompted me to ask the AI about design patterns for multiple scoring modes. The AI suggested the Strategy pattern because it keeps each scoring algorithm self-contained and makes it easy to add new modes without modifying existing code. The AI implemented the abstract base class `ScoringStrategy` with a `score()` method, and three concrete strategies that each weight the features differently.

**How does the pattern appear in your final code?**

- `ScoringStrategy` (abstract base class) in `src/recommender.py`
- `MoodFirstStrategy`, `GenreFirstStrategy`, `EnergyFocusedStrategy` — concrete implementations
- `STRATEGIES` dictionary maps string keys to strategy instances
- `recommend_songs()` accepts an optional `strategy` parameter to switch modes
- `main.py` loops through all strategies to compare results side by side
