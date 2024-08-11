import pytest
from datetime import datetime
from podcast.domainmodel.model import Author, Podcast, Category, User, PodcastSubscription, Episode, AudioTime, Comment, Review, Playlist
from podcast.adapters.datareader.csvdatareader import CSVDataReader


def test_author_initialization():
    author1 = Author(1, "Brian Denny")
    assert repr(author1) == "<Author 1: Brian Denny>"
    assert author1.name == "Brian Denny"

    with pytest.raises(ValueError):
        author2 = Author(2, "")

    with pytest.raises(ValueError):
        author3 = Author(3, 123)

    author4 = Author(4, " USA Radio   ")
    assert author4.name == "USA Radio"

    author4.name = "Jackson Mumey"
    assert repr(author4) == "<Author 4: Jackson Mumey>"


def test_author_eq():
    author1 = Author(1, "Author A")
    author2 = Author(1, "Author A")
    author3 = Author(3, "Author B")
    assert author1 == author2
    assert author1 != author3
    assert author3 != author2
    assert author3 == author3


def test_author_lt():
    author1 = Author(1, "Jackson Mumey")
    author2 = Author(2, "USA Radio")
    author3 = Author(3, "Jesmond Parish Church")
    assert author1 < author2
    assert author2 > author3
    assert author1 < author3
    author_list = [author3, author2, author1]
    assert sorted(author_list) == [author1, author3, author2]


def test_author_hash():
    authors = set()
    author1 = Author(1, "Doctor Squee")
    author2 = Author(2, "USA Radio")
    author3 = Author(3, "Jesmond Parish Church")
    authors.add(author1)
    authors.add(author2)
    authors.add(author3)
    assert len(authors) == 3
    assert repr(
        sorted(authors)) == "[<Author 1: Doctor Squee>, <Author 3: Jesmond Parish Church>, <Author 2: USA Radio>]"
    authors.discard(author1)
    assert repr(sorted(authors)) == "[<Author 3: Jesmond Parish Church>, <Author 2: USA Radio>]"


def test_author_name_setter():
    author = Author(1, "Doctor Squee")
    author.name = "   USA Radio  "
    assert repr(author) == "<Author 1: USA Radio>"

    with pytest.raises(ValueError):
        author.name = ""

    with pytest.raises(ValueError):
        author.name = 123


def test_category_initialization():
    category1 = Category(1, "Comedy")
    assert repr(category1) == "<Category 1: Comedy>"
    category2 = Category(2, " Christianity ")
    assert repr(category2) == "<Category 2: Christianity>"

    with pytest.raises(ValueError):
        category3 = Category(3, 300)

    category5 = Category(5, " Religion & Spirituality  ")
    assert category5.name == "Religion & Spirituality"

    with pytest.raises(ValueError):
        category1 = Category(4, "")


def test_category_name_setter():
    category1 = Category(6, "Category A")
    assert category1.name == "Category A"

    with pytest.raises(ValueError):
        category1 = Category(7, "")

    with pytest.raises(ValueError):
        category1 = Category(8, 123)


def test_category_eq():
    category1 = Category(9, "Action")
    category2 = Category(10, "Indie")
    category3 = Category(11, "Sports")
    assert category1 == category1
    assert category1 != category2
    assert category2 != category3
    assert category1 != "9: Adventure"
    assert category2 != 105


def test_category_hash():
    category1 = Category(9, "Action")
    category2 = Category(10, "Indie")
    category3 = Category(11, "Sports")
    category_set = set()
    category_set.add(category1)
    category_set.add(category2)
    category_set.add(category3)
    assert sorted(category_set) == [category1, category2, category3]
    category_set.discard(category2)
    category_set.discard(category1)
    assert sorted(category_set) == [category3]


def test_category_lt():
    category1 = Category(9, "Action")
    category2 = Category(10, "Indie")
    category3 = Category(11, "Sports")
    assert category1 < category2
    assert category2 < category3
    assert category3 > category1
    category_list = [category3, category2, category1]
    assert sorted(category_list) == [category1, category2, category3]


