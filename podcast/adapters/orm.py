from sqlalchemy import (
    Table, Column, Integer, Float, String, DateTime, ForeignKey, Text
)
from sqlalchemy.orm import registry, relationship
from datetime import datetime

from podcast.domainmodel.model import Podcast, Author, Category, User, Review, Episode

# Global variable giving access to the MetaData (schema) information of the database
mapper_registry = registry()

authors_table = Table(
    'authors', mapper_registry.metadata,
    Column('author_id', Integer, primary_key=True),
    Column('name', String(255), nullable=False, unique=True)
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
    Column('itunes_id', Integer, nullable=True)
)

# Episodes should have links to its podcast through its foreign keys
episode_table = Table(
    'episodes', mapper_registry.metadata,
    Column('episode_id', Integer, primary_key=True),
    Column('podcast_id', Integer, ForeignKey('podcasts.podcast_id')),
    Column('title', Text, nullable=True),
    Column('audio_url', Text, nullable=True),
    Column('description', String(255), nullable=True),
    Column('pub_date', Text, nullable=True)
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
    Column('timestamp', DateTime, nullable=False),
    Column('review_text', String(255), nullable=False),
    Column('rating', Integer, nullable=False),
    Column('podcast_id', ForeignKey('podcasts.podcast_id')),
    Column('user_id', ForeignKey('users.user_id')),
)

def map_model_to_tables():
    mapper_registry.map_imperatively(Author, authors_table, properties={
        '_id': authors_table.c.author_id,
        '_name': authors_table.c.name,
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
        '_author': relationship(Author),
        '_Podcast_episodes': relationship(Episode, back_populates='episode_podcast'),
        # '_reviews': relationship(Review, back_populates='_Review__podcast'),
        'categories': relationship(Category, secondary=podcast_categories_table),
    })

    mapper_registry.map_imperatively(Episode, episode_table, properties={
        'episode_id': episode_table.c.episode_id,
        'episode_podcast': relationship(Podcast, back_populates='_Podcast_episodes'),
        'episode_title': episode_table.c.title,
        'episode_audio_link': episode_table.c.audio_url,
        'episode_description': episode_table.c.description,
        'episode_publish_date': episode_table.c.pub_date,
    })

    mapper_registry.map_imperatively(User, users_table, properties={
        '_id': users_table.c.user_id,
        '_username': users_table.c.username,
        '_password': users_table.c.password,
        '_reviews': relationship(Review, back_populates='_owner')
    })

    mapper_registry.map_imperatively(Review, reviews_table, properties={
        # '_Review__timestamp': reviews_table.c.timestamp,
        '_comment': reviews_table.c.review_text,
        '_rating': reviews_table.c.rating,
        '_owner': relationship(User, back_populates='_reviews'),
        # '_Review__podcast': relationship(Podcast, back_populates='_Podcast_reviews')
    })