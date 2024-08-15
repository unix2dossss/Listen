import abc
from podcast.domainmodel.model import (Author, Podcast, Category, User, PodcastSubscription, Episode, AudioTime,
                                       Comment, Review, Playlist)


repo_instance = None


class RepositoryException(Exception):
    def __init__(self, message=None):
        pass


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def get_n_podcasts(self, n):
        """ Returns n number of articles
        Returns None if the repository is empty.
        """
        raise NotImplementedError
