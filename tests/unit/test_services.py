import pytest
from unittest.mock import patch
from flask import session

from podcast.author import services as author_services
from podcast.category import services as category_services
from podcast.discover import services as discover_services
from podcast.home import services as home_services
from podcast.podcastbp import services as podcast_services
from podcast.authentication import services as auth_services
from podcast.playlist import services as playlist_services
from podcast.review import services as review_services
from podcast.utilities import services as util_services
from tests.conftest import in_memory_repo


# author services tests


def test_can_get_all_authors(in_memory_repo):
    # Test retrieval of all authors using the author services.
    authors = author_services.get_all_authors(in_memory_repo)
    assert authors == in_memory_repo.get_all_authors()


# category services tests


def test_can_get_all_categories(in_memory_repo):
    # Test retrieval of all categories using the category services.
    categories = category_services.get_all_categories(in_memory_repo)
    assert categories == in_memory_repo.get_all_categories()


# discover services tests


def test_can_get_popular_categories(in_memory_repo):
    # Test retrieval of popular categories using the discover services.
    popular_categories = discover_services.get_popular_categories(in_memory_repo)
    assert popular_categories == in_memory_repo.get_popular_categories()


def test_can_get_editor_picks(in_memory_repo):
    # Test retrieval of editor's picks using the discover services.
    editor_picks = discover_services.get_editor_picks(in_memory_repo)
    expected_picks = in_memory_repo.get_editor_picks()

    editor_picks_ids = [podcast["id"] for podcast in editor_picks]
    expected_picks_ids = [podcast.id for podcast in expected_picks]

    assert editor_picks_ids == expected_picks_ids


def test_can_get_podcast_search_list(in_memory_repo):
    # Test retrieval of the podcast search list using the discover services.
    podcast_list = discover_services.get_podcast_search_list(in_memory_repo)
    expected_podcast_list = discover_services.format_podcast_list(
        in_memory_repo.get_podcast_search_list(), repo=in_memory_repo
    )
    assert podcast_list == expected_podcast_list


def test_can_get_podcasts_in_category(in_memory_repo):
    # Test retrieval of podcasts within a specified category using the discover services.
    podcast_list = discover_services.get_podcasts_in_category("Comedy", in_memory_repo)
    expected_podcast_list = discover_services.format_podcast_list(
        sorted(in_memory_repo.get_podcasts_in_category("Comedy"))
    )
    assert podcast_list == expected_podcast_list


def test_can_get_all_podcasts(in_memory_repo):
    # Test retrieval of all podcasts using the discover services.
    podcasts = discover_services.get_all_podcasts(in_memory_repo)
    expected_podcasts = discover_services.format_podcast_list(
        sorted(in_memory_repo.get_all_podcasts())
    )
    assert podcasts == expected_podcasts


def test_get_top_podcasts(in_memory_repo):
    # Test retrieval of top podcasts using the discover services.
    top_podcasts = discover_services.get_top_podcasts(in_memory_repo)
    expected_top_podcasts = discover_services.format_podcast_list(
        sorted(in_memory_repo.get_top_podcasts_list())
    )
    assert top_podcasts == expected_top_podcasts


def test_can_get_recently_played_podcasts(in_memory_repo):
    # Test retrieval of recently played podcasts using the discover services.
    recent_podcasts = discover_services.get_recently_played(in_memory_repo)
    expected_recent_podcasts = discover_services.format_podcast_list(
        sorted(in_memory_repo.get_recently_played_list())
    )
    assert recent_podcasts == expected_recent_podcasts


def test_can_get_new_podcasts(in_memory_repo):
    # Test retrieval of new podcasts using the discover services.
    new_podcasts = discover_services.get_new_podcasts(in_memory_repo)
    expected_new_podcasts = discover_services.format_podcast_list(
        sorted(in_memory_repo.get_new_podcasts_list())
    )
    assert new_podcasts == expected_new_podcasts


def test_can_get_podcasts_by_given_author(in_memory_repo):
    # Test retrieval of podcasts by a specific author using the discover services.
    podcast_list = discover_services.get_podcasts_by_author("Audioboom", in_memory_repo)
    expected_podcast_list = discover_services.format_podcast_list(
        sorted(in_memory_repo.get_podcasts_by_author("Audioboom"))
    )
    assert podcast_list == expected_podcast_list


# home services tests


