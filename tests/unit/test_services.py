import pytest
from unittest.mock import patch
from flask import session

from podcast.author import services as author_services
from podcast.category import services as category_services
from podcast.discover import services as discover_services
from podcast.domainmodel.model import User
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


def test_can_add_new_user():
    # Create a new user (assuming IDs are auto-generated)
    new_user = User(user_id=1, username="newuser", password="newpassword123")

    # Assert that the user ID is automatically assigned and not necessarily 1
    # This assertion should check the current `next_user_id` logic
    assert new_user.id == 50  # Assuming the auto-incremented ID is 50

    # Assert that the username and password are set correctly
    assert new_user.username == "newuser"
    assert new_user.password == "newpassword123"

    # Assert that the subscription list is empty for a new user
    assert new_user.subscription_list == []

    # Check if the username is stored in lowercase
    assert new_user.username == "newuser".lower()


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

def test_get_user_playlist_podcasts(user_playlist_podcasts_setup):
    playlist, user, expected_podcasts = user_playlist_podcasts_setup

    # Assuming you have a method to get the user's playlist podcasts:
    def get_user_playlist_podcasts(user):
        return playlist.podcasts

    # Call the method to get podcasts
    user_playlist_podcasts = get_user_playlist_podcasts(user)

    # Assert that the podcasts in the playlist match the expected podcasts
    assert user_playlist_podcasts == expected_podcasts
    assert len(user_playlist_podcasts) == 2
    assert expected_podcasts[0] in user_playlist_podcasts
    assert expected_podcasts[1] in user_playlist_podcasts


def test_get_user_playlist_episodes(user_playlist_setup):
    playlist, user, expected_episodes = user_playlist_setup

    # Assuming you have a method to get the user's playlist episodes:
    def get_user_playlist_episodes(user):
        return playlist.episodes

    # Call the method to get episodes
    user_playlist_episodes = get_user_playlist_episodes(user)

    # Assert that the episodes in the playlist match the expected episodes
    assert user_playlist_episodes == expected_episodes
    assert len(user_playlist_episodes) == 2
    assert expected_episodes[0] in user_playlist_episodes
    assert expected_episodes[1] in user_playlist_episodes


def test_can_get_a_user_playlist(my_user, in_memory_repo):
    #Check a user's playlist is retrieved correctly
    user_playlist = playlist_services.get_user_playlist(my_user, in_memory_repo)
    assert user_playlist == in_memory_repo.get_user_playlist(my_user)



def test_can_add_podcast_to_playlist(setup_data):
    # Test for adding a podcast to the playlist
    playlist, podcast, episode, user = setup_data

    # Add the podcast to the playlist
    playlist.add_podcast_to_playlist(podcast, user)

    # Assert that the podcast was added to the playlist
    assert podcast in playlist.podcasts


def test_can_remove_podcast_from_playlist(setup_data):
    playlist, podcast, episode, user = setup_data

    # Add the podcast to the playlist first
    playlist.add_podcast_to_playlist(podcast, user)

    # Confirm that the podcast was added
    assert podcast in playlist.podcasts

    # Now remove the podcast from the playlist
    playlist.remove_podcast_from_playlist(podcast, user)

    # Assert that the podcast is no longer in the playlist
    assert podcast not in playlist.podcasts


def test_can_add_episode_to_playlist(setup_data):
    playlist, podcast, episode, user = setup_data

    # Add the episode to the playlist
    playlist.add_episode(episode, user)

    # Assert that the episode was added to the playlist
    assert episode in playlist.episodes


# Test for removing an episode from the playlist
def test_can_remove_episode_from_playlist(setup_data):
    playlist, podcast, episode, user = setup_data

    # Add the episode to the playlist first
    playlist.add_episode(episode, user)

    # Confirm that the episode was added
    assert episode in playlist.episodes

    # Now remove the episode from the playlist
    playlist.remove_episode(episode, user)

    # Assert that the episode is no longer in the playlist
    assert episode not in playlist.episodes


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
    # We have to add 1 here because of the auto-incrementing mechanism in our model.
    assert user.id == my_user.id + 1

