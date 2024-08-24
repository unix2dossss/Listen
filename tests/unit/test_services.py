import pytest

from podcast.author import services as author_services
from podcast.category import services as category_services
from podcast.discover import services as discover_services
from podcast.home import services as home_services
from podcast.podcastbp import services as podcast_services


# author services tests

def test_can_get_all_authors(in_memory_repo):
    authors = author_services.get_all_authors(in_memory_repo)
    assert authors == in_memory_repo.get_all_authors()


# category services tests

def test_can_get_all_categories(in_memory_repo):
    categories = category_services.get_all_categories(in_memory_repo)
    assert categories == in_memory_repo.get_all_categories()


# discover services tests

def test_can_get_popular_categories(in_memory_repo):
    popular_categories = discover_services.get_popular_categories(in_memory_repo)
    assert popular_categories == in_memory_repo.get_popular_categories()


def test_can_get_editor_picks(in_memory_repo):
    editor_picks = discover_services.get_editor_picks(in_memory_repo)
    assert editor_picks == in_memory_repo.get_editor_picks()


def test_can_get_podcast_search_list(in_memory_repo):
    podcast_list = discover_services.get_podcast_search_list(in_memory_repo)
    assert podcast_list == in_memory_repo.get_podcast_search_list()


def test_can_get_podcasts_in_category(in_memory_repo):
    podcast_list = discover_services.get_podcasts_in_category('comedy', in_memory_repo)
    assert podcast_list == in_memory_repo.get_podcasts_in_category('comedy')


def test_can_get_all_podcasts(in_memory_repo):
    podcasts = discover_services.get_all_podcasts(in_memory_repo)
    assert podcasts == in_memory_repo.get_all_podcasts()


def test_get_top_podcasts(in_memory_repo):
    top_podcasts = discover_services.get_top_podcasts(in_memory_repo)
    assert top_podcasts == in_memory_repo.get_top_podcasts()


def test_can_get_recently_played_podcasts(in_memory_repo):
    recent_podcasts = discover_services.get_recently_played(in_memory_repo)
    assert recent_podcasts == in_memory_repo.get_recently_played()


def test_can_get_new_podcasts(in_memory_repo):
    new_podcasts = discover_services.get_new_podcasts(in_memory_repo)
    assert new_podcasts == in_memory_repo.get_new_podcasts()


def test_can_get_podcasts_by_given_author(in_memory_repo):
    podcast_list = discover_services.get_podcasts_by_author('audioboom')
    assert podcast_list == in_memory_repo.get_podcasts_by_author('audioboom')


# home services tests

def test_can_get_top_podcasts(in_memory_repo):
    top_podcasts = home_services.get_top_podcasts(in_memory_repo)
    assert top_podcasts == in_memory_repo.get_top_podcasts()


def test_can_get_recently_played_podcasts_for_home(in_memory_repo):
    recent_podcasts = home_services.get_recently_played(in_memory_repo)
    assert recent_podcasts == in_memory_repo.get_recently_played()


def test_can_get_new_podcasts_from_home(in_memory_repo):
    new_podcasts = home_services.get_new_podcasts(in_memory_repo)
    assert new_podcasts == in_memory_repo.get_new_podcasts()


def test_can_get_continue_listening_podcasts(in_memory_repo):
    podcasts = home_services.get_continue_listening_podcasts(in_memory_repo)
    assert podcasts == in_memory_repo.get_continue_listening_podcasts()


def test_can_get_top_authors(in_memory_repo):
    authors = home_services.get_top_authors(in_memory_repo)
    assert authors == in_memory_repo.get_top_authors()


# podcast services test

def test_can_get_podcast_by_id(in_memory_repo):
    podcast = podcast_services.get_podcast(2, in_memory_repo)
    assert podcast == in_memory_repo.get_podcast(2)


def test_can_get_podcast_description(in_memory_repo):
    podcast_id = 2
    podcast = podcast_services.get_podcast(podcast_id, in_memory_repo)

    podcast_desc_dict = podcast_services.podcast_about(podcast_id, in_memory_repo)

    assert podcast_desc_dict["id"] == podcast.id
    assert podcast_desc_dict["podcast_image"] == podcast.image
    assert podcast_desc_dict["podcast_title"] == podcast.title
    assert podcast_desc_dict["podcast_author"] == podcast.author.name
    assert podcast_desc_dict["podcast_description"] == podcast.description
    assert podcast_desc_dict["podcast_language"] == podcast.language
    assert podcast_desc_dict["podcast_website"] == podcast.website

def test_can_get_podcasts_categories(in_memory_repo):
    #To implement
    pass

def test_can_retrieve_podcasts_episodes(in_memory_repo):
    #To implement
    pass