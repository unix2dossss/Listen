from pathlib import Path

from podcast.adapters.repository import AbstractRepository, RepositoryException
from podcast.adapters.datareader.csvdatareader import CSVDataReader
from podcast.domainmodel.model import (Author, Podcast, Category, User, PodcastSubscription, Episode, AudioTime,
                                       Comment, Review, Playlist)


class MemoryRepository(AbstractRepository):
    def __init__(self):
        pass


def populate(data_path: Path, repo: MemoryRepository):
    # create instance of csvreader
    # get data from csv reader
    # repo.set_podcasts, episodes, authors, category, podcasts_by_category.
    pass
