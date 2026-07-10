from src.recommender import Song, UserProfile, Recommender

def make_small_recommender() -> Recommender:
    songs = [
        Song(
            id=1,
            title="Test Pop Track",
            artist="Test Artist",
            genre="pop",
            mood="happy",
            energy=0.8,
            tempo_bpm=120,
            valence=0.9,
            danceability=0.8,
            acousticness=0.2,
        ),
        Song(
            id=2,
            title="Chill Lofi Loop",
            artist="Test Artist",
            genre="lofi",
            mood="chill",
            energy=0.4,
            tempo_bpm=80,
            valence=0.6,
            danceability=0.5,
            acousticness=0.9,
        ),
    ]
    return Recommender(songs)


def test_recommend_returns_songs_sorted_by_score():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    results = rec.recommend(user, k=2)

    assert len(results) == 2
    # Starter expectation: the pop, happy, high energy song should score higher
    assert results[0].genre == "pop"
    assert results[0].mood == "happy"


def test_explain_recommendation_returns_non_empty_string():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    song = rec.songs[0]

    explanation = rec.explain_recommendation(user, song)
    assert isinstance(explanation, str)
    assert explanation.strip() != ""


def test_acoustic_melancholic_user_prefers_matching_songs():
    songs = [
        Song(
            id=1,
            title="Cure My Tragedy",
            artist="Cold",
            genre="alt-rock",
            mood="melancholic",
            energy=0.6,
            tempo_bpm=100,
            valence=0.28,
            danceability=0.42,
            acousticness=0.30,
        ),
        Song(
            id=2,
            title="Gym Hero",
            artist="Max Pulse",
            genre="pop",
            mood="intense",
            energy=0.93,
            tempo_bpm=132,
            valence=0.77,
            danceability=0.88,
            acousticness=0.05,
        ),
    ]
    user = UserProfile(
        favorite_genre="alt-rock",
        favorite_mood="melancholic",
        target_energy=0.65,
        likes_acoustic=True,
    )
    rec = Recommender(songs)
    results = rec.recommend(user, k=2)

    # Alt-rock melancholic song should rank above pop intense song
    assert results[0].title == "Cure My Tragedy"
    assert results[0].genre == "alt-rock"
