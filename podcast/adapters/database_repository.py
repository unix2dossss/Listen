from sqlalchemy import func, delete
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import scoped_session
from abc import ABC
from typing import List, Type, Any

from podcast import Podcast, Author
from podcast.adapters.orm import podcast_categories_table, podcast_users_table, episode_users_table
from podcast.adapters.repository import AbstractRepository
from podcast.domainmodel.model import Category, Episode, User, Playlist, Review, AudioTime


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

    def get_episode(self, ep_id):
        episode = None
        try:
            query = self._session_cm.session.query(Episode).filter(
                Episode._episode_id == ep_id)
            episode = query.one()
        except NoResultFound:
            print(f'Podcast {ep_id} was not found')

        return episode

    def get_popular_categories(self) -> List[Category]:
        try:
            popular_categories = self._session_cm.session.query(Category).filter(
                Category._id.in_([1, 5, 16])
            ).all()
        except NoResultFound:
            print(f'Categories with ids"{1, 5, 16}" was not found')
            return []

        return popular_categories


    def get_editor_picks(self) -> List[Podcast]:
        try:
            editor_picks = self._session_cm.session.query(Podcast).filter(
                Podcast._id.in_([107, 504, 830])
            ).all()
        except NoResultFound:
            print(f'Podcasts with ids"{107, 504, 830}" was not found')
            return []

        return editor_picks


    def get_podcast_search_list(self) -> List[Podcast]:
        try:
            podcast_search_list = self._session_cm.session.query(Podcast).filter(
                Podcast._id.in_([289, 163, 800, 318])
            ).all()
        except NoResultFound:
            print(f'Podcasts with ids"{289, 163, 800, 318}" was not found')
            return []

        return podcast_search_list

    def get_podcasts_in_category(self, category_name: str) -> List[Podcast]:
        formatted_category_name = category_name.strip()

        try:
            # Try to query the category by exact name
            category = self._session_cm.session.query(Category).filter(
                Category._name == formatted_category_name).first()

            if category:
                # If the category exists, retrieve the podcasts associated with it
                return self._session_cm.session.query(Podcast).join(
                    podcast_categories_table, Podcast._id == podcast_categories_table.c.podcast_id
                ).join(
                    Category, podcast_categories_table.c.category_id == Category._id
                ).filter(
                    Category._id == category.id
                ).all()

            # If no exact match, perform a case-insensitive partial search
            categories = self._session_cm.session.query(Category).filter(
                Category._name.ilike(f"%{formatted_category_name}%")
            ).all()

            podcasts = []
            for c in categories:
                category_podcasts = self._session_cm.session.query(Podcast).join(
                    podcast_categories_table, Podcast._id == podcast_categories_table.c.podcast_id
                ).join(
                    Category, podcast_categories_table.c.category_id == Category._id
                ).filter(
                    Category._id == c.id
                ).all()
                podcasts.extend(category_podcasts)

            return podcasts

        except Exception as e:
            print(f"An error occurred while retrieving podcasts: {e}")
            return []

    def get_podcasts_by_author(self, author_name: str) -> List[Podcast]:
        formatted_author_name = author_name.strip()
        try:
            searched_podcasts = self._session_cm.session.query(Podcast).join(Author).filter(
                func.lower(Author._name).like(f"%{formatted_author_name}%")
            ).all()
            print(searched_podcasts)
        except NoResultFound:
            print(f'Author "{formatted_author_name}" was not found')
            return []

        return searched_podcasts


    def get_all_podcasts(self) -> List[Podcast]:
        podcasts = self._session_cm.session.query(Podcast).all()
        return podcasts

    def get_all_categories(self) -> List[Category]:
        categories = self._session_cm.session.query(Category).all()
        return categories

    def get_all_authors(self) -> List[Author]:
        authors = self._session_cm.session.query(Author).all()
        return authors

    def get_top_podcasts(self) -> List[Podcast]:
        try:
            top_podcasts = self._session_cm.session.query(Podcast).filter(
                Podcast._id.in_([772, 532, 89, 439])
            ).all()
        except NoResultFound:
            print(f'Podcasts with ids "{772, 532, 89, 439}" were not found')
            return []

        return top_podcasts

    def get_recently_played(self) -> List[Podcast]:
        try:
            recently_played_podcasts = self._session_cm.session.query(Podcast).filter(
                Podcast._id.in_([671, 220, 729, 9])
            ).all()
        except NoResultFound:
            print(f'Podcasts with ids "{671, 220, 729, 9}" were not found')
            return []

        return recently_played_podcasts


    def get_new_podcasts(self) -> List[Podcast]:
        try:
            new_podcasts = self._session_cm.session.query(Podcast).filter(
                Podcast._id.in_([740, 269, 640, 201])
            ).all()
        except NoResultFound:
            print(f'Podcasts with ids "{740, 269, 640, 201}" were not found')
            return []

        return new_podcasts

    def get_continue_listening_podcasts(self) -> List[Podcast]:
        try:
            continue_listening_podcasts = self._session_cm.session.query(Podcast).filter(
                Podcast._id.in_([547, 824, 909, 676])
            ).all()
        except NoResultFound:
            print(f'Podcasts with ids "{547, 824, 909, 676}" were not found')
            return []

        return continue_listening_podcasts
    #
    #
    # # Need to do this
    #

    def get_total_audio_time(self, audio_times: List[AudioTime]):
        total_time = AudioTime(0, 0, 0)
        for time in audio_times:
            total_time = total_time.add_time(time)
        return total_time

    def get_top_authors(self) -> List[Author]:
        try:
            authors = self.get_all_authors()
            top_authors = self._session_cm.session.query(Author).filter(
                Author._id.in_([authors[22].id, authors[45].id, authors[52].id])
            ).all()
        except NoResultFound:
            print('Top authors were not found')
            return []
        except IndexError:
            print('Index out of range for authors')
            return []

        return top_authors


    def get_top_podcasts_list(self) -> List[Podcast]:
        try:
            podcasts = self.get_all_podcasts()
            top_podcasts = self._session_cm.session.query(Podcast).filter(
                Podcast._id.in_([podcasts[i].id for i in range(162, 174)])
            ).all()
        except NoResultFound:
            print('Top podcasts were not found')
            return []
        except IndexError:
            print('Index out of range for podcasts')
            return []

        return top_podcasts


    def get_recently_played_list(self) -> List[Podcast]:
        try:
            podcasts = self.get_all_podcasts()
            recently_played_podcasts = self._session_cm.session.query(Podcast).filter(
                Podcast._id.in_([podcasts[i].id for i in range(44, 56)])
            ).all()
        except NoResultFound:
            print('Recently played podcasts were not found')
            return []
        except IndexError:
            print('Index out of range for podcasts')
            return []

        return recently_played_podcasts


    def get_new_podcasts_list(self) -> List[Podcast]:
        try:
            podcasts = self.get_all_podcasts()  # Retrieve all podcasts
            new_podcasts = self._session_cm.session.query(Podcast).filter(
                Podcast._id.in_([podcasts[i]._id for i in range(280, 292)])
            ).all()
        except NoResultFound:
            print('New podcasts were not found')
            return []
        except IndexError:
            print('Index out of range for podcasts')
            return []

        return new_podcasts


    def get_podcasts_by_title(self, title: str) -> List[Podcast]:
        if not isinstance(title, str):
            print(f"Invalid title type: {type(title)}")
            return []

        try:
            title = title.lower()
            searched_podcasts = self._session_cm.session.query(Podcast).filter(
                func.lower(Podcast._title).like(f"%{title}%")
            ).all()
        except NoResultFound:
            print(f'Title "{title}" was not found')
            return []

        return searched_podcasts


    def add_user(self, user: User):
        with self._session_cm as scm:
            scm.session.add(user)
            scm.commit()

    # ****** NOT SURE ************
    def add_playlist(self, playlist: Playlist):
        with self._session_cm as scm:
            scm.session.add(playlist)
            scm.commit()


    def get_user(self, username: str) -> Any | None:
        try:
            user = self._session_cm.session.query(User).filter(
                User._username == username.lower()
            ).one()
        except NoResultFound:
            return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

        return user


    def get_reviews_of_podcast(self, pc_id: int) -> List[Review]:
        try:
            podcast = self._session_cm.session.query(Podcast).filter(
                Podcast._id == pc_id
            ).one()
            reviews = podcast.reviews
        except NoResultFound:
            print(f'Podcast with id "{pc_id}" was not found')
            return []
        except Exception as e:
            print(f"An error occurred: {e}")
            return []

        return reviews

    # *********** NOT SURE *************
    def add_review(self, review, podcast_id: int):
        try:
            podcast = self._session_cm.session.query(Podcast).filter(
                Podcast._id == podcast_id
            ).one()
            podcast.add_review(review)

            # Step 2: Add the Comment first if it exists in the Review
            if review.comment:
                self._session_cm.session.add(review.comment)  # Add comment to the session first
                self._session_cm.session.flush()  # Ensure the comment is written to the database and assigned an ID

                # Step 3: Set the review's comment_id to the persisted comment's ID
                review.comment_id = review.comment.id  # Make sure the foreign key is set

            self._session_cm.session.add(review)
            self._session_cm.session.commit()

        except NoResultFound:
            print(f'Podcast with id "{podcast_id}" was not found')
        except Exception as e:
            print(f"An error occurred: {e}")
            self._session_cm.session.rollback()


