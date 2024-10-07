from typing import Any

from podcast.adapters.repository import AbstractRepository, RepositoryException
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


class MemoryRepository(AbstractRepository):
    def __init__(self):
        self._podcasts = []
        self._episodes = []
        self._authors = {}
        self._categories = {}
        self._podcasts_by_category = {}
        self.__users = []
        self.__playlists = []

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

    @property
    def users(self):
        return self.__users

    # Setter for __users
    @users.setter
    def users(self, value):
        self.__users = value

    @property
    def playlists(self):
        return self.__playlists

    # Setter for __playlists
    @playlists.setter
    def playlists(self, value):
        self.__playlists = value

    def get_n_podcasts(self, n):
        raise NotImplementedError

    def get_podcast(self, pc_id):
        return self._podcasts[pc_id - 1]

    def get_episode(self, ep_id):
        return self._episodes[ep_id - 1]

    def get_popular_categories(self):
        popular_categories = [
            (list(self._categories.values())[1]),
            (list(self._categories.values())[5]),
            (list(self._categories.values())[16]),
        ]
        return popular_categories

    def get_editor_picks(self):
        return [self._podcasts[106], self._podcasts[503], self._podcasts[829]]

    def get_podcast_search_list(self):
        return [
            self._podcasts[288],
            self._podcasts[162],
            self._podcasts[799],
            self._podcasts[317],
        ]

    def get_podcasts_in_category(self, category_name):
        formatted_category_name = category_name.strip()

        if formatted_category_name in self._podcasts_by_category:
            return self._podcasts_by_category[formatted_category_name]

        # Searching with incorrect category_name format
        for category_key in self._podcasts_by_category:
            if formatted_category_name in category_key or formatted_category_name.lower() in category_key.lower():
                return self._podcasts_by_category[category_key]

            # If no exact match, perform a partial match search
            splited_category_name = formatted_category_name.lower().split(" ")
            normalized_category_key = category_key.lower()

            for word in splited_category_name:
                if word in normalized_category_key:
                    return self._podcasts_by_category[category_key]
        return []


    def get_podcasts_by_author(self, author_name):
        formatted_author_name = author_name.strip()

        if formatted_author_name in self._authors:
            return self._authors[formatted_author_name].podcast_list

        specific_authors_podcasts = []
        # Searching with incorrect author_name format
        for author_key in self._authors:
            if formatted_author_name in author_key or formatted_author_name.lower() in author_key.lower():
                for podcast in self._authors[author_key].podcast_list:
                    specific_authors_podcasts.append(podcast)

            # If no exact match, perform a partial match search
            else:
                splited_author_name = formatted_author_name.lower().split(" ")
                normalized_author_key = author_key.lower()

                for word in splited_author_name:
                    if word in normalized_author_key:
                        for podcast in self._authors[author_key].podcast_list:
                            specific_authors_podcasts.append(podcast)
        return specific_authors_podcasts


    def get_all_podcasts(self):
        return self._podcasts

    def get_all_categories(self):
        all_categories = list(self._categories.values())
        return all_categories

    def get_all_authors(self):
        all_authors = list(self._authors.values())
        return all_authors

    def get_top_podcasts(self):
        top_podcasts = [
            self._podcasts[771],
            self._podcasts[531],
            self._podcasts[88],
            self._podcasts[438],
        ]
        return top_podcasts

    def get_recently_played(self):
        recently_played_podcasts = [
            self._podcasts[670],
            self._podcasts[219],
            self._podcasts[728],
            self._podcasts[8],
        ]
        return recently_played_podcasts

    def get_new_podcasts(self):
        new_podcasts = [
            self._podcasts[739],
            self._podcasts[268],
            self._podcasts[639],
            self._podcasts[200],
        ]
        return new_podcasts

    def get_continue_listening_podcasts(self):
        continue_listening_podcasts = [
            self._podcasts[546],
            self._podcasts[823],
            self._podcasts[908],
            self._podcasts[675],
        ]
        return continue_listening_podcasts

    def get_total_audio_time(self, audio_times):
        total_time = AudioTime(0, 0, 0)
        for time in audio_times:
            total_time = total_time.add_time(time)
        return total_time

    def get_top_authors(self):
        # top_authors = list(self._authors.values())[117:120]
        top_authors = [
            list(self._authors.values())[22],
            list(self._authors.values())[45],
            list(self._authors.values())[52],
        ]
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

    def get_podcasts_by_title(self, title):
        return [podcast for podcast in self.podcasts if title.lower() in podcast.title.lower()]

    def add_user(self, user: User):
        self.__users.append(user)

    def add_playlist(self, playlist: Playlist):
        self.__playlists.append(playlist)

    def get_user(self, username: str) -> Any | None:
        for user in self.__users:
            if user.username == username.lower():
                return user
        return None

    def get_reviews_of_podcast(self, pc_id: int):
        podcast = self.get_podcast(pc_id)
        reviews = podcast.reviews
        return reviews

    def add_review(self, review, podcast_id):
        podcast = self.get_podcast(podcast_id)
        podcast.add_review(review)

    def get_user_playlist(self, user: User):
        for playlist in self.__playlists:
            if playlist.user == user:
                return playlist

    def add_podcast_to_playlist(self, playlist: Playlist, podcast: Podcast, user: User):
        playlist.add_podcast_to_playlist(podcast, user)

    def add_episode_to_playlist(self, playlist: Playlist, episode: Episode, user: User):
        playlist.add_episode(episode, user)

    def get_podcast_average_rating(self, podcast_id):
        podcast = self.get_podcast(podcast_id)
        average_rating = None
        total_rating = 0

        if len(podcast.reviews) != 0:
            for review in podcast.reviews:
                total_rating += review.rating
            average_rating = round(total_rating / len(podcast.reviews), 1)

        return average_rating

    def add_podcast(self, podcast):
        self._podcasts.append(podcast)

    def add_episode(self, episode):
        self._episodes.append(episode)



