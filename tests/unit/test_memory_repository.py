from datetime import date, datetime
from typing import List

import pytest

from podcast.domainmodel.model import User, Podcast
from podcast.adapters.repository import RepositoryException


def test_repository_can_retrieve_a_podcast_by_id(in_memory_repo):
    id_no = 1
    podcast = in_memory_repo.get_podcast(id_no)
    assert podcast == in_memory_repo.podcasts[0]



