import pytest

from podcast.author import services as author_services
from podcast.category import services as category_services
from podcast.discover import services as discover_services
from podcast.home import services as home_services
from podcast.podcastbp import services as podcast_services

#author services tests

def test_can_get_all_authors(in_memory_repo):
    authors = author_services.get_all_authors(in_memory_repo)
    assert authors == in_memory_repo.get_all_authors()

