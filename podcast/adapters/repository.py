import abc
from podcast.domainmodel.model import (
    Author,
    Podcast,
    Category,
    User,
    PodcastSubscription,
    Episode,
    AudioTime,
    Comment,
    Review,
    Playlist,
)


repo_instance = None


class RepositoryException(Exception):
    def __init__(self, message=None):
        pass


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def get_n_podcasts(self, n):
        """Returns n number of articles
        Returns None if the repository is empty.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_podcast(self, pc_id):
        """Returns a Podcast whose id matches id, from the repository.
        If there are no matches, this method returns an empty list.
        """
        raise NotImplementedError

    def get_popular_categories(self):
        """return three Popular Categories"""
        raise NotImplementedError

    def get_editor_picks(self):
        """return three Editor picked podcasts"""
        raise NotImplementedError

    def get_podcast_search_list(self):
        """return a podcast list according to filtered criteria"""
        raise NotImplementedError

    def get_podcasts_in_category(self, category_name):
        """return a Podcast list by Category"""
        raise NotImplementedError

    def get_podcasts_by_author(self, author_name):
        """ return a Podcast list by Category
        """
        raise NotImplementedError

    def get_all_podcasts(self):
        """return all Podcasts"""
        raise NotImplementedError

    def get_all_categories(self):
        """return all Categories"""
        raise NotImplementedError

    def get_all_authors(self):
        """return all Categories"""
        raise NotImplementedError

    def get_top_podcasts(self):
        """return top podcasts"""
        raise NotImplementedError

    def get_recently_played(self):
        """return recently played podcasts"""
        raise NotImplementedError

    def get_new_podcasts(self):
        """return new podcasts"""
        raise NotImplementedError

    def get_continue_listening_podcasts(self):
        """return a list of continue listening podcasts"""
        raise NotImplementedError

    def get_top_authors(self):
        """return a list of top authors"""
        raise NotImplementedError

    def get_total_audio_time(self, audio_times):
        """return a list of top authors"""
        raise NotImplementedError

    def get_top_podcasts_list(self):
        """return a top podcasts list for show all"""
        raise NotImplementedError

    def get_recently_played_list(self):
        """return a recently played podcasts list for show all"""
        raise NotImplementedError

    def get_new_podcasts_list(self):
        """return a new podcasts list for show all"""
        raise NotImplementedError

    def add_user(self, user: User):
        """add a user"""
        raise NotImplementedError

    def get_user(self, user_name):
        """get a user"""
        raise NotImplementedError

    def get_reviews_of_podcast(self, pc_id):
        """get a reviews of a podcast"""
        raise NotImplementedError

    def add_review(self, review, podcast_id):
        """add review to podcast"""
        raise NotImplementedError

    def get_podcast_average_rating(self, podcast_id):
        """get average rating of a podcast"""
        raise NotImplementedError

    def add_playlist(self, playlist):
        """add review to podcast"""
        raise NotImplementedError

    def get_user_playlist(self, user: User):
        """add review to podcast"""
        raise NotImplementedError

    def get_episode(self, param):
        """add review to podcast"""
        raise NotImplementedError

    def get_podcasts_by_title(self, title):
        """ return all the podcasts that have the argument string as part of the podcast title
        """
        raise NotImplementedError

    def add_multiple_authors(self, authors):
        """add multiple authors to populate repo"""
        raise NotImplementedError

    def add_multiple_categories(self, categories):
        """add multiple categories to populate repo"""
        raise NotImplementedError

    def add_multiple_podcasts(self, podcasts):
        """add multiple podcasts to populate repo"""
        raise NotImplementedError

    def add_multiple_episodes(self, episodes):
        """add multiple episodes to populate repo"""
        raise NotImplementedError
