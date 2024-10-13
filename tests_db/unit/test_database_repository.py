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

    episode = repo_instance.get_episode(5079)

    # Check that the Episode has the expected attributes.
    assert episode.episode_title == 'The Tuesday Spot Feat...Harold Branch aka HB and Tamika (Georgia Me) Harper'
    assert episode.episode_podcast.title == 'D-Hour Radio Network'
    assert episode.episode_podcast.id == 1
    assert episode.episode_id == 5079


def test_repository_can_retrieve_popular_categories(session_factory):
    repo_instance = SqlAlchemyRepository(session_factory)

    # Test retrieval of the most popular categories.
    popular_categories = repo_instance.get_popular_categories()

    assert popular_categories[0].name == 'Personal Journals'
    assert popular_categories[1].name == 'Comedy'


def test_can_retrieve_editor_picks(session_factory):
    repo_instance = SqlAlchemyRepository(session_factory)

    # simulate retreival of editor picks:
    session = session_factory()  # Open a new session
    podcasts = session.query(Podcast).filter(Podcast._id.in_([1, 2])).all()

    assert podcasts[0].title == 'D-Hour Radio Network'
    assert podcasts[1].title == 'Brian Denny Radio'


def test_can_retrieve_podcast_search_list(session_factory):
    repo_instance = SqlAlchemyRepository(session_factory)

    # Test retrieval of a list of podcasts for search functionality.
    podcasts = repo_instance.get_podcast_search_list()

    # simulate retreival of search list:
    session = session_factory()  # Open a new session
    podcasts = session.query(Podcast).filter(Podcast._id.in_([1, 2])).all()

    assert podcasts[0].title == 'D-Hour Radio Network'
    assert podcasts[1].title == 'Brian Denny Radio'


def test_can_get_podcasts_in_specified_category(session_factory):
    repo_instance = SqlAlchemyRepository(session_factory)

    # Test retrieval of podcasts within a specified category.
    podcasts = repo_instance.get_podcasts_in_category("Comedy")

    assert len(podcasts) == 1


def test_can_retrieve_podcasts_by_specified_author(session_factory):
    repo_instance = SqlAlchemyRepository(session_factory)

    # Test retrieval of podcasts by a specific author.
    author_name = "Audioboom"
    podcasts = repo_instance.get_podcasts_by_author(author_name)

    # simulate retreival of authors podcast list:
    session = session_factory()  # Open a new session
    authors = session.query(Author).filter(Author._id.in_([1, 2])).all()

    author1_podcast_list = authors[0].podcast_list
    author2_podcast_list = authors[1].podcast_list

    assert author1_podcast_list[0].title == 'D-Hour Radio Network'
    assert author2_podcast_list[0].title == 'Brian Denny Radio'

    assert len(authors) == 2


def test_can_retrieve_all_podcasts(session_factory):
    repo_instance = SqlAlchemyRepository(session_factory)

    # Test retrieval of all podcasts in the repository.
    podcasts = repo_instance.get_all_podcasts()

    assert len(podcasts) == 2


def test_can_retrieve_all_categories(session_factory):
    repo_instance = SqlAlchemyRepository(session_factory)

    # Test retrieval of all categories in the repository.
    podcasts = repo_instance.get_all_categories()

    assert len(podcasts) == 6
    assert podcasts[5].name == "Comedy"


def test_can_retrieve_all_authors(session_factory):
    repo_instance = SqlAlchemyRepository(session_factory)

    # simulate retreival of all authors list:
    session = session_factory()  # Open a new session
    authors = session.query(Author).filter(Author._id.in_([1, 2])).all()

    assert authors[0].name == 'D Hour Radio Network'
    assert authors[1].name == 'Brian Denny'


def test_can_retrieve_top_podcasts(session_factory):
    repo_instance = SqlAlchemyRepository(session_factory)

    # simulate retreival of top podcasts list:
    session = session_factory()  # Open a new session
    podcasts = session.query(Podcast).filter(Podcast._id.in_([1, 2])).all()

    assert podcasts[0].title == 'D-Hour Radio Network'
    assert podcasts[1].title == 'Brian Denny Radio'


def test_can_retrieve_recently_played_podcasts(session_factory):
    repo_instance = SqlAlchemyRepository(session_factory)

    # simulate retreival of recent played podcasts:
    session = session_factory()  # Open a new session
    podcasts = session.query(Podcast).filter(Podcast._id.in_([1, 2])).all()

    assert podcasts[0].title == 'D-Hour Radio Network'
    assert podcasts[1].title == 'Brian Denny Radio'


def test_can_retrieve_new_podcasts(session_factory):
    repo_instance = SqlAlchemyRepository(session_factory)

    # simulate retreival of new podcasts:
    session = session_factory()  # Open a new session
    podcasts = session.query(Podcast).filter(Podcast._id.in_([1, 2])).all()

    assert podcasts[0].title == 'D-Hour Radio Network'
    assert podcasts[1].title == 'Brian Denny Radio'


def test_can_retrieve_continue_listening_podcasts(session_factory):
    repo_instance = SqlAlchemyRepository(session_factory)

    # simulate retreival of new podcasts:
    session = session_factory()  # Open a new session
    podcasts = session.query(Podcast).filter(Podcast._id.in_([1, 2])).all()

    assert podcasts[0].title == 'D-Hour Radio Network'
    assert podcasts[1].title == 'Brian Denny Radio'


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

    # simulate retreival of top authors list:
    session = session_factory()  # Open a new session
    authors = session.query(Author).filter(Author._id.in_([1, 2])).all()

    assert authors[0].name == 'D Hour Radio Network'
    assert authors[1].name == 'Brian Denny'


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

