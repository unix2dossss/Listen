import pytest

import datetime

from sqlalchemy.exc import IntegrityError

from podcast.domainmodel.model import (
    Author,
    Podcast,
    Category,
    User,
    Episode,
    Comment,
    Review,
    Playlist, AudioTime,
)


# ORM Tests Config

def insert_user(empty_session, values=None):
    new_name = "Meow"
    new_password = "Testing235"

    if values is not None:
        new_name = values[0]
        new_password = values[1]

    empty_session.execute('INSERT INTO users (username, password) VALUES (:username, :password)',
                          {'username': new_name, 'password': new_password})
    row = empty_session.execute('SELECT user_id from users where username = :username',
                                {'username': new_name}).fetchone()
    return row[0]


def insert_users(empty_session, values):
    for value in values:
        empty_session.execute('INSERT INTO users (username, password) VALUES (:username, :password)',
                              {'username': value[0], 'password': value[1]})
    rows = list(empty_session.execute('SELECT user_id from users'))
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
    row = empty_session.execute('SELECT author_id from authors where name = :name',
                                {'name': new_name}).fetchone()
    return row[0]


def insert_authors(empty_session, values):
    for value in values:
        empty_session.execute('INSERT INTO authors (author_id, name) VALUES (:author_id, :name)',
                              {'author_id': value[0], 'name': value[1]})
    rows = list(empty_session.execute('SELECT author_id from authors'))
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
    row = empty_session.execute('SELECT podcast_id from podcasts').fetchone()
    return row[0]


def insert_categories(empty_session):
    empty_session.execute(
        'INSERT INTO categories (category_name) VALUES ("Society & Culture"), ("Professional")'
    )
    rows = list(empty_session.execute('SELECT category_id from categories'))
    keys = tuple(row[0] for row in rows)
    return keys


def insert_podcast_categories_associations(empty_session, podcast_key, category_keys):
    stmt = 'INSERT INTO podcast_categories (podcast_id, category_id) VALUES (:podcast_id, :category_id)'
    for category_key in category_keys:
        empty_session.execute(stmt, {'podcast_id': podcast_key, 'category_id': category_key})


def insert_episode(empty_session):
    empty_session.execute(
        'INSERT INTO episodes (episode_id, title, audio_url, audio_length, description, pub_date) VALUES '
        '(1, "Joe Toste Podcast - Sales Training Expert", '
        '"https://www.stuff.co.nz/national/health/119899280/ministry-of-health-gives-latest-update-on-novel-coronavirus", '
        '"The first case of coronavirus has been confirmed in New Zealand  and authorities are now scrambling to track down people who may have come into contact with the patient.", '
        '"https://www.stuff.co.nz/national/health/119899280/ministry-of-health-gives-latest-update-on-novel-coronavirus", '
        '"2020-03-04 12:00:00")'
    )
    row = empty_session.execute('SELECT episode_id from episodes').fetchone()
    return row[0]


def insert_playlist(empty_session):
    empty_session.execute(
        'INSERT INTO playlists (playlist_id, user_id, name) VALUES '
        '(3, 1, "Testing")'
    )
    row = empty_session.execute('SELECT playlist_id from playlists').fetchone()
    return row[0]


def make_user():
    return User(1, "Shyamli", "Testing235")


def make_author():
    return Author(1, "Joe Toste")


def make_podcast():
    my_author = make_author()
    return Podcast(100, my_author, "Joe Toste Podcast - Sales Training Expert")


def make_episode():
    my_podcast = make_podcast()
    my_audio_time = AudioTime(5, 36, 0)
    my_date_time = datetime.datetime.strptime("2017-12-11 15:00:00+0000", "%Y-%m-%d %H:%M:%S%z")
    return Episode(
        1,
        my_podcast,
        "1: Festive food and farming",
        "https://audioboom.com/posts/6546476.mp3?source=rss&stitched=1",
        my_audio_time,
        """
                       <p>John Bates hosts this festive special from the AHDB consumer insights team looking at how the 
                       season of goodwill changes what and how we buy, how Brexit might impact our favourite festive 
                       foods and what farmers and growers need to think about to gear up for Christmas future.</p><p>
                       <a href="https://ahdb.org.uk/">https://ahdb.org.uk/</a></p><p>Photo by Keenan Loo on Unsplash</p>
                       """,
        my_date_time,
    )


