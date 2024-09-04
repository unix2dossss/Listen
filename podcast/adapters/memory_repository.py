from pathlib import Path

from podcast.adapters.repository import AbstractRepository, RepositoryException
from podcast.adapters.datareader.csvdatareader import CSVDataReader
from podcast.domainmodel.model import (Author, Podcast, Category, User, PodcastSubscription, Episode, AudioTime,
                                       Comment, Review, Playlist)


class MemoryRepository(AbstractRepository):
    def __init__(self):
        self._podcasts = []
        self._episodes = []
        self._authors = {}
        self._categories = {}
        self._podcasts_by_category = {}
        self.__users = []

    # Getter for _podcasts
    @property
    def podcasts(self):
        return self._podcasts

    # Setter for _podcasts
    @podcasts.setter
    def podcasts(self, value):
        self._podcasts = value

    # Getter for _episodes
    @property
    def episodes(self):
        return self._episodes

    # Setter for _episodes
    @episodes.setter
    def episodes(self, value):
        self._episodes = value

    # Getter for _authors
    @property
    def authors(self):
        return self._authors

    # Setter for _authors
    @authors.setter
    def authors(self, value):
        self._authors = value

    # Getter for _categories
    @property
    def categories(self):
        return self._categories

    # Setter for _categories
    @categories.setter
    def categories(self, value):
        self._categories = value

    # Getter for _podcasts_by_category
    @property
    def podcasts_by_category(self):
        return self._podcasts_by_category

    # Setter for _podcasts_by_category
    @podcasts_by_category.setter
    def podcasts_by_category(self, value):
        self._podcasts_by_category = value

    def get_n_podcasts(self, n):
        raise NotImplementedError

    def get_podcast(self, pc_id):
        return self._podcasts[pc_id-1]

    def get_popular_categories(self):
        popular_categories = [(list(self._categories.values())[1]), (list(self._categories.values())[5]), (list(self._categories.values())[16])]
        return popular_categories

    def get_editor_picks(self):
        return [self._podcasts[106], self._podcasts[503], self._podcasts[829]]

    def get_podcast_search_list(self):
        return [self._podcasts[288], self._podcasts[162], self._podcasts[799], self._podcasts[317]]

    def get_podcasts_in_category(self, category_name):
        return self._podcasts_by_category[category_name]

    def get_podcasts_by_author(self, author_name):
        return self._authors[author_name].podcast_list

    def get_all_podcasts(self):
        return self._podcasts

    def get_all_categories(self):
        all_categories = list(self._categories.values())
        return all_categories

    def get_all_authors(self):
        all_authors = list(self._authors.values())
        return all_authors

    def get_top_podcasts(self):
        top_podcasts = [self._podcasts[771], self._podcasts[531], self._podcasts[88], self._podcasts[438]]
        return top_podcasts

    def get_recently_played(self):
        recently_played_podcasts = [self._podcasts[670], self._podcasts[219], self._podcasts[728], self._podcasts[8]]
        return recently_played_podcasts

    def get_new_podcasts(self):
        new_podcasts = [self._podcasts[739], self._podcasts[268], self._podcasts[639], self._podcasts[200]]
        return new_podcasts

    def get_continue_listening_podcasts(self):
        continue_listening_podcasts = [self._podcasts[546], self._podcasts[823], self._podcasts[908], self._podcasts[675]]
        return continue_listening_podcasts

    def get_total_audio_time(self, audio_times):
        total_time = AudioTime(0, 0, 0)
        for time in audio_times:
            total_time = total_time.add_time(time)
        return total_time

    def get_top_authors(self):
        # top_authors = list(self._authors.values())[117:120]
        top_authors = [list(self._authors.values())[22], list(self._authors.values())[45], list(self._authors.values())[52]]
        return top_authors

    def get_top_podcasts_list(self):
        top_podcasts = self._podcasts[162:174]
        return top_podcasts

    def get_recently_played_list(self):
        recently_played_podcasts = self._podcasts[44:56]
        return recently_played_podcasts

    def get_new_podcasts_list(self):
        new_podcasts = self._podcasts[280:292]
        return new_podcasts

    def add_user(self, user: User):
        self.__users.append(user)


def populate(data_path: Path, repo: MemoryRepository):
    # create instance of csvreader
    podcasts_csv_path = data_path / "podcasts.csv"
    episodes_csv_path = data_path / "episodes.csv"

    csvdatareader_instance = CSVDataReader(podcasts_csv_path, episodes_csv_path)

    repo.podcasts = csvdatareader_instance.podcasts
    repo.episodes = csvdatareader_instance.episodes
    repo.authors = csvdatareader_instance.authors
    repo.categories = csvdatareader_instance.categories
    repo.podcasts_by_category = csvdatareader_instance.podcasts_by_category
