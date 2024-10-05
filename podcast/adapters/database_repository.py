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

