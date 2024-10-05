from sqlalchemy import func
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import scoped_session
from abc import ABC
from typing import List, Type

from podcast import Podcast, Author
from podcast.adapters.repository import AbstractRepository
from podcast.domainmodel.model import Category, Episode


class SessionContextManager:
    def __init__(self, session_factory):
        self.__session_factory = session_factory
        self.__session = scoped_session(self.__session_factory)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    @property
    def session(self):
        return self.__session

    def commit(self):
        self.__session.commit()

    def rollback(self):
        self.__session.rollback()

    def reset_session(self):
        # this method can be used e.g. to allow Flask to start a new session for each http request,
        # via the 'before_request' callback
        self.close_current_session()
        self.__session = scoped_session(self.__session_factory)

    def close_current_session(self):
        if not self.__session is None:
            self.__session.close()


class SqlAlchemyRepository(AbstractRepository, ABC):

    def __init__(self, session_factory):
        self._session_cm = SessionContextManager(session_factory)

    def close_session(self):
        self._session_cm.close_current_session()

    def reset_session(self):
        self._session_cm.reset_session()

    # Methods to populate database
    def add_multiple_authors(self, authors):
        with self._session_cm as scm:
            with scm.session.no_autoflush:
                for author in authors:
                    if author is None:
                        raise ValueError("Author name cannot be None")
                    scm.session.add(authors[author])
            scm.commit()

    def add_multiple_categories(self, categories):
        with self._session_cm as scm:
            with scm.session.no_autoflush:
                for category in categories:
                    scm.session.add(categories[category])
            scm.commit()

    def add_multiple_podcasts(self, podcasts: List[Podcast]):
        with self._session_cm as scm:
            for podcast in podcasts:
                scm.session.add(podcast)
            scm.commit()

    def add_multiple_episodes(self, episode: List[Episode]):
        with self._session_cm as scm:
            for episode in episode:
                scm.session.merge(episode)
            scm.commit()

    # Database implementations (of memory repository methods)
    def get_n_podcasts(self):
        # Your code here that fetches the required number of podcasts
        pass

    def get_podcast(self, pc_id):
        podcast = None
        try:
            query = self._session_cm.session.query(Podcast).filter(
                Podcast._id == pc_id)
            podcast = query.one()
        except NoResultFound:
            print(f'Podcast {pc_id} was not found')

        return podcast

    def get_popular_categories(self):
        try:
            popular_categories = self._session_cm.session.query(Category).filter(
                Category.id.in_([1, 5, 16])
            ).all()
        except NoResultFound:
            print(f'Categories with ids"{1, 5, 16}" was not found')
            return []

        return popular_categories


    def get_editor_picks(self):
        try:
            editor_picks = self._session_cm.session.query(Podcast).filter(
                Podcast.id.in_([106, 503, 829])
            ).all()
        except NoResultFound:
            print(f'Podcasts with ids"{106, 503, 829}" was not found')
            return []

        return editor_picks


    def get_podcast_search_list(self):
        try:
            podcast_search_list = self._session_cm.session.query(Podcast).filter(
                Podcast.id.in_([288, 162, 799, 317])
            ).all()
        except NoResultFound:
            print(f'Podcasts with ids"{288, 162, 799, 317}" was not found')
            return []

        return podcast_search_list


    def get_podcasts_in_category(self, category_name):
        formatted_category_name = category_name.strip()

        try:
            # Try to query the category by exact name
            category = self._session_cm.session.query(Category).filter(Category.name == formatted_category_name).first()

            if category:
                # If the category exists, retrieve the podcasts associated with it
                return self._session_cm.session.query(Podcast).join(Category).filter(Category.id == category.id).all()

            # If no exact match, perform a case-insensitive partial search
            categories = self._session_cm.session.query(Category).filter(
                Category.name.ilike(f"%{formatted_category_name}%")
            ).all()

            podcasts = []
            for c in categories:
                category_podcasts = self._session_cm.session.query(Podcast).join(Category).filter(
                    Category.id == c.id).all()
                podcasts.extend(category_podcasts)

            return podcasts

        except Exception as e:
            print(f"An error occurred while retrieving podcasts: {e}")
            return []


    def get_podcasts_by_author(self, author_name):
        formatted_author_name = author_name.strip()
        try:
            searched_podcasts = self._session_cm.session.query(Podcast).join(Author).filter(
                func.lower(Author.name).like(f"%{formatted_author_name}%")
            ).all()
        except NoResultFound:
            print(f'Author "{formatted_author_name}" was not found')
            return []

        return searched_podcasts


    def get_all_podcasts(self):
        podcasts = self._session_cm.session.query(Podcast).all()
        return podcasts

    def get_all_categories(self):
        categories = self._session_cm.session.query(Category).all()
        return categories

    def get_all_authors(self):
        authors = self._session_cm.session.query(Author).all()
        return authors

    def get_top_podcasts(self):
        try:
            top_podcasts = self._session_cm.session.query(Podcast).filter(
                Podcast.id.in_([771, 531, 88, 438])
            ).all()
        except NoResultFound:
            print(f'Podcasts with ids "{771, 531, 88, 438}" were not found')
            return []

        return top_podcasts

    def get_recently_played(self):
        try:
            recently_played_podcasts = self._session_cm.session.query(Podcast).filter(
                Podcast.id.in_([670, 219, 728, 8])
            ).all()
        except NoResultFound:
            print(f'Podcasts with ids "{670, 219, 728, 8}" were not found')
            return []

        return recently_played_podcasts


    def get_new_podcasts(self):
        try:
            new_podcasts = self._session_cm.session.query(Podcast).filter(
                Podcast.id.in_([739, 268, 639, 200])
            ).all()
        except NoResultFound:
            print(f'Podcasts with ids "{739, 268, 639, 200}" were not found')
            return []

        return new_podcasts

    def get_continue_listening_podcasts(self):
        try:
            continue_listening_podcasts = self._session_cm.session.query(Podcast).filter(
                Podcast.id.in_([546, 823, 908, 675])
            ).all()
        except NoResultFound:
            print(f'Podcasts with ids "{546, 823, 908, 675}" were not found')
            return []

        return continue_listening_podcasts


    # Need to do this

    # def get_total_audio_time(self, audio_times):
    #     total_time = AudioTime(0, 0, 0)
    #     for time in audio_times:
    #         total_time = total_time.add_time(time)
    #     return total_time