def test_can_get_top_podcasts(in_memory_repo):
    # Test retrieval of top podcasts using the home services.
    top_podcasts = home_services.get_top_podcasts(in_memory_repo)
    expected_podcasts = home_services.format_facet_podcasts(
        in_memory_repo.get_top_podcasts()
    )
    assert top_podcasts == expected_podcasts


def test_can_get_recently_played_podcasts_for_home(in_memory_repo):
    # Test retrieval of recently played podcasts using the home services.
    recent_podcasts = home_services.get_recently_played(in_memory_repo)
    expected_podcasts = home_services.format_facet_podcasts(
        in_memory_repo.get_recently_played()
    )
    assert recent_podcasts == expected_podcasts


def test_can_get_new_podcasts_from_home(in_memory_repo):
    # Test retrieval of new podcasts using the home services.
    new_podcasts = home_services.get_new_podcasts(in_memory_repo)
    expected_podcasts = home_services.format_facet_podcasts(
        in_memory_repo.get_new_podcasts()
    )
    assert new_podcasts == expected_podcasts


def test_can_get_continue_listening_podcasts(in_memory_repo):
    # Test retrieval of continue listening podcasts using the home services.
    continue_listening_podcasts = home_services.get_continue_listening_podcasts(
        in_memory_repo
    )
    expected_podcasts = home_services.format_facet_podcasts(
        sorted(in_memory_repo.get_continue_listening_podcasts()),
        "continue_listening",
        repo=in_memory_repo,
    )
    assert continue_listening_podcasts == expected_podcasts


def test_can_get_top_authors(in_memory_repo):
    # Test retrieval of top authors using the home services.
    top_authors = home_services.get_top_authors(in_memory_repo)
    expected_authors = home_services.format_facet_podcasts(
        authors=in_memory_repo.get_top_authors()
    )
    assert top_authors == expected_authors


# podcast services test


def test_can_get_podcast_by_id(in_memory_repo):
    # Test retrieval of a podcast by ID using the podcast services.
    podcast = podcast_services.get_podcast(2, in_memory_repo)
    assert podcast == in_memory_repo.get_podcast(2)

def test_can_get_podcast_description(my_user, in_memory_repo, client, auth):
    auth.login()

    podcast_id = 2
    podcast = podcast_services.get_podcast(podcast_id, in_memory_repo)

    # Use a request context for session access
    with client.application.test_request_context():
        # Add session data if needed
        session['username'] = my_user.username

        podcast_desc_dict = podcast_services.podcast_about(podcast_id, in_memory_repo)

    assert podcast_desc_dict["podcast_image"] == podcast.image
    assert podcast_desc_dict["podcast_title"] == podcast.title
    assert podcast_desc_dict["podcast_author"] == podcast.author.name
    assert podcast_desc_dict["podcast_description"] == podcast.description
    assert podcast_desc_dict["podcast_language"] == podcast.language
    assert podcast_desc_dict["podcast_website"] == podcast.website


def test_can_get_podcasts_categories(in_memory_repo):
    # Test retrieval of podcast categories using the podcast services.
    expected_categories = []

    for category in in_memory_repo.podcasts[0].categories:
        expected_categories.append({"category_name": category.name})

    podcast_categories_result = podcast_services.podcast_categories(1, in_memory_repo)

    assert podcast_categories_result == expected_categories


def test_can_retrieve_podcasts_episodes(my_user, in_memory_repo, client, auth):
    auth.login()

    # Use a request context for session access
    with client.application.test_request_context():
        # Add session data if needed
        session['username'] = my_user.username

        # Test retrieval of podcast episodes using the podcast services.
        expected_episodes = []
        ep_n = 1

        for episode in sorted(
            in_memory_repo.podcasts[0].episodes,
            key=lambda ep: ep.episode_publish_date,
            reverse=True,
        ):
            episode_dict = dict()

            episode_dict["episode_id"] = episode.episode_id
            episode_dict["episode_number"] = ep_n
            ep_n += 1
            episode_dict["episode_title"] = episode.episode_title
            episode_dict["episode_description"] = episode.episode_description
            episode_dict["episode_date"] = episode.episode_publish_date.strftime("%Y-%m-%d")
            episode_dict["episode_length"] = str(episode.episode_audio_length)
            episode_dict["episode_in_playlist"] = episode.episode_in_playlist

            expected_episodes.append(episode_dict)

        podcast_episodes_result = podcast_services.podcast_episodes(1, in_memory_repo)

    assert podcast_episodes_result == expected_episodes