def make_playlist():
    my_user = make_user()
    return Playlist(1, my_user, 'My Playlist')


# ORM Tests

# User Tests

# def test_loading_of_users(empty_session):
#     users = list()
#     users.append((1, "Shaymli", "Testing235"))
#     users.append((2, "Asma", "Testing111"))
#     insert_users(empty_session, users)
#
#     expected = [
#         User(1, "Shaymli", "Testing235"),
#         User(2, "Asma", "Testing111")
#     ]
#
#     assert empty_session.query(User).all()[0].id == 1
#     assert empty_session.query(User).all()[1].id == 2
#
#
# def test_saving_of_users(empty_session):
#     user = make_user()
#     empty_session.add(user)
#     empty_session.commit()
#
#     rows = list(empty_session.execute('SELECT username, password FROM users'))
#     assert rows == [("shyamli", "Testing235")]
#
#
# def test_saving_of_users_with_common_user_name(empty_session):
#     insert_user(empty_session, ("shyamli", "Testing1234"))
#     empty_session.commit()
#
#     with pytest.raises(IntegrityError):
#         user = User(1, "shyamli", "Testing111")
#         empty_session.add(user)
#         empty_session.commit()
#
#
# # Author Tests
#
# def test_loading_of_authors(empty_session):
#     authors = list()
#     authors.append((1, "Shaymli"))
#     authors.append((2, "Asma"))
#     insert_authors(empty_session, authors)
#
#     expected = [
#         Author(1, "Shaymli"),
#         Author(2, "Asma")
#     ]
#
#     assert empty_session.query(Author).all() == expected
#
#
# def test_saving_of_authors(empty_session):
#     author = make_author()
#     empty_session.add(author)
#     empty_session.commit()
#
#     rows = list(empty_session.execute('SELECT author_id, name FROM authors'))
#
#     assert rows == [(1, 'Joe Toste')]
#
#
# def test_saving_of_authors_with_common_name(empty_session):
#     insert_author(empty_session, (1, 'Joe Toste'))
#     empty_session.commit()
#
#     with pytest.raises(IntegrityError):
#         author = Author(1, 'Joe Toste')
#         empty_session.add(author)
#         empty_session.commit()
#
#
# # Podcast Tests
#
# def test_loading_of_podcasts(empty_session):
#     podcast_key = insert_podcast(empty_session)
#     expected_podcast = make_podcast()
#     fetched_podcast = empty_session.query(Podcast).one()
#
#     assert expected_podcast == fetched_podcast
#     assert podcast_key == fetched_podcast.id
#
#
# def test_saving_of_podcast(empty_session):
#     podcast = make_podcast()
#     empty_session.add(podcast)
#     empty_session.commit()
#
#     rows = list(
#         empty_session.execute('SELECT podcast_id, title, image_url, description, language, website_url FROM podcasts'))
#
#     assert rows == [(100, 'Joe Toste Podcast - Sales Training Expert', None, '', 'Unspecified', '')]


# Episode Tests

def test_loading_of_episodes(empty_session):
    episode_key = insert_episode(empty_session)
    expected_episode = make_episode()
    fetched_episode = empty_session.query(Episode).one()


    assert expected_episode == fetched_episode
    assert episode_key == fetched_episode.episode_id

# def test_saving_of_podcast(empty_session):
#     podcast = make_podcast()
#     empty_session.add(podcast)
#     empty_session.commit()
#
#     rows = list(
#         empty_session.execute('SELECT podcast_id, title, image_url, description, language, website_url FROM podcasts'))
#
#     assert rows == [(100, 'Joe Toste Podcast - Sales Training Expert', None, '', 'Unspecified', '')]


# Playlist Tests

# def test_loading_of_playlist(empty_session):
#     playlist_key = insert_playlist(empty_session)
#     expected_playlist = make_playlist()
#     fetched_playlist = empty_session.query(Playlist).one()
#
#     assert expected_playlist.id == fetched_playlist.id
#
#
# def test_saving_of_playlist(empty_session):
#     playlist = make_playlist()
#     empty_session.add(playlist)
#     empty_session.commit()
#
#     rows = list(
#         empty_session.execute('SELECT playlist_id, user_id, name FROM playlists'))
#
#
#     assert rows[0].name == 'My Playlist'