# _ .
# . _
# . .
# _ _

    def get_user_playlist(self, user: User):
        try:
            playlist = self._session_cm.session.query(Playlist).filter(Playlist.user_id == user.id).one()
            return playlist

        except Exception as e:
            print(f"An error occurred while retrieving the user's playlist: {e}")
            return None

    def add_podcast_to_playlist(self, playlist: Playlist, podcast: Podcast, user: User):
        stmt = podcast_users_table.insert().values(
            podcast_id=podcast._id,
            user_id=user._id
        )

        # Execute the statement and commit the changes to the database
        self._session_cm.session.execute(stmt)
        self._session_cm.session.commit()

    def add_episode_to_playlist(self, playlist: Playlist, episode: Episode, user: User):
        stmt = episode_users_table.insert().values(
            episode_id=episode._episode_id,
            user_id=user._id
        )

        self._session_cm.session.execute(stmt)
        self._session_cm.session.commit()

    def remove_podcast_from_playlist(self, playlist: Playlist, podcast: Podcast, user: User):
        stmt = delete(podcast_users_table).where(
            podcast_users_table.c.podcast_id == podcast._id,
            podcast_users_table.c.user_id == user._id
        )

        self._session_cm.session.execute(stmt)
        self._session_cm.session.commit()

    def remove_episode_from_playlist(self, playlist: Playlist, episode: Episode, user: User):
        stmt = delete(episode_users_table).where(
            episode_users_table.c.episode_id == episode._episode_id,
            episode_users_table.c.user_id == user._id
        )

        self._session_cm.session.execute(stmt)
        self._session_cm.session.commit()


    def get_podcast_average_rating(self, podcast_id):
        average_rating = None
        total_rating = 0

        try:
            podcast = self._session_cm.session.query(Podcast).filter(Podcast._id == podcast_id).one_or_none()

            if podcast is None:
                raise ValueError(f"Podcast with ID {podcast_id} not found.")

            if podcast.reviews:
                total_rating = sum(review.rating for review in podcast.reviews)
                average_rating = round(total_rating / len(podcast.reviews), 1)

        except Exception as e:
            print(f"An error occurred: {e}")

        return average_rating


    def add_podcast(self, podcast: Podcast):
        with self._session_cm as scm:
            scm.session.merge(podcast)
            scm.commit()


    def add_episode(self, episode: Episode):
        with self._session_cm as scm:
            scm.session.merge(episode)
            scm.commit()
