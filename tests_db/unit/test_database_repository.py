from datetime import date, datetime

import pytest

import podcast.adapters.repository as repo
from podcast.adapters.database_repository import SqlAlchemyRepository
from podcast.domainmodel.model import (
    Author,
    Podcast,
    Category,
    User,
    Episode,
    Comment,
    Review,
    Playlist, AudioTime,
)


def test_repository_can_retrieve_podcast(session_factory):
    repo_instance = SqlAlchemyRepository(session_factory)

    podcast = repo_instance.get_podcast(1)

    # Check that the Podcast has the expected attributes.
    assert podcast.title == 'D-Hour Radio Network'
    assert podcast.author.name == 'D Hour Radio Network'
    assert podcast.id == 1


def test_repository_can_retrieve_episode(session_factory):
    repo_instance = SqlAlchemyRepository(session_factory)

    episode = repo_instance.get_episode(1)

    # Check that the Episode has the expected attributes.
    assert episode.episode_title == 'The Mandarian Orange Show Episode 74- Bad Hammer Time, or: 30 Day MoviePass Challenge Part 3'
    assert episode.episode_podcast.title == 'The Mandarian Orange Show'
    assert episode.episode_podcast.id == 14
    assert episode.episode_id == 1


def test_repository_can_retrieve_popular_categories(session_factory):
    repo_instance = SqlAlchemyRepository(session_factory)

    # Test retrieval of the most popular categories.
    popular_categories = repo_instance.get_popular_categories()

    print(popular_categories)
    print(":)))")


    assert popular_categories[0].name == 'Personal Journals'
    assert popular_categories[1].name == 'Comedy'
    # assert popular_categories[2].name == 'Tech News'

def test_can_retrieve_editor_picks(session_factory):
    repo_instance = SqlAlchemyRepository(session_factory)

    # Test retrieval of podcasts that are editor's picks.
    podcasts = repo_instance.get_editor_picks()


    assert podcasts[0].title == 'Animal Talk Naturally'
    assert podcasts[1].title == 'Purple Reign Show'
    assert podcasts[2].title == 'BRAWLcast'


def test_can_retrieve_podcast_search_list(session_factory):
    repo_instance = SqlAlchemyRepository(session_factory)

    # Test retrieval of a list of podcasts for search functionality.
    podcasts = repo_instance.get_podcast_search_list()

    assert podcasts[0].title == 'PopBuzz Podcast'
    assert podcasts[1].title == 'Spirit of the Endeavor'
    assert podcasts[2].title == 'Lakeviews'


def test_can_get_podcasts_in_specified_category(session_factory):
    repo_instance = SqlAlchemyRepository(session_factory)

    # Test retrieval of podcasts within a specified category.
    podcasts = repo_instance.get_podcasts_in_category("Comedy")

    assert len(podcasts) == 135


def test_can_retrieve_podcasts_by_specified_author(session_factory):
    repo_instance = SqlAlchemyRepository(session_factory)

    # Test retrieval of podcasts by a specific author.
    author_name = "Audioboom"
    podcasts = repo_instance.get_podcasts_by_author(author_name)

    assert len(podcasts) == 13


def test_can_retrieve_all_podcasts(session_factory):
    repo_instance = SqlAlchemyRepository(session_factory)

    # Test retrieval of all podcasts in the repository.
    podcasts = repo_instance.get_all_podcasts()

    assert len(podcasts) == 1000


def test_can_retrieve_all_categories(session_factory):
    repo_instance = SqlAlchemyRepository(session_factory)

    # Test retrieval of all categories in the repository.
    podcasts = repo_instance.get_all_categories()

    assert len(podcasts) == 65
    assert podcasts[64].name == "Islam"


def test_can_retrieve_all_authors(session_factory):
    repo_instance = SqlAlchemyRepository(session_factory)

    # Test retrieval of all authors in the repository.
    authors = repo_instance.get_all_authors()

    assert len(authors) == 955
    assert authors[954].name == 'Just GQ & International P'


def test_can_retrieve_top_podcasts(session_factory):
    repo_instance = SqlAlchemyRepository(session_factory)

    # Test retrieval of top podcasts based on some criteria.
    podcasts = repo_instance.get_top_podcasts()

    assert podcasts[0].title == 'The Alt-Country Show'
    assert podcasts[1].title == 'Super Hopped-Up'
    assert podcasts[2].title == 'Our World Network'