# Fixtures to reuse in multiple tests
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
    return Comment(1, my_user, "Good!", my_date_time)


def test_podcast_initialization():
    author1 = Author(1, "Doctor Squee")
    podcast1 = Podcast(2, author1, "My First Podcast")
    assert podcast1.id == 2
    assert podcast1.author == author1
    assert podcast1.title == "My First Podcast"
    assert podcast1.description == ""
    assert podcast1.website == ""

    assert repr(podcast1) == "<Podcast 2: 'My First Podcast' by Doctor Squee>"

    with pytest.raises(ValueError):
        podcast3 = Podcast(-123, "Todd Clayton")

    podcast4 = Podcast(123, " ")
    assert podcast4.title is 'Untitled'
    assert podcast4.image is None


def test_podcast_change_title(my_podcast):
    my_podcast.title = "TourMix Podcast"
    assert my_podcast.title == "TourMix Podcast"

    with pytest.raises(ValueError):
        my_podcast.title = ""


def test_podcast_add_category(my_podcast):
    category = Category(12, "TV & Film")
    my_podcast.add_category(category)
    assert category in my_podcast.categories
    assert len(my_podcast.categories) == 1

    my_podcast.add_category(category)
    my_podcast.add_category(category)
    assert len(my_podcast.categories) == 1


def test_podcast_remove_category(my_podcast):
    category1 = Category(13, "Technology")
    my_podcast.add_category(category1)
    my_podcast.remove_category(category1)
    assert len(my_podcast.categories) == 0

    category2 = Category(14, "Science")
    my_podcast.add_category(category1)
    my_podcast.remove_category(category2)
    assert len(my_podcast.categories) == 1


def test_podcast_title_setter(my_podcast):
    my_podcast.title = "Dark Throne"
    assert my_podcast.title == 'Dark Throne'

    with pytest.raises(ValueError):
        my_podcast.title = " "

    with pytest.raises(ValueError):
        my_podcast.title = ""


def test_podcast_eq():
    author1 = Author(1, "Author A")
    author2 = Author(2, "Author C")
    author3 = Author(3, "Author B")
    podcast1 = Podcast(100, author1, "Joe Toste Podcast - Sales Training Expert")
    podcast2 = Podcast(200, author2, "Voices in AI")
    podcast3 = Podcast(101, author3, "Law Talk")
    assert podcast1 == podcast1
    assert podcast1 != podcast2
    assert podcast2 != podcast3


def test_podcast_hash():
    author1 = Author(1, "Author A")
    author2 = Author(2, "Author C")
    author3 = Author(3, "Author B")
    podcast1 = Podcast(100, author1, "Joe Toste Podcast - Sales Training Expert")
    podcast2 = Podcast(100, author2, "Voices in AI")
    podcast3 = Podcast(101, author3, "Law Talk")
    podcast_set = {podcast1, podcast2, podcast3}
    assert len(podcast_set) == 2  # Since podcast1 and podcast2 have the same ID


def test_podcast_lt():
    author1 = Author(1, "Author A")
    author2 = Author(2, "Author C")
    author3 = Author(3, "Author B")
    podcast1 = Podcast(100, author1, "Joe Toste Podcast - Sales Training Expert")
    podcast2 = Podcast(200, author2, "Voices in AI")
    podcast3 = Podcast(101, author3, "Law Talk")
    assert podcast1 < podcast2
    assert podcast2 > podcast3
    assert podcast3 > podcast1


def test_user_initialization():
    user1 = User(1, "Shyamli", "pw12345")
    user2 = User(2, "asma", "pw67890")
    user3 = User(3, "JeNNy  ", "pw87465")
    assert repr(user1) == "<User 1: shyamli>"
    assert repr(user2) == "<User 2: asma>"
    assert repr(user3) == "<User 3: jenny>"
    assert user2.password == "pw67890"
    with pytest.raises(ValueError):
        user4 = User(4, "xyz  ", "")
    with pytest.raises(ValueError):
        user4 = User(5, "    ", "qwerty12345")


