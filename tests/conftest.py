import pytest

from podcast import MemoryRepository, populate, create_app
from pathlib import Path
from datetime import datetime
import os
from podcast.adapters.datareader.csvdatareader import CSVDataReader

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

# Fixtures to reuse in multiple tests

@pytest.fixture
def in_memory_repo():
    repo = MemoryRepository()
    data_path = Path("podcast") / "adapters" / "data"
    populate(data_path, repo)
    return repo

@pytest.fixture
def my_author():
    return Author(1, "Joe Toste")


@pytest.fixture
def my_podcast(my_author):
    return Podcast(100, my_author, "Joe Toste Podcast - Sales Training Expert")


@pytest.fixture
def my_user():
    return User(1, "Shyamli", "pw12345")


@pytest.fixture
def my_episode(my_podcast, my_audio_time, my_date_time):
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


@pytest.fixture
def my_subscription(my_user, my_podcast):
    return PodcastSubscription(1, my_user, my_podcast)


@pytest.fixture
def my_audio_time():
    return AudioTime(5, 36, 0)


@pytest.fixture
def my_date_time():
    return datetime.strptime("2017-12-11 15:00:00+0000", "%Y-%m-%d %H:%M:%S%z")


@pytest.fixture
def my_comment(my_user, my_date_time):
    return Comment(my_user, "Good!", my_date_time)


@pytest.fixture
def my_csv_data_reader():
    dir_name = os.path.dirname(os.path.abspath(__file__))
    podcast_file_name = os.path.join(dir_name, "data/podcasts.csv")
    episode_file_name = os.path.join(dir_name, "data/episodes.csv")

    return CSVDataReader(testing=True)

@pytest.fixture
def my_playlist(my_user):
    return Playlist(1, my_user, 'My Playlist')


@pytest.fixture
def my_review(my_user, my_comment):
    return Review(my_user, my_comment)


@pytest.fixture
def client():
    my_app = create_app({
        'TESTING': True,
        'TEST_DATA_PATH': Path("podcast") / "adapters" / "data",
        'WTF_CSRF_ENABLED': False
    })

    return my_app.test_client()

class AuthenticationManager:
    def __init__(self, client):
        self.__client = client

    def login(self, user_name='Shyamli', password='Password12345'):
        return self.__client.post(
            'auth/login',
            data={'user_name': user_name, 'password': password}
        )
    def logout(self):
        return self.__client.get('/auth/logout')


@pytest.fixture
def auth(client):
    return AuthenticationManager(client)

@pytest.fixture
def client_with_user(client):
    with client.session_transaction() as sess:
        sess['logged_in'] = True
        sess['username'] = 'test_user'
    return client
