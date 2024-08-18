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

    @abc.abstractmethod
    def get_podcast(self, pc_id):
        """ Returns a Podcast whose id matches id, from the repository.
        If there are no matches, this method returns an empty list.
        """
        raise NotImplementedError

    def get_popular_categories(self):
        """ return three Popular Categories
        """
        raise NotImplementedError


    def get_editor_picks(self):
        """ return three Editor picked podcasts
        """
        raise NotImplementedError


    def get_podcast_search_list(self):
        """ return a podcast list according to filtered criteria
        """
        raise NotImplementedError


    def get_podcasts_in_category(self, category_name):
        """ return a Podcast list by Category
        """
        raise NotImplementedError

    def get_all_podcasts(self):
        """ return all Podcasts
        """
        raise NotImplementedError

    def get_all_categories(self):
        """ return all Categories
        """
        raise NotImplementedError