def test_user_eq():
    user1 = User(1, "Shyamli", "pw12345")
    user2 = User(2, "asma", "pw67890")
    user3 = User(3, "JeNNy  ", "pw87465")
    user4 = User(1, "Shyamli", "pw12345")
    assert user1 == user4
    assert user1 != user2
    assert user2 != user3


def test_user_hash():
    user1 = User(1, "   Shyamli", "pw12345")
    user2 = User(2, "asma", "pw67890")
    user3 = User(3, "JeNNy  ", "pw87465")
    user_set = set()
    user_set.add(user1)
    user_set.add(user2)
    user_set.add(user3)
    assert sorted(user_set) == [user1, user2, user3]
    user_set.discard(user1)
    user_set.discard(user2)
    assert list(user_set) == [user3]


def test_user_lt():
    user1 = User(1, "Shyamli", "pw12345")
    user2 = User(2, "asma", "pw67890")
    user3 = User(3, "JeNNy  ", "pw87465")
    assert user1 < user2
    assert user2 < user3
    assert user3 > user1
    user_list = [user3, user2, user1]
    assert sorted(user_list) == [user1, user2, user3]


def test_user_add_remove_favourite_podcasts(my_user, my_subscription):
    my_user.add_subscription(my_subscription)
    assert repr(my_user.subscription_list) == "[<PodcastSubscription 1: Owned by shyamli>]"
    my_user.add_subscription(my_subscription)
    assert len(my_user.subscription_list) == 1
    my_user.remove_subscription(my_subscription)
    assert repr(my_user.subscription_list) == "[]"


def test_podcast_subscription_initialization(my_subscription):
    assert my_subscription.id == 1
    assert repr(my_subscription.owner) == "<User 1: shyamli>"
    assert repr(my_subscription.podcast) == "<Podcast 100: 'Joe Toste Podcast - Sales Training Expert' by Joe Toste>"

    assert repr(my_subscription) == "<PodcastSubscription 1: Owned by shyamli>"


def test_podcast_subscription_set_owner(my_subscription):
    new_user = User(2, "asma", "pw67890")
    my_subscription.owner = new_user
    assert my_subscription.owner == new_user

    with pytest.raises(TypeError):
        my_subscription.owner = "not a user"


def test_podcast_subscription_set_podcast(my_subscription):
    author2 = Author(2, "Author C")
    new_podcast = Podcast(200, author2, "Voices in AI")
    my_subscription.podcast = new_podcast
    assert my_subscription.podcast == new_podcast

    with pytest.raises(TypeError):
        my_subscription.podcast = "not a podcast"


def test_podcast_subscription_equality(my_user, my_podcast):
    sub1 = PodcastSubscription(1, my_user, my_podcast)
    sub2 = PodcastSubscription(1, my_user, my_podcast)
    sub3 = PodcastSubscription(2, my_user, my_podcast)
    assert sub1 == sub2
    assert sub1 != sub3


def test_podcast_subscription_hash(my_user, my_podcast):
    sub1 = PodcastSubscription(1, my_user, my_podcast)
    sub2 = PodcastSubscription(1, my_user, my_podcast)
    sub_set = {sub1, sub2}  # Should only contain one element since hash should be the same
    assert len(sub_set) == 1

# TODO : Write Unit Tests for CSVDataReader, Episode, Review, Playlist classes


