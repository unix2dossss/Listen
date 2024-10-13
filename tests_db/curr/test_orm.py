import pytest
import datetime
from sqlalchemy import text
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


def insert_category(empty_session):
    empty_session.execute(text('INSERT INTO categories (category_id, name) VALUES (1, "Comedy")'))
    row = empty_session.execute(text('SELECT category_id from categories')).fetchone()
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


def insert_episodes(empty_session):
    podcast_key = insert_podcast(empty_session)
    empty_session.execute(text(
        'INSERT INTO episodes (episode_id, podcast_id, audio, audio_length, date, title, episode_description) VALUES'
        '(1, :podcast_id, "some audio", 20, "some date", "some title", "this is cool"),'
        '(2, :podcast_id, "audio some", 30, "date some", "title some", "cool this is")'), {'podcast_id': podcast_key})
    rows = list(empty_session.execute(text('SELECT episode_id FROM episodes')))
    keys = tuple(row[0] for row in rows)
    return keys


def insert_playlist(empty_session):
    empty_session.execute(
        'INSERT INTO playlists (playlist_id, user_id, name) VALUES '
        '(1, 1, "Testing")'
    )
    row = empty_session.execute('SELECT playlist_id from playlists').fetchone()
    return row[0]


def insert_reviewed_podcast(empty_session):
    podcast_key = insert_podcast(empty_session)
    user_key = insert_user(empty_session)

    empty_session.execute(text(
        'INSERT INTO reviews (review_id, username, rating, comment, podcast_id) VALUES (:review_id, :username, :rating, :comment, :podcast_id)'),
        {'review_id': 33, 'username': user_key, 'rating': 5, 'comment': 'so good',
         'podcast_id': podcast_key})

    row = empty_session.execute(text('SELECT review_id from reviews')).fetchone()
    return row[0]


def insert_test_podcast_categories_associations(empty_session, podcast_key, category_keys):
    stmt = 'INSERT INTO podcast_categories (podcast_id, category_id) VALUES (:podcast_id, :category_id)'
    for category_key in category_keys:
        empty_session.execute(text(stmt), {'podcast_id': podcast_key, 'category_id': category_key})


def insert_test_playlist_episodes_associations(empty_session, playlist_key, episode_keys):
    stmt = 'INSERT INTO playlists_episodes (playlist_id, episode_id) VALUES (:playlist_id, :episode_id)'
    for episode_key in episode_keys:
        empty_session.execute(text(stmt), {'playlist_id': playlist_key, 'episode_id': episode_key})


def make_user():
    return User(1, "Shyamli", "Testing235")


def make_author():
    return Author(1, "Joe Toste")


def make_podcast():
    my_author = make_author()
    return Podcast(100, my_author, "Joe Toste Podcast - Sales Training Expert")


def make_category():
    category = Category(1, "Comedy")
    return category


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

def make_comment():
    my_user = make_user()
    my_date_time = datetime.datetime.strptime("2017-12-11 15:00:00+0000", "%Y-%m-%d %H:%M:%S%z")
    return Comment(my_user, "Good!", my_date_time)

def make_review():
    my_user = make_user()
    my_comment = make_comment()
    Review(my_user, my_comment)


# ORM Tests

# User Tests
def test_loading_of_users(empty_session):
    users = list()
    users.append((1, "Shaymli", "Testing235"))
    users.append((2, "Asma", "Testing111"))
    insert_users(empty_session, users)

    expected = [
        User(1, "Shaymli", "Testing235"),
        User(2, "Asma", "Testing111")
    ]

    assert empty_session.query(User).all()[0].id == 1
    assert empty_session.query(User).all()[1].id == 2


def test_saving_of_users(empty_session):
    user = make_user()
    empty_session.add(user)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT username, password FROM users'))
    assert rows == [("shyamli", "Testing235")]


def test_saving_of_users_with_common_user_name(empty_session):
    insert_user(empty_session, ("shyamli", "Testing1234"))
    empty_session.commit()

    with pytest.raises(IntegrityError):
        user = User(1, "shyamli", "Testing111")
        empty_session.add(user)
        empty_session.commit()


# Author Tests

def test_loading_of_authors(empty_session):
    authors = list()
    authors.append((1, "Shaymli"))
    authors.append((2, "Asma"))
    insert_authors(empty_session, authors)

    expected = [
        Author(1, "Shaymli"),
        Author(2, "Asma")
    ]

    assert empty_session.query(Author).all() == expected


def test_saving_of_authors(empty_session):
    author = make_author()
    empty_session.add(author)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT author_id, name FROM authors'))

    assert rows == [(1, 'Joe Toste')]


def test_saving_of_authors_with_common_name(empty_session):
    insert_author(empty_session, (1, 'Joe Toste'))
    empty_session.commit()

    with pytest.raises(IntegrityError):
        author = Author(1, 'Joe Toste')
        empty_session.add(author)
        empty_session.commit()


# Podcast Tests
def test_loading_of_podcasts(empty_session):
    podcast_key = insert_podcast(empty_session)
    expected_podcast = make_podcast()
    fetched_podcast = empty_session.query(Podcast).one()

    assert expected_podcast == fetched_podcast
    assert podcast_key == fetched_podcast.id


def test_saving_of_podcast(empty_session):
    podcast = make_podcast()
    empty_session.add(podcast)
    empty_session.commit()

    rows = list(
        empty_session.execute('SELECT podcast_id, title, image_url, description, language, website_url FROM podcasts'))

    assert rows == [(100, 'Joe Toste Podcast - Sales Training Expert', None, '', 'Unspecified', '')]


# Category Tests

def test_loading_of_categories(empty_session):
    insert_category(empty_session)

    expected = [Category(1, "Comedy")]
    assert empty_session.query(Category).all() == expected


