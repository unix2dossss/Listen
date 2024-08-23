from datetime import date, datetime
from typing import List

import pytest

from podcast.domainmodel.model import User, Podcast
from podcast.adapters.repository import RepositoryException


def test_repository_can_retrieve_a_podcast_by_id(in_memory_repo):
    id_no = 1
    podcast = in_memory_repo.get_podcast(id_no)
    assert podcast == in_memory_repo.podcasts[0]


def test_repository_can_retrieve_popular_categories(in_memory_repo):
    popular_categories = in_memory_repo.get_popular_categories()
    assert popular_categories == [in_memory_repo.categories.values()[1], in_memory_repo.categories.values()[5],
                                  in_memory_repo.categories.values()[16]]


def test_can_retrieve_editor_picks(in_memory_repo):
    editor_picks = in_memory_repo.get_editor_picks()
    assert editor_picks == [[in_memory_repo.podcasts[288], in_memory_repo.podcasts[162], in_memory_repo.podcasts[799],
                             in_memory_repo.podcasts[317]]]


def test_can_get_podcasts_in_specified_category(in_memory_repo):
    comedy_podcasts = in_memory_repo.get_podcasts_in_category('comedy')
    assert comedy_podcasts == in_memory_repo.podcasts_by_category['comedy']


def test_can_retrieve_podcasts_by_specified_author(in_memory_repo):
    author_name = "audioboom"
    audioboom_podcasts = in_memory_repo.get_podcasts_by_author(author_name)
    assert audioboom_podcasts == in_memory_repo.authors[author_name].podcast_list


def test_can_retrieve_all_podcasts(in_memory_repo):
    all_podcasts = in_memory_repo.get_all_podcasts()
    assert all_podcasts == in_memory_repo.podcasts


def test_can_retrieve_all_categories(in_memory_repo):
    all_categories = in_memory_repo.get_all_categories()
    assert all_categories == in_memory_repo.categories.values()

def test_can_retrieve_all_authors(in_memory_repo):
    all_authors = in_memory_repo.get_all_authors()
    assert all_authors == in_memory_repo.authors.values()