# Audio Class Tests
def test_audiotime_initialization():
    # test negative hours, minutes and seconds
    with pytest.raises(ValueError):
        audiotime_obj1 = AudioTime(-1, 20, 30)
    with pytest.raises(ValueError):
        audiotime_obj1 = AudioTime(1, -20, 30)
    with pytest.raises(ValueError):
        audiotime_obj1 = AudioTime(1, 20, -30)

    # test string hours, minutes, seconds
    with pytest.raises(ValueError):
        audiotime_obj1 = AudioTime("2", 20, 30)
    with pytest.raises(ValueError):
        audiotime_obj1 = AudioTime(2, "20", 30)
    with pytest.raises(ValueError):
        audiotime_obj1 = AudioTime(2, 20, "30")

    # test 0 hours, minutes, seconds
    zero_hours_obj = AudioTime(0, 20, 30)
    zero_minutes_obj = AudioTime(20, 0, 30)
    zero_seconds_obj = AudioTime(20, 30, 0)
    assert zero_hours_obj.audio_hours == 0
    assert zero_minutes_obj.audio_minutes == 0
    assert zero_seconds_obj.audio_seconds == 0

    # test 0 hours, 0 minutes, 0 seconds all together (invalid)
    with pytest.raises(ValueError):
        audiotime_obj2 = AudioTime(0, 0, 0)


def test_audiotime_str(my_audio_time):
    assert str(my_audio_time) == "5h 36m 0s"


def test_audiotime_lt():
    time1 = AudioTime(2, 30, 15)
    time2 = AudioTime(3, 25, 10)
    time3 = AudioTime(2, 29, 59)
    time4 = AudioTime(2, 30, 15)
    time5 = AudioTime(0, 0, 2)
    time6 = AudioTime(0, 0, 1)

    assert time1 < time2  # time1 < time2 (hours)
    assert time3 < time1  # time3 < time1 (minutes)
    assert time6 < time5  # time6 < time5 (seconds)

    assert not time1 < time4
    assert time5 > time6

    # Edge Cases
    time1 = AudioTime(2, 0, 0)
    time2 = AudioTime(1, 59, 59)

    # Test hours comparison
    assert time2 < time1

    time3 = AudioTime(3, 0, 0)
    time4 = AudioTime(2, 59, 59)

    assert not time3 < time4

# Episode Class Tests
def test_episode_initialization(my_podcast, my_audio_time, my_date_time):
    episode1 = Episode(1,
                       my_podcast,
                       "1: Festive food and farming",
                       "https://audioboom.com/posts/6546476.mp3?source=rss&stitched=1",
                       my_audio_time,
                       """
                       <p>John Bates hosts this festive special from the AHDB consumer insights team looking at how the 
                       season of goodwill changes what and how we buy, how Brexit might impact our favourite festive 
                       foods and what farmers and growers need to think about to gear up for Christmas future.</p><p>
                       <a href="https://ahdb.org.uk/">https://ahdb.org.uk/</a></p><p>Photo by Keenan Loo on Unsplash</p>
                       """, my_date_time)

    # Random Episode 2 for same Podcast as episode1
    episode2 = Episode(2,
                       my_podcast,
                       "2: Episode 2 Under Same Podcast",
                       "https://audioboom.com/posts/6546476.mp3?source=rss&stitched=1",
                       my_audio_time,
                       "This is a test episode. Episode 2", my_date_time)

    assert repr(episode1) == "<Episode 1: 1: Festive food and farming, 5h 36m 0s>"
    assert repr(episode2) == "<Episode 2: 2: Episode 2 Under Same Podcast, 5h 36m 0s>"

    assert episode2.episode_description == "This is a test episode. Episode 2"
    assert episode2.episode_audio_link == "https://audioboom.com/posts/6546476.mp3?source=rss&stitched=1"

    # test validate_non_negative_int
    with pytest.raises(ValueError):
        episode3 = Episode(-3,
                           my_podcast,"2: Episode 2 Under Same Podcast",
                           "https://audioboom.com/posts/6546476.mp3?source=rss&stitched=1",
                           my_audio_time, "This is a test episode. Episode 3", my_date_time)

    # test validate_non_empty_string
    with pytest.raises(ValueError):
        episode4 = Episode(4,
                           my_podcast, "",
                           "https://audioboom.com/posts/6546476.mp3?source=rss&stitched=1",
                           my_audio_time, "This is a test episode. Episode 4", my_date_time)