def test_can_retrieve_recently_played_podcasts(session_factory):
    repo_instance = SqlAlchemyRepository(session_factory)

    # Test retrieval of recently played podcasts.
    podcasts = repo_instance.get_recently_played()

    assert podcasts[0].title == 'Faith Baptist Church'
    assert podcasts[1].title == 'In Our Time: Culture'
    assert podcasts[2].title == 'DADicated podcast'


def test_can_retrieve_new_podcasts(session_factory):
    repo_instance = SqlAlchemyRepository(session_factory)

    # Test retrieval of newly added podcasts.
    podcasts = repo_instance.get_new_podcasts()

    assert podcasts[0].title == 'Kinda Funny Morning Show'
    assert podcasts[1].title == "Hangin' With The 'Boys"
    assert podcasts[2].title == 'Learn to Code With Me'


def test_can_retrieve_continue_listening_podcasts(session_factory):
    repo_instance = SqlAlchemyRepository(session_factory)

    # Test retrieval of podcasts in the continue listening list.
    podcasts = repo_instance.get_continue_listening_podcasts()

    assert podcasts[0].title == 'AquaBlack'
    assert podcasts[1].title == 'Nerdy Legion'
    assert podcasts[2].title == 'Comics Dash'


def test_total_audio_time_addition(session_factory):
    repo_instance = SqlAlchemyRepository(session_factory)

    # Test the addition of audio times for a list of podcasts.
    audio_time_1 = AudioTime(1, 30, 0)
    audio_time_2 = AudioTime(0, 30, 0)
    total_time = repo_instance.get_total_audio_time([audio_time_1, audio_time_2])
    assert total_time.colon_format() == "02:00:00"

    # Test handling of incorrect types in audio time addition.
    with pytest.raises(TypeError):
        total_time2 = repo_instance.get_total_audio_time([audio_time_1, 1])


def test_can_retrieve_top_authors(session_factory):
    repo_instance = SqlAlchemyRepository(session_factory)

    # Test retrieval of top authors based on some criteria.
    top_authors = repo_instance.get_top_authors()

    assert top_authors[0].name == 'Audioboom'
    assert top_authors[1].name == 'Leo Laporte'
    assert top_authors[2].name == 'BBC'


def test_can_add_new_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    #Test if user can be added successfully.
    user = User(1, 'Dave', '123456789')
    repo.add_user(user)

    repo.add_user(User(2, 'Martin', '123456789'))

    user2 = repo.get_user('Dave')

    assert user2 == user and user2 is user


def test_repository_can_retrieve_a_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = User(1, 'Dave', '123456789')
    repo.add_user(user)
    retrieved_user = repo.get_user('Dave')

    assert retrieved_user == user

def test_can_add_playlist(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = User(1, 'Dave', '123456789')

    playlist = Playlist(1, user, 'Moo')
    repo.add_playlist(playlist)

    playlist2 = repo.get_user_playlist(user)

    assert playlist2.name == playlist.name and playlist2 is playlist


def test_repository_can_retrieve_a_playlist(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = User(1, 'Dave', '123456789')

    playlist = Playlist(1, user, 'Moo')
    repo.add_playlist(playlist)
    retrieved_playlist = repo.get_user_playlist(user)

    assert retrieved_playlist == playlist


def test_can_add_review(session_factory):
    repo_instance = SqlAlchemyRepository(session_factory)
    author = Author(1, "Joe Toste")
    podcast = Podcast(100, author, "Joe Toste Podcast - Sales Training Expert")
    user = User(1, 'Dave', '123456789')
    comment = Comment(user, "Good!", None)
    review = Review(user, comment)

    # Test if review is added successfully
    init_reviews = len(repo_instance.get_reviews_of_podcast(podcast.id))
    repo_instance.add_review(review, podcast.id)
    new_reviews = len(repo_instance.get_reviews_of_podcast(podcast.id))

    assert init_reviews == new_reviews

def test_can_add_podcast(session_factory):
    repo_instance = SqlAlchemyRepository(session_factory)
    author = Author(1, "Jane Toste")
    podcast = Podcast(100, author, "Joe Toste Podcast - Sales Training Expert")

    # Test if podcast is added successfully
    repo_instance.add_podcast(podcast)
    retrieved_podcast = repo_instance.get_podcast(100)

    assert retrieved_podcast == podcast

