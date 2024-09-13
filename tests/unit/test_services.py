import pytest

from podcast.author import services as author_services
from podcast.category import services as category_services
from podcast.discover import services as discover_services
from podcast.home import services as home_services
from podcast.podcastbp import services as podcast_services


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


def test_can_get_podcast_description(in_memory_repo):
    # Test retrieval of podcast description using the podcast services.
    podcast_id = 2
    podcast = podcast_services.get_podcast(podcast_id, in_memory_repo)

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


def test_can_retrieve_podcasts_episodes(in_memory_repo):
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

        expected_episodes.append(episode_dict)

    podcast_episodes_result = podcast_services.podcast_episodes(1, in_memory_repo)

    assert podcast_episodes_result == expected_episodes