def test_episode_eq(my_podcast, my_audio_time, my_date_time):
    episode1 = Episode(1,
                       my_podcast, "4 Spaces",
                       "https://audioboom.com/posts/6546476.mp3?source=rss&stitched=1",
                       my_audio_time, "This is a test episode. Episode 1", my_date_time)

    episode2 = Episode(1,
                       my_podcast, "4 Spaces",
                       "https://audioboom.com/posts/6546476.mp3?source=rss&stitched=1",
                       my_audio_time, "This is a test episode. Episode 1", my_date_time)

    episode3 = Episode(3,
                       my_podcast, "A different Episode",
                       "https://audioboom.com/posts/6546476.mp3?source=rss&stitched=1",
                       my_audio_time, "This is a test episode. Episode 3", my_date_time)

    assert episode1 == episode2
    assert episode1 != episode3
    assert episode2 != episode3

def test_episode_hash(my_podcast, my_audio_time, my_date_time):
    episode1 = Episode(1,
                       my_podcast, "Test Episode 1",
                       "https://audioboom.com/posts/6546476.mp3?source=rss&stitched=1",
                       my_audio_time, "This is a test episode. Episode 1", my_date_time)

    episode2 = Episode(2,
                       my_podcast, "Test Episode 2",
                       "https://audioboom.com/posts/6546476.mp3?source=rss&stitched=1",
                       my_audio_time, "This is a test episode. Episode 2", my_date_time)

    episode3 = Episode(3,
                       my_podcast, "Test Episode 3",
                       "https://audioboom.com/posts/6546476.mp3?source=rss&stitched=1",
                       my_audio_time, "This is a test episode. Episode 3", my_date_time)

    episode_set = set()
    episode_set.add(episode1)
    episode_set.add(episode2)
    episode_set.add(episode3)

    assert sorted(episode_set) == [episode1, episode2, episode3]

    episode_set.discard(episode1)
    episode_set.discard(episode2)
    assert list(episode_set) == [episode3]


def test_episode_lt(my_podcast, my_audio_time, my_date_time):
    episode1 = Episode(1,
                       my_podcast, "Test Episode 1",
                       "https://audioboom.com/posts/6546476.mp3?source=rss&stitched=1",
                       my_audio_time, "This is a test episode. Episode 1", my_date_time)

    episode2 = Episode(2,
                       my_podcast, "Test Episode 2",
                       "https://audioboom.com/posts/6546476.mp3?source=rss&stitched=1",
                       my_audio_time, "This is a test episode. Episode 2", my_date_time)

    episode3 = Episode(3,
                       my_podcast, "Test Episode 3",
                       "https://audioboom.com/posts/6546476.mp3?source=rss&stitched=1",
                       my_audio_time, "This is a test episode. Episode 3", my_date_time)

    assert episode1 < episode2
    assert episode2 < episode3
    assert episode3 > episode1
    user_list = [episode1, episode2, episode3]
    assert sorted(user_list) == [episode1, episode2, episode3]


def test_episode_setters(my_podcast, my_audio_time, my_date_time):
    episode1 = Episode(1,
                       my_podcast, "1: Festive food and farming",
                       "https://audioboom.com/posts/6546476.mp3?source=rss&stitched=1",
                       my_audio_time, "Temporary shortened test description", my_date_time)

    # set new invalid ID
    with pytest.raises(ValueError):
        episode1.episode_id = -2
    # set new valid ID
    episode1.episode_id = 2
    assert episode1.episode_id == 2

    # test new invalid str attribute setter (Title) - just need to test validate once.
    with pytest.raises(ValueError):
        episode1.episode_title = ""

    # test getter
    assert episode1.episode_title == "1: Festive food and farming"
    # test valid str attribute setter
    episode1.episode_title = "The Forbidden Tomb"
    assert episode1.episode_title == "The Forbidden Tomb"
    episode1.episode_audio_link = "https://testlink.com"
    assert episode1.episode_audio_link == "https://testlink.com"

    new_audio_length = AudioTime(4, 20, 24)
    episode1.episode_audio_length = new_audio_length
    assert str(episode1.episode_audio_length) == "4h 20m 24s"

    episode1.episode_description = "This is the new episode description"
    assert episode1.episode_description == "This is the new episode description"

    new_date_time_obj = datetime.strptime("2012-12-12 15:00:00+0000", "%Y-%m-%d %H:%M:%S%z")
    episode1.episode_publish_date = new_date_time_obj
    assert episode1.episode_publish_date == new_date_time_obj
    # test str(Episode)
    assert str(episode1) == """
            Episode ID: 2
            Episode Podcast: <Podcast 100: 'Joe Toste Podcast - Sales Training Expert' by Joe Toste>
            Episode Title: The Forbidden Tomb
            Episode Description: This is the new episode description
            Episode Publish Date: 2012-12-12 15:00:00+00:00
            Episode Length: 4h 20m 24s
            Episode Link: https://testlink.com
        """