# ------------- services tests for additional services -------------


# authentication services tests


def test_can_add_new_user(my_user, in_memory_repo):
    new_user_name = my_user.username
    new_password = my_user.password

    auth_services.add_user(new_user_name, new_password, in_memory_repo)

    user_as_dict = auth_services.get_user(new_user_name, in_memory_repo)
    assert user_as_dict['user_name'] == new_user_name

    # Check that password has been encrypted.
    assert user_as_dict['password'].startswith('scrypt:')

    # Verify playlist is added
    playlists = in_memory_repo.get_playlists_for_user(new_user_name)
    assert len(playlists) == 1  # Check that one playlist was created
    assert playlists[0].name == f"{new_user_name.title()}'s Playlist"
    assert playlists[0].user.username == new_user_name


def test_add_user_existing_username(my_user, in_memory_repo):
    existing_user_name = my_user.username
    existing_password = my_user.password

    # Add user
    auth_services.add_user(existing_user_name, existing_password, in_memory_repo)

    # Try to add same username
    with pytest.raises(auth_services.UsernameExistsException):
        auth_services.username_exists(existing_user_name, in_memory_repo)


def test_get_user_success(my_user, in_memory_repo):
    new_user_name = my_user.username
    new_password = my_user.password

    # Add user
    auth_services.add_user(new_user_name, new_password, in_memory_repo)

    # Get user
    user_as_dict = auth_services.get_user(new_user_name, in_memory_repo)
    assert user_as_dict['user_name'] == new_user_name


def test_get_user_unknown_user(in_memory_repo):
    unknown_user_name = 'unknown'

    # Attempt to get an unknown user
    with pytest.raises(auth_services.UnknownUserException):
        auth_services.get_user(unknown_user_name, in_memory_repo)


def test_authenticate_user_valid_credentials(my_user, in_memory_repo):
    new_user_name = my_user.username
    new_password = my_user.password

    # Add user
    auth_services.add_user(new_user_name, new_password, in_memory_repo)

    # Authenticate user
    try:
        auth_services.authenticate_user(new_user_name, new_password, in_memory_repo)
    except auth_services.AuthenticationException:
        assert False


def test_authenticate_user_invalid_password(my_user, in_memory_repo):
    new_user_name = my_user.username
    new_password = my_user.password

    # Add user
    auth_services.add_user(new_user_name, new_password, in_memory_repo)

    # Try to authenticate with an incorrect password
    with pytest.raises(auth_services.AuthenticationException):
        auth_services.authenticate_user(new_user_name, 'WrongPassword123', in_memory_repo)


# playlist services tests

def test_get_user_playlist_podcasts(my_user, my_podcast, in_memory_repo, client, auth):
    auth.login()

    # Add user and create playlist
    auth_services.add_user(my_user.username, my_user.password, in_memory_repo)

    # Add podcasts to user's playlist
    playlist_services.add_to_podcast_playlist(my_user, my_podcast.id, in_memory_repo)

    # Use a request context for session access
    with client.application.test_request_context():
        # Add session data if needed
        session['username'] = my_user.username

        # Get user's playlist podcasts
        pod_in_playlist = playlist_services.get_user_playlist_podcasts(my_user, in_memory_repo)

    assert len(pod_in_playlist) == 1
    assert pod_in_playlist[0]["id"] == 100


def test_get_user_playlist_episodes(in_memory_repo, my_user, my_playlist, my_episode, client, auth):
    auth.login()

    # Add user and create playlist
    auth_services.add_user(my_user.username, my_user.password, in_memory_repo)

    # Add podcasts to user's playlist
    playlist_services.add_to_episode_playlist(my_user, my_episode.episode_id, in_memory_repo)

    # Use a request context for session access
    with client.application.test_request_context():
        # Add session data if needed
        session['username'] = my_user.username

        # Get user's playlist podcasts
        episodes_in_playlist = playlist_services.get_user_playlist_episodes(my_user, in_memory_repo)

    assert len(episodes_in_playlist) == 1
    assert episodes_in_playlist[0]["episode_id"] == 1


def test_can_get_a_user_playlist(my_user, in_memory_repo):
    #Check a user's playlist is retrieved correctly
    user_playlist = playlist_services.get_user_playlist(my_user, in_memory_repo)
    assert user_playlist == in_memory_repo.get_user_playlist(my_user)


