import pytest

import datetime

from sqlalchemy.exc import IntegrityError

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


def insert_user(empty_session, values=None):
    new_name = "Meow"
    new_password = "Testing235"

    if values is not None:
        new_name = values[0]
        new_password = values[1]

    empty_session.execute('INSERT INTO users (user_name, password) VALUES (:user_name, :password)',
                          {'user_name': new_name, 'password': new_password})
    row = empty_session.execute('SELECT id from users where user_name = :user_name',
                                {'user_name': new_name}).fetchone()
    return row[0]


def insert_users(empty_session, values):
    for value in values:
        empty_session.execute('INSERT INTO users (user_name, password) VALUES (:user_name, :password)',
                              {'user_name': value[0], 'password': value[1]})
    rows = list(empty_session.execute('SELECT id from users'))
    keys = tuple(row[0] for row in rows)
    return keys


def insert_author(empty_session, values=None):
    new_id = 1
    new_name = "Meow"

    if values is not None:
        new_id = values[0]
        new_name = values[1]

    empty_session.execute('INSERT INTO authors (author_id, name) VALUES (:author_id, :name)',
                          {'author_id': new_id, 'name': new_name})
    row = empty_session.execute('SELECT id from authors where name = :name',
                                {'name': new_name}).fetchone()
    return row[0]


def insert_authors(empty_session, values):
    for value in values:
        empty_session.execute('INSERT INTO authors (author_id, name) VALUES (:author_id, :name)',
                              {'author_id': value[0], 'name': value[1]})
    rows = list(empty_session.execute('SELECT id from authors'))
    keys = tuple(row[0] for row in rows)
    return keys


def insert_podcast(empty_session):
    empty_session.execute(
        'INSERT INTO podcasts (podcast_id, title, image_url, description, language, website_url) VALUES '
        '(100, "Joe Toste Podcast - Sales Training Expert", '
        '"https://www.stuff.co.nz/national/health/119899280/ministry-of-health-gives-latest-update-on-novel-coronavirus", '
        '"The first case of coronavirus has been confirmed in New Zealand  and authorities are now scrambling to track down people who may have come into contact with the patient.", '
        '"https://www.stuff.co.nz/national/health/119899280/ministry-of-health-gives-latest-update-on-novel-coronavirus", '
        '"https://resources.stuff.co.nz/content/dam/images/1/z/e/3/w/n/image.related.StuffLandscapeSixteenByNine.1240x700.1zduvk.png/1583369866749.jpg")'
    )
    row = empty_session.execute('SELECT id from podcasts').fetchone()
    return row[0]


def insert_categories(empty_session):
    empty_session.execute(
        'INSERT INTO categories (category_name) VALUES ("Society & Culture"), ("Professional")'
    )
    rows = list(empty_session.execute('SELECT id from categories'))
    keys = tuple(row[0] for row in rows)
    return keys


def insert_podcast_categories_associations(empty_session, podcast_key, category_keys):
    stmt = 'INSERT INTO podcast_categories (podcast_id, category_id) VALUES (:podcast_id, :category_id)'
    for category_key in category_keys:
        empty_session.execute(stmt, {'podcast_id': podcast_key, 'category_id': category_key})


def make_user():
    return User(1, "Shyamli", "pw12345")

def make_author():
    return Author(1, "Joe Toste")

def make_podcast():
    my_author = make_author()
    return Podcast(100, my_author, "Joe Toste Podcast - Sales Training Expert")