# Comment Class Tests
def test_comment_initialization(my_user, my_date_time):
    comment1 = Comment(1, my_user, "Good!", my_date_time)
    assert repr(comment1) == "<Comment 1: Owned by shyamli>"
    assert comment1.comment_text == "Good!"

    # test with passing invalid values

    # pass an invalid ID
    with pytest.raises(ValueError):
        comment2 = Comment(-2, my_user, "Good!", my_date_time)

    # pass an Author object instead of User object
    with pytest.raises(TypeError):
        comment3 = Comment(3, my_author, "Good!", my_date_time)

    # pass an empty string for comment_text
    with pytest.raises(ValueError):
        comment3 = Comment(3, my_user, "", my_date_time)

    comment4 = Comment(4, my_user, "  Good!  ", my_date_time)
    assert comment4.comment_text == "Good!"


def test_comment_eq(my_user, my_date_time):
    comment1 = Comment(1, my_user, "Good!", my_date_time)
    comment2 = Comment(1, my_user, "Nice!", my_date_time)
    comment3 = Comment(3, my_user, "Awesome!", my_date_time)
    assert comment1 == comment2
    assert comment1 != comment3
    assert comment3 != comment2
    assert comment3 == comment3


def test_comment_str(my_user, my_date_time):
    comment1 = Comment(1, my_user, "Good!", my_date_time)
    assert str(comment1) == """
            Comment ID: 1
            Comment Owner: <User 1: shyamli>
            Commented Date: 2017-12-11 15:00:00+00:00
            Comment Text: Good!
        """

# Test setters
def test_comment_setters(my_user, my_date_time, my_author):
    comment1 = Comment(1, my_user, "Good!", my_date_time)

    # set new invalid Owner by setting an Author object instead of User object
    with pytest.raises(TypeError):
        comment1.owner = my_author
    # set new valid object type for Owner
    user1 = User(1, "John", "123")
    comment1.owner = user1
    assert comment1.owner == user1


    # test new invalid str attribute for comment_text
    with pytest.raises(ValueError):
        comment1.comment_text = ""

    user1 = User(1, "John", "123")
    comment1.owner = user1
    assert comment1.owner == user1

    # set new comment_date
    new_date_time_obj = datetime.strptime("2024-11-01 15:00:00+0000", "%Y-%m-%d %H:%M:%S%z")
    comment1.comment_date = new_date_time_obj
    assert comment1.comment_date == new_date_time_obj

# Test getters
def test_comment_getters(my_user, my_date_time):
    comment1 = Comment(1, my_user, "Good!", my_date_time)

    assert comment1.id == 1
    assert comment1.owner == my_user
    assert comment1.comment_text == "Good!"
    assert comment1.comment_date == my_date_time

# Review Class Tests
def test_review_initialization(my_user, my_comment, my_author):
    review1 = Review(1, my_user, my_comment)
    assert repr(review1) == "<Review 1: Owned by shyamli>"

    # test with passing invalid values

    # pass an invalid ID
    with pytest.raises(ValueError):
        review2 = Review(-2, my_user, my_comment)

    # pass an Author object instead of User object
    with pytest.raises(TypeError):
        review3 = Review(3, my_author, my_comment)

    # # pass an empty string for comment_text
    # with pytest.raises(TypeError):
    #     review4 = Review(4, my_user, my_comment)


