"""
Command line runner for the Music Recommender Simulation.

Supports multiple scoring strategies and formatted table output.
"""

from recommender import load_songs, recommend_songs, STRATEGIES


def print_table(recommendations: list, strategy_name: str, user_prefs: dict) -> None:
    """Print recommendations as a formatted ASCII table (Challenge 4)."""
    print(f"\n{'=' * 90}")
    print(f"  Strategy: {strategy_name}")
    print(f"  Profile:  genre={user_prefs['genre']}, mood={user_prefs['mood']}, "
          f"energy={user_prefs['energy']}, acoustic={user_prefs['likes_acoustic']}")
    print(f"{'=' * 90}")
    print(f"  {'#':<3} {'Title':<30} {'Artist':<22} {'Score':<7} {'Reasons'}")
    print(f"  {'-' * 3} {'-' * 30} {'-' * 22} {'-' * 7} {'-' * 25}")

    for i, (song, score, explanation) in enumerate(recommendations, 1):
        title = song['title'][:28]
        artist = song['artist'][:20]
        print(f"  {i:<3} {title:<30} {artist:<22} {score:<7.2f} {explanation}")

    print()


def run_profile(name: str, user_prefs: dict, songs: list, strategy_key: str = "mood-first") -> None:
    """Run the recommender for a given profile and strategy."""
    strategy = STRATEGIES[strategy_key]
    recommendations = recommend_songs(user_prefs, songs, k=5, strategy=strategy, diversity=True)
    print_table(recommendations, f"{name} ({strategy.name()})", user_prefs)


def main() -> None:
    songs = load_songs("data/songs.csv")

    # === Your profile across all 3 strategies ===
    my_prefs = {
        "genre": "alt-rock",
        "mood": "melancholic",
        "energy": 0.65,
        "likes_acoustic": True,
    }

    print("\n" + "=" * 90)
    print("  COMPARING SCORING STRATEGIES - Same profile, different modes")
    print("=" * 90)

    for strategy_key in STRATEGIES:
        run_profile("My Profile", my_prefs, songs, strategy_key)

    # === Diverse profiles with default (Mood-First) strategy ===
    print("\n" + "=" * 90)
    print("  DIVERSE PROFILE STRESS TEST - Mood-First strategy")
    print("=" * 90)

    profiles = [
        ("High-Energy Pop Lover", {
            "genre": "pop",
            "mood": "happy",
            "energy": 0.9,
            "likes_acoustic": False,
        }),
        ("Chill Lofi Listener", {
            "genre": "lofi",
            "mood": "chill",
            "energy": 0.35,
            "likes_acoustic": True,
        }),
        ("Edge Case: High Energy + Heartbreak", {
            "genre": "pop",
            "mood": "heartbreak",
            "energy": 0.9,
            "likes_acoustic": False,
        }),
    ]

    for name, prefs in profiles:
        run_profile(name, prefs, songs)


if __name__ == "__main__":
    main()
