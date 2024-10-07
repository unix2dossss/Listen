from sqlalchemy import (
    Table, Column, Integer, Float, String, DateTime, ForeignKey, Text
)
from sqlalchemy.orm import registry, relationship
from datetime import datetime

from podcast.domainmodel.model import Podcast, Author, Category, User, Review, Episode, Comment, AudioTime, Playlist

# Global variable giving access to the MetaData (schema) information of the database
mapper_registry = registry()

authors_table = Table(
    'authors', mapper_registry.metadata,
    Column('author_id', Integer, primary_key=True),
    Column('name', String(255), nullable=False, unique=True),
)

podcast_table = Table(
    'podcasts', mapper_registry.metadata,
    Column('podcast_id', Integer, primary_key=True),
    Column('title', Text, nullable=True),
    Column('image_url', Text, nullable=True),
    Column('description', String(255), nullable=True),
    Column('language', String(255), nullable=True),
    Column('website_url', String(255), nullable=True),
    Column('author_id', ForeignKey('authors.author_id')),
    Column('itunes_id', Integer, nullable=True),
)

# Episodes should have links to its podcast through its foreign keys
episode_table = Table(
    'episodes', mapper_registry.metadata,
    Column('episode_id', Integer, primary_key=True),
    Column('podcast_id', Integer, ForeignKey('podcasts.podcast_id')),
    Column('title', Text, nullable=True),
    Column('audio_url', Text, nullable=True),
    Column('audio_length', Integer, nullable=True),
    Column('description', String(255), nullable=True),
    Column('pub_date', Text, nullable=True),

)

categories_table = Table(
    'categories', mapper_registry.metadata,
    Column('category_id', Integer, primary_key=True, autoincrement=True),
    Column('category_name', String(64)) #, nullable=False)
)

podcast_categories_table = Table(
    'podcast_categories', mapper_registry.metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('podcast_id', ForeignKey('podcasts.podcast_id')),
    Column('category_id', ForeignKey('categories.category_id')),
)

users_table = Table(
    'users', mapper_registry.metadata,
    Column('user_id', Integer, primary_key=True, autoincrement=True),
    Column('username', String(255), unique=True, nullable=False),
    Column('password', String(255), nullable=False),
)

# Reviews should have links to its podcast and user through its foreign keys
reviews_table = Table(
    'reviews', mapper_registry.metadata,
    Column('review_id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', ForeignKey('users.user_id')),
    Column('podcast_id', ForeignKey('podcasts.podcast_id')),
    # Column('comment', ForeignKey('comments.comment_id')),
    # Column('comment', Integer),  # Keep this as an integer to store the comment ID
    # Column('comment', ForeignKey('comments.comment_id')),  # This sets the foreign key correctly
    Column('comment_id', ForeignKey('comments.comment_id')),
    Column('rating', Integer, nullable=False),
    # Column('timestamp', DateTime, nullable=False),
)

# Comments should have links to its user through its foreign keys
comments_table = Table(
    'comments', mapper_registry.metadata,
    Column('comment_id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', ForeignKey('users.user_id')),
    Column('comment_text', String(255), nullable=False),
    Column('comment_date', DateTime, nullable=False),
    # Column('review_id', ForeignKey('reviews.review_id')),
)


audio_times_table = Table(
    'audio_times', mapper_registry.metadata,
    Column('audio_time_id', Integer, primary_key=True, autoincrement=True),
    Column('audio_hours', Integer, nullable=True),
    Column('audio_minutes', Integer, nullable=True),
    Column('audio_seconds', Integer, nullable=True),
    # Column('episode_id', Integer, ForeignKey('episodes.episode_id')),
    Column('episode_id', Integer, ForeignKey('episodes.episode_id', ondelete='CASCADE'), unique=True),
)

playlists_table = Table(
    'playlists', mapper_registry.metadata,
    Column('playlist_id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', ForeignKey('users.user_id')),
    Column('name', ForeignKey('podcasts.podcast_id')),
)

# playlist_episodes_table = Table(
#     'playlist_episodes', mapper_registry.metadata,
#     Column('id', Integer, primary_key=True, autoincrement=True),
#     Column('episode_id', ForeignKey('episodes.episode_id')),
#     Column('playlist_id', ForeignKey('playlists.playlist_id')),
# )
#
# playlist_podcasts_table = Table(
#     'playlist_podcasts', mapper_registry.metadata,
#     Column('id', Integer, primary_key=True, autoincrement=True),
#     Column('podcast_id', ForeignKey('podcasts.podcast_id')),
#     Column('playlist_id', ForeignKey('playlists.playlist_id')),
# )