def test_review_eq(my_user, my_comment):
    review1 = Review(1, my_user, my_comment)
    review2 = Review(1, my_user, my_comment)
    review3 = Review(2, my_user, my_comment)
    assert review1 == review2
    assert review1 != review3
    assert review3 != review2
    assert review3 == review3


def test_review_lt(my_user, my_comment):
    review1 = Review(1, my_user, my_comment)
    review2 = Review(1, my_user, my_comment)
    review3 = Review(2, my_user, my_comment)

    review1.rating = "*"
    review2.rating = "**"
    review3.rating = "***"

    assert review1 < review2
    assert review2 < review3
    assert review3 > review1

# Test setters
def test_review_setters(my_user, my_comment, my_author, my_date_time):
    review1 = Review(1, my_user, my_comment)

    # set new invalid Owner by setting an Author object instead of User object
    with pytest.raises(TypeError):
        review1.owner = my_author
    # set new valid object type for Owner
    user1 = User(1, "John", "123")
    review1.owner = user1
    assert review1.owner == user1


    # test new invalid str attribute for rating
    with pytest.raises(ValueError):
        review1.rating = ""

    review1.rating = " ** "
    assert review1.rating == "**"

    # set new comment
    comment1 = Comment(2, my_user, "So Good!", my_date_time)
    review1.comment = comment1
    assert review1.comment == comment1


# Test getters
def test_review_getters(my_user, my_comment, my_author):
    review1 = Review(3, my_user, my_comment)

    assert review1.id == 3
    assert review1.owner == my_user
    assert review1.rating == ""       # initially rating is an empty string
    assert review1.comment == my_comment
    assert review1.comment_text == "Good!"

    review1.rating = "***"
    assert review1.rating == "***"


# Playlist Class Tests
def test_podcast_initialisation(my_user, my_author):
    playlist1 = Playlist(1, my_user)
    assert playlist1.id == 1
    assert playlist1.user == my_user
    assert playlist1.name == "Untitled"

    assert repr(playlist1) == "<Playlist 1: Untitled>"

    # Invalid values entered
    with pytest.raises(ValueError):
        playlist2 = Playlist(-3, my_user)

    with pytest.raises(TypeError):
        playlist3 = Playlist(3, my_author)

    playlist4 = Playlist(4, my_user, "History for Weirdos")
    assert playlist4.name == "History for Weirdos"

    playlist5 = Playlist(5, my_user, "   PodName   ")
    assert playlist5.name == "PodName"

def test_playlist_eq(my_user):
    playlist1 = Playlist(1, my_user)
    playlist2 = Playlist(2, my_user)
    playlist3 = Playlist(1, my_user, "Once Upon a Time")
    playlist4 = Playlist(3, my_user, "ABC")
    assert playlist1 == playlist1
    assert playlist1 == playlist3
    assert playlist2 != playlist3
    assert playlist2 != playlist3
    assert playlist3 != playlist4

def test_playlist_lt():
    playlist1 = Playlist(1, "ABC")
    playlist2 = Playlist(2, "BCD")
    playlist3 = Playlist(3, "CDE")
    assert playlist1 < playlist2
    assert playlist2 > playlist3
    assert playlist1 < playlist3
    playlist_list = [playlist3, playlist2, playlist1]
    assert sorted(playlist_list) == [playlist1, playlist2, playlist3]

def test_playlist_getters(my_user):
    playlist1 = Playlist(1, my_user, "ABC")
    assert playlist1.id == 1
    assert playlist1.name == "ABC"
    assert playlist1.user == my_user

def test_playlist_name_setter(my_user):
    playlist1 = Playlist(1, my_user, "ABC")
    playlist1.name = "XYZ"
    assert playlist1.name == "XYZ"

    playlist2 = Playlist(2, my_user)
    playlist2.name = "  AAA  "
    assert playlist2.name == "AAA"

    with pytest.raises(ValueError):
        my_podcast.title = " "

    with pytest.raises(ValueError):
        my_podcast.title = ""