def test_can_add_podcast_to_playlist(my_user, my_podcast, in_memory_repo):
    #Add user and create playlist
    auth_services.add_user(my_user.username, my_user.password, in_memory_repo)

    #Get initial size of a user's playlist
    init_playlist_size = playlist_services.get_user_playlist(my_user, in_memory_repo).size()

    #Add a podcast to user's playlist
    playlist_services.add_to_podcast_playlist(my_user, my_podcast.id, in_memory_repo)

    #Check if the size is updated
    updated_playlist_size = playlist_services.get_user_playlist(my_user, in_memory_repo).size()
    assert init_playlist_size + 1 == updated_playlist_size


def test_can_remove_podcast_from_playlist(my_user, my_podcast, in_memory_repo):
    # Add user and create playlist
    auth_services.add_user(my_user.username, my_user.password, in_memory_repo)

    # Get initial size of a user's playlist
    init_playlist_size = playlist_services.get_user_playlist(my_user, in_memory_repo).size()

    # Add a podcast to user's playlist
    playlist_services.add_to_podcast_playlist(my_user, my_podcast.id, in_memory_repo)

    # Remove podcast
    playlist_services.remove_from_podcast_playlist(my_user, my_podcast.id, in_memory_repo)

    # Get updated playlist size
    updated_playlist_size = playlist_services.get_user_playlist(my_user, in_memory_repo).size()

    assert init_playlist_size == updated_playlist_size


def test_can_add_episode_to_playlist(my_user, my_episode, in_memory_repo):
    # Add user and create playlist
    auth_services.add_user(my_user.username, my_user.password, in_memory_repo)

    # Get initial size of a user's playlist
    init_playlist_size = playlist_services.get_user_playlist(my_user, in_memory_repo).size()

    # Add an episode to user's playlist
    playlist_services.add_to_episode_playlist(my_user, my_episode.episode_id, in_memory_repo)

    # Check if the size is updated
    updated_playlist_size = playlist_services.get_user_playlist(my_user, in_memory_repo).size()
    assert init_playlist_size + 1 == updated_playlist_size


def test_can_remove_episode_from_playlist(my_user, my_episode, in_memory_repo):
    # Add user and create playlist
    auth_services.add_user(my_user.username, my_user.password, in_memory_repo)

    # Get initial size of a user's playlist
    init_playlist_size = playlist_services.get_user_playlist(my_user, in_memory_repo).size()

    # Add an episode to user's playlist
    playlist_services.add_to_podcast_playlist(my_user, my_episode.episode_id, in_memory_repo)

    # Remove episode
    playlist_services.remove_from_podcast_playlist(my_user, my_episode.episode_id, in_memory_repo)

    # Get updated playlist size
    updated_playlist_size = playlist_services.get_user_playlist(my_user, in_memory_repo).size()

    assert init_playlist_size == updated_playlist_size


# review services tests


def test_can_get_reviews_of_podcasts(my_podcast, in_memory_repo):
    #Test if all the reviews for a given podcasts are retrieved correctly
    reviews = review_services.get_reviews_of_podcast(my_podcast.id, in_memory_repo)
    assert reviews == in_memory_repo.get_reviews_of_podcast(my_podcast.id)


def test_user_can_add_a_review(my_review, my_podcast, in_memory_repo):
    #Test if a user can add a review for a podcast
    init_review_no = len(review_services.get_reviews_of_podcast(my_podcast.id, in_memory_repo))
    review_services.add_review(my_review, my_podcast.id, in_memory_repo)
    new_review_no = len(review_services.get_reviews_of_podcast(my_podcast.id, in_memory_repo))
    assert init_review_no + 1 == new_review_no


def test_check_user_has_reviewed_podcasts(my_user, my_podcast, my_review, in_memory_repo):
    #Test that user has not reviewed a podcast
    review = review_services.user_has_reviewed_podcast(my_user, my_podcast.id, in_memory_repo)
    assert review == False

    #Test that user has reviewed a podcast
    review_services.add_review(my_review, my_podcast.id, in_memory_repo)
    review = review_services.user_has_reviewed_podcast(my_user, my_podcast.id, in_memory_repo)
    assert review == True


# utilities services tests

def test_if_user_can_be_retrieved_by_username(my_user, in_memory_repo):
    auth_services.add_user(my_user.username, my_user.password, in_memory_repo)
    user = util_services.get_user_by_username(my_user.username, in_memory_repo)
    assert user.id == my_user.id