podcast_users_table = Table(
    'podcast_users', mapper_registry.metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('podcast_id', Integer, ForeignKey('podcasts.podcast_id')),
    Column('user_id', Integer, ForeignKey('users.user_id')),
)

episode_users_table = Table(
    'episode_users', mapper_registry.metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('episode_id', Integer, ForeignKey('episodes.episode_id')),
    Column('user_id', Integer, ForeignKey('users.user_id')),
)


def map_model_to_tables():
    mapper_registry.map_imperatively(Author, authors_table, properties={
        '_id': authors_table.c.author_id,
        '_name': authors_table.c.name,
        'podcast_list': relationship(Podcast, back_populates='_author')
    })

    mapper_registry.map_imperatively(Category, categories_table, properties={
        '_id': categories_table.c.category_id,
        '_name': categories_table.c.category_name,
    })

    mapper_registry.map_imperatively(Podcast, podcast_table, properties={
        '_id': podcast_table.c.podcast_id,
        '_title': podcast_table.c.title,
        '_image': podcast_table.c.image_url,
        '_description': podcast_table.c.description,
        '_language': podcast_table.c.language,
        '_website': podcast_table.c.website_url,
        '_itunes_id': podcast_table.c.itunes_id,
        '_author': relationship(Author, back_populates='podcast_list'),
        'episodes': relationship(Episode, back_populates='_episode_podcast'),
        '_reviews': relationship(Review),
        'categories': relationship(Category, secondary=podcast_categories_table),
        '_in_playlist_users': relationship(User, secondary=podcast_users_table),
    })

    mapper_registry.map_imperatively(Episode, episode_table, properties={
        '_episode_id': episode_table.c.episode_id,
        '_episode_podcast': relationship(Podcast, back_populates='episodes'),
        '_episode_title': episode_table.c.title,
        '_episode_audio_link': episode_table.c.audio_url,
        '_episode_audio_length': relationship(AudioTime, uselist=False),
        '_episode_description': episode_table.c.description,
        '_episode_publish_date': episode_table.c.pub_date,
        '_episode_in_playlist_users': relationship(User, secondary=episode_users_table),
    })

    mapper_registry.map_imperatively(User, users_table, properties={
        '_id': users_table.c.user_id,
        '_username': users_table.c.username,
        '_password': users_table.c.password,
        '_reviews': relationship(Review)
    })

    mapper_registry.map_imperatively(Review, reviews_table, properties={
        # '_Review__timestamp': reviews_table.c.timestamp,
        '_id': reviews_table.c.review_id,
        '_owner': relationship(User, back_populates='_reviews'),
        '_rating': reviews_table.c.rating,
        # '_comment': relationship(Comment),
        # '_comment': relationship(Comment, foreign_keys=[reviews_table.c.comment]),
        # '_comment': relationship(Comment, backref='review', viewonly=True),  # Backref allows reverse access from Comment to Review
        '_comment': relationship(Comment, foreign_keys=[reviews_table.c.comment_id], backref='review', viewonly=True),

    })

    mapper_registry.map_imperatively(Comment, comments_table, properties={
        # '_Review__timestamp': reviews_table.c.timestamp,
        '_id': comments_table.c.comment_id,
        '_comment_text': comments_table.c.comment_text,
        '_comment_date': comments_table.c.comment_date,
        '_owner': relationship(User),
    })

    mapper_registry.map_imperatively(AudioTime, audio_times_table, properties={
        'audio_hours': audio_times_table.c.audio_hours,
        'audio_minutes': audio_times_table.c.audio_minutes,
        'audio_seconds': audio_times_table.c.audio_seconds,
    })

    # mapper_registry.map_imperatively(Playlist, playlists_table, properties={
    #     '_id': playlists_table.c.playlist_id,
    #     '_name': playlists_table.c.name,
    #     '_user': relationship(User),
    #     '_episodes': relationship(Episode, secondary=podcast_users_table),
    #     '_podcasts': relationship(Podcast, secondary=episode_users_table),
    # })

    mapper_registry.map_imperatively(Playlist, playlists_table, properties={
        '_id': playlists_table.c.playlist_id,
        '_name': playlists_table.c.name,
        '_user': relationship(User),
        '_episodes': relationship(
            Episode,
            secondary=episode_users_table,
            primaryjoin=playlists_table.c.playlist_id == episode_users_table.c.user_id,  # Adjust this join condition
            secondaryjoin=episode_users_table.c.episode_id == episode_table.c.episode_id
        ),
        '_podcasts': relationship(
            Podcast,
            secondary=podcast_users_table,
            primaryjoin=playlists_table.c.playlist_id == podcast_users_table.c.user_id,  # Adjust this join condition
            secondaryjoin=podcast_users_table.c.podcast_id == podcast_table.c.podcast_id
        ),
    })

