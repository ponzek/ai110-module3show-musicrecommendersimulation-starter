"""Music Recommender Simulation — Hybrid content-based recommender with Strategy pattern."""

import csv
import os
from typing import List, Dict, Tuple, Optional, Callable
from dataclasses import dataclass
from abc import ABC, abstractmethod

# Project root is one level up from this file's directory (src/)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


@dataclass
class Song:
    """Represents a song and its attributes, including advanced features."""
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
    # Advanced features (Challenge 1)
    popularity: int = 0
    release_decade: str = ""
    sub_mood: str = ""
    language: str = "en"
    duration_sec: int = 0


@dataclass
class UserProfile:
    """Represents a user's taste preferences."""
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool


# ---------------------------------------------------------------------------
# Challenge 2: Strategy Pattern — Multiple Scoring Modes
# ---------------------------------------------------------------------------

class ScoringStrategy(ABC):
    """Abstract base class for scoring strategies."""

    @abstractmethod
    def name(self) -> str:
        """Return the name of this scoring strategy."""
        pass

    @abstractmethod
    def score(self, user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
        """Score a song against user preferences. Returns (score, reasons)."""
        pass


class MoodFirstStrategy(ScoringStrategy):
    """Default strategy: mood is the strongest signal."""

    def name(self) -> str:
        return "Mood-First"

    def score(self, user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
        score = 0.0
        reasons = []

        # Mood match (weight: 3)
        if song["mood"] == user_prefs.get("mood"):
            score += 3.0
            reasons.append(f"mood match: '{song['mood']}' (+3.0)")

        # Acousticness bonus (weight: 2)
        likes_acoustic = user_prefs.get("likes_acoustic", False)
        if likes_acoustic and song["acousticness"] >= 0.6:
            score += 2.0
            reasons.append(f"acoustic fit: {song['acousticness']:.2f} (+2.0)")
        elif not likes_acoustic and song["acousticness"] < 0.4:
            score += 2.0
            reasons.append(f"non-acoustic fit: {song['acousticness']:.2f} (+2.0)")

        # Genre match (weight: 1.5)
        if song["genre"] == user_prefs.get("genre"):
            score += 1.5
            reasons.append(f"genre match: '{song['genre']}' (+1.5)")

        # Energy closeness (weight: 1)
        target_energy = user_prefs.get("energy", 0.5)
        energy_closeness = 1.0 - abs(song["energy"] - target_energy)
        score += energy_closeness
        reasons.append(f"energy closeness: {energy_closeness:.2f}")

        # Popularity bonus — hybrid signal (weight: 0.5)
        pop = song.get("popularity", 0)
        pop_bonus = (pop / 100.0) * 0.5
        score += pop_bonus
        reasons.append(f"popularity: {pop}/100 (+{pop_bonus:.2f})")

        return (score, reasons)


class GenreFirstStrategy(ScoringStrategy):
    """Genre is the strongest signal."""

    def name(self) -> str:
        return "Genre-First"

    def score(self, user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
        score = 0.0
        reasons = []

        # Genre match (weight: 3)
        if song["genre"] == user_prefs.get("genre"):
            score += 3.0
            reasons.append(f"genre match: '{song['genre']}' (+3.0)")

        # Mood match (weight: 2)
        if song["mood"] == user_prefs.get("mood"):
            score += 2.0
            reasons.append(f"mood match: '{song['mood']}' (+2.0)")

        # Acousticness bonus (weight: 1.5)
        likes_acoustic = user_prefs.get("likes_acoustic", False)
        if likes_acoustic and song["acousticness"] >= 0.6:
            score += 1.5
            reasons.append(f"acoustic fit: {song['acousticness']:.2f} (+1.5)")
        elif not likes_acoustic and song["acousticness"] < 0.4:
            score += 1.5
            reasons.append(f"non-acoustic fit: {song['acousticness']:.2f} (+1.5)")

        # Energy closeness (weight: 1)
        target_energy = user_prefs.get("energy", 0.5)
        energy_closeness = 1.0 - abs(song["energy"] - target_energy)
        score += energy_closeness
        reasons.append(f"energy closeness: {energy_closeness:.2f}")

        # Popularity bonus (weight: 0.5)
        pop = song.get("popularity", 0)
        pop_bonus = (pop / 100.0) * 0.5
        score += pop_bonus
        reasons.append(f"popularity: {pop}/100 (+{pop_bonus:.2f})")

        return (score, reasons)


class EnergyFocusedStrategy(ScoringStrategy):
    """Energy closeness is the strongest signal — great for workout/study playlists."""

    def name(self) -> str:
        return "Energy-Focused"

    def score(self, user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
        score = 0.0
        reasons = []

        # Energy closeness (weight: 3)
        target_energy = user_prefs.get("energy", 0.5)
        energy_closeness = 1.0 - abs(song["energy"] - target_energy)
        score += energy_closeness * 3.0
        reasons.append(f"energy closeness: {energy_closeness:.2f} (x3 = +{energy_closeness * 3:.2f})")

        # Mood match (weight: 1.5)
        if song["mood"] == user_prefs.get("mood"):
            score += 1.5
            reasons.append(f"mood match: '{song['mood']}' (+1.5)")

        # Genre match (weight: 1)
        if song["genre"] == user_prefs.get("genre"):
            score += 1.0
            reasons.append(f"genre match: '{song['genre']}' (+1.0)")

        # Popularity bonus (weight: 0.5)
        pop = song.get("popularity", 0)
        pop_bonus = (pop / 100.0) * 0.5
        score += pop_bonus
        reasons.append(f"popularity: {pop}/100 (+{pop_bonus:.2f})")

        return (score, reasons)


# Map of available strategies
STRATEGIES: Dict[str, ScoringStrategy] = {
    "mood-first": MoodFirstStrategy(),
    "genre-first": GenreFirstStrategy(),
    "energy-focused": EnergyFocusedStrategy(),
}


# ---------------------------------------------------------------------------
# OOP Recommender (required by tests)
# ---------------------------------------------------------------------------

class Recommender:
    """OOP implementation of the recommendation logic."""

    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Score and rank songs, returning the top-k matches for the user."""
        scored = []
        for song in self.songs:
            score = self._score(user, song)
            scored.append((song, score))

        scored.sort(key=lambda x: x[1], reverse=True)
        return [song for song, score in scored[:k]]

    def _score(self, user: UserProfile, song: Song) -> float:
        """Calculate a match score between a user profile and a song."""
        score = 0.0

        if song.mood == user.favorite_mood:
            score += 3.0

        if user.likes_acoustic and song.acousticness >= 0.6:
            score += 2.0
        elif not user.likes_acoustic and song.acousticness < 0.4:
            score += 2.0

        if song.genre == user.favorite_genre:
            score += 1.5

        energy_closeness = 1.0 - abs(song.energy - user.target_energy)
        score += energy_closeness

        return score

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Generate a human-readable explanation for why a song was recommended."""
        reasons = []

        if song.mood == user.favorite_mood:
            reasons.append(f"mood match: '{song.mood}' (+3.0)")

        if user.likes_acoustic and song.acousticness >= 0.6:
            reasons.append(f"acoustic fit: {song.acousticness:.2f} (+2.0)")
        elif not user.likes_acoustic and song.acousticness < 0.4:
            reasons.append(f"non-acoustic fit: {song.acousticness:.2f} (+2.0)")

        if song.genre == user.favorite_genre:
            reasons.append(f"genre match: '{song.genre}' (+1.5)")

        energy_closeness = 1.0 - abs(song.energy - user.target_energy)
        reasons.append(f"energy closeness: {energy_closeness:.2f}")

        return "; ".join(reasons) if reasons else "No strong match found"


# ---------------------------------------------------------------------------
# Standalone Functions (used by main.py)
# ---------------------------------------------------------------------------

def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from a CSV file and return a list of dictionaries with proper types."""
    songs = []
    full_path = os.path.join(PROJECT_ROOT, csv_path)
    with open(full_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            song = {
                "id": int(row["id"]),
                "title": row["title"],
                "artist": row["artist"],
                "genre": row["genre"],
                "mood": row["mood"],
                "energy": float(row["energy"]),
                "tempo_bpm": float(row["tempo_bpm"]),
                "valence": float(row["valence"]),
                "danceability": float(row["danceability"]),
                "acousticness": float(row["acousticness"]),
                # Advanced features
                "popularity": int(row.get("popularity", 0)),
                "release_decade": row.get("release_decade", ""),
                "sub_mood": row.get("sub_mood", ""),
                "language": row.get("language", "en"),
                "duration_sec": int(row.get("duration_sec", 0)),
            }
            songs.append(song)

    print(f"Loaded songs: {len(songs)}")
    return songs


def score_song(user_prefs: Dict, song: Dict, strategy: ScoringStrategy = None) -> Tuple[float, List[str]]:
    """Score a single song against user preferences using the given strategy."""
    if strategy is None:
        strategy = STRATEGIES["mood-first"]
    return strategy.score(user_prefs, song)


# ---------------------------------------------------------------------------
# Challenge 3: Diversity Penalty
# ---------------------------------------------------------------------------

def apply_diversity_penalty(
    scored_songs: List[Tuple[Dict, float, str]],
    penalty: float = 1.5,
) -> List[Tuple[Dict, float, str]]:
    """Re-rank songs by penalizing repeat artists/genres in the top results."""
    reranked = []
    seen_artists = set()
    seen_genres = set()

    for song, score, explanation in scored_songs:
        adjusted_score = score
        penalties = []

        if song["artist"] in seen_artists:
            adjusted_score -= penalty
            penalties.append(f"repeat artist penalty (-{penalty})")

        if song["genre"] in seen_genres:
            adjusted_score -= penalty * 0.5
            penalties.append(f"repeat genre penalty (-{penalty * 0.5})")

        if penalties:
            explanation += "; " + "; ".join(penalties)

        reranked.append((song, adjusted_score, explanation))
        seen_artists.add(song["artist"])
        seen_genres.add(song["genre"])

    # Re-sort after penalties
    reranked.sort(key=lambda x: x[1], reverse=True)
    return reranked


def recommend_songs(
    user_prefs: Dict,
    songs: List[Dict],
    k: int = 5,
    strategy: ScoringStrategy = None,
    diversity: bool = True,
) -> List[Tuple[Dict, float, str]]:
    """Score all songs, optionally apply diversity penalty, and return top-k."""
    if strategy is None:
        strategy = STRATEGIES["mood-first"]

    scored_songs = []
    for song in songs:
        score, reasons = score_song(user_prefs, song, strategy)
        explanation = "; ".join(reasons)
        scored_songs.append((song, score, explanation))

    # Sort by score descending
    scored_songs.sort(key=lambda x: x[1], reverse=True)

    # Apply diversity penalty if enabled (Challenge 3)
    if diversity:
        scored_songs = apply_diversity_penalty(scored_songs)

    return scored_songs[:k]