def test_saving_of_categories(empty_session):
    category = make_category()
    empty_session.add(category)
    empty_session.commit()

    rows = list(empty_session.execute(text('SELECT category_id, category_name FROM categories')).all())
    assert rows == [(1, "Comedy")]


# Episode Tests
def test_loading_of_episodes(empty_session):
    episode_key = insert_episode(empty_session)
    expected_episode = make_episode()
    fetched_episode = empty_session.query(Episode).one()

    assert expected_episode == fetched_episode
    assert episode_key == fetched_episode.episode_id


def test_saving_of_episode(empty_session):
    episode = make_episode()
    empty_session.add(episode)
    empty_session.commit()

    rows = list(empty_session.execute(text(
        'SELECT episode_id, podcast_id, title, audio_url, description, pub_date FROM episodes')).all())

    print(rows)
    print(":))")

    assert rows == [(23, 10, "some audio", 22, "some date", "some title", "yeeeeah")]


# Playlist Tests
def test_loading_of_playlist(empty_session):
    playlist_key = insert_playlist(empty_session)
    expected_playlist = make_playlist()
    fetched_playlist = empty_session.query(Playlist).one()

    assert expected_playlist.id == fetched_playlist.id


def test_saving_of_playlist(empty_session):
    playlist = make_playlist()
    empty_session.add(playlist)
    empty_session.commit()

    rows = list(
        empty_session.execute('SELECT playlist_id, user_id, name FROM playlists'))

    assert rows[0].name == 'My Playlist'


# Relationship Tests

def test_loading_of_playlist_with_episodes(empty_session):
    playlist_key = insert_playlist(empty_session)
    episode_keys = insert_episodes(empty_session)

    insert_test_playlist_episodes_associations(empty_session, playlist_key, episode_keys)

    playlist = empty_session.get(Playlist, playlist_key)
    episodes = [empty_session.get(Episode, key) for key in episode_keys]

    for episode in episodes:
        assert episode in playlist.playlist_episodes


def test_saving_of_episodes_to_playlist(empty_session):
    playlist = make_playlist()
    episode = make_episode()
    user = make_user()

    empty_session.add(playlist)
    empty_session.add(episode)
    empty_session.commit()

    playlist.add_episode(episode, user)
    empty_session.commit()

    rows = list(empty_session.execute((text('SELECT playlist_id FROM playlists'))))
    playlist_key = rows[0][0]

    rows = list(empty_session.execute((text('SELECT episode_id FROM episodes'))))
    episode_key = rows[0][0]

    rows = list(empty_session.execute((text('SELECT playlist_id, episode_id FROM playlists_episodes'))))
    playlist_foreign_key = rows[0][0]
    episode_foreign_key = rows[0][1]

    assert playlist_key == playlist_foreign_key
    assert episode_key == episode_foreign_key


def test_loading_of_podcast_with_categories(empty_session):
    podcast_key = insert_podcast(empty_session)
    category_keys = insert_categories(empty_session)

    insert_test_podcast_categories_associations(empty_session, podcast_key, category_keys)

    podcast = empty_session.get(Podcast, podcast_key)
    categories = [empty_session.get(Category, key) for key in category_keys]

    for category in categories:
        assert category in podcast.categories


def test_saving_categories_to_podcasts(empty_session):
    podcast = make_podcast()
    category = make_category()

    empty_session.add(podcast)
    empty_session.commit()
    empty_session.add(category)
    empty_session.commit()

    podcast.add_category(category)
    empty_session.commit()

    rows = list(empty_session.execute(text('SELECT podcast_id FROM podcasts')))
    podcast_key = rows[0][0]

    rows = list(empty_session.execute(text('SELECT category_id, name FROM categories')))
    category_key = rows[0][0]
    assert rows[0][1] == "Sports"

    rows = list(empty_session.execute(text('SELECT podcast_id, category_id FROM podcast_categories')))
    podcast_foreign_key = rows[0][0]
    category_foreign_key = rows[0][1]

    assert podcast_key == podcast_foreign_key
    assert category_key == category_foreign_key


def test_loading_of_reviewed_podcast(empty_session):
    insert_reviewed_podcast(empty_session)

    rows = empty_session.query(Podcast).all()
    podcast = rows[0]

    for review in podcast.get_reviews:
        assert review.podcast is podcast


def test_saving_of_review(empty_session):
    podcast_key = insert_podcast(empty_session)
    user_key = insert_user(empty_session, (1000, "locky", "123"))

    rows = empty_session.query(Podcast).all()
    podcast = rows[0]
    user = empty_session.query(User).filter(User._username == "locky").one()

    review_text = "so good"
    review = make_review()

    empty_session.add(review)
    empty_session.commit()

    podcast.add_review(review)

    rows = list(empty_session.execute(text('SELECT review_id, username, rating, comment, podcast_id FROM reviews')))

    assert rows == [(1, user_key, 5, "so good", podcast_key)]


def test_saving_reviewed_podcast(empty_session):
    podcast = make_podcast()
    user = make_user()

    review_text = "so good"
    review = make_review()

    empty_session.add(podcast)
    empty_session.commit()
    empty_session.add(user)
    empty_session.commit()
    empty_session.add(review)
    empty_session.commit()

    podcast.add_review(review)
    user.add_review(review)

    rows = list(empty_session.execute(text("SELECT podcast_id FROM podcasts")))
    podcast_key = rows[0][0]

    rows = list(empty_session.execute(text("SELECT username FROM users")))
    user_key = rows[0][0]

    rows = list(empty_session.execute(text("SELECT review_id, username, rating, comment, podcast_id FROM reviews")))
    assert rows == [(1, user_key, 5, review_text, podcast_key)]

