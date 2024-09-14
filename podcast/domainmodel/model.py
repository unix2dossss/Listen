from __future__ import annotations

from datetime import datetime


def validate_non_negative_int(value):
    if not isinstance(value, int) or value < 0:
        raise ValueError("ID must be a non-negative integer.")


def validate_non_empty_string(value, field_name="value"):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


def validate_time(hours, minutes, seconds):
    if not isinstance(hours, int) or hours < 0:
        raise ValueError("Hours must be a non-negative integer")
    if not isinstance(minutes, int) or minutes < 0 or minutes > 60:
        raise ValueError("Minutes must be between 0 and 59")
    if not isinstance(seconds, int) or seconds < 0 or seconds > 60:
        raise ValueError("Seconds must be between 0 and 59")


class Author:
    def __init__(self, author_id: int, name: str):
        validate_non_negative_int(author_id)
        validate_non_empty_string(name, "Author name")
        self._id = author_id
        self._name = name.strip()
        self.podcast_list = []

    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, new_name: str):
        validate_non_empty_string(new_name, "New name")
        self._name = new_name.strip()

    def add_podcast(self, podcast: Podcast):
        if not isinstance(podcast, Podcast):
            raise TypeError("Expected a Podcast instance.")
        if podcast not in self.podcast_list:
            self.podcast_list.append(podcast)

    def remove_podcast(self, podcast: Podcast):
        if podcast in self.podcast_list:
            self.podcast_list.remove(podcast)

    def __repr__(self) -> str:
        return f"<Author {self._id}: {self._name}>"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Author):
            return False
        return self.id == other.id

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Author):
            return False
        return self.name < other.name

    def __hash__(self) -> int:
        return hash(self.id)


class Podcast:
    def __init__(
        self,
        podcast_id: int,
        author: Author,
        title: str = "Untitled",
        image: str = None,
        description: str = "",
        website: str = "",
        itunes_id: int = None,
        language: str = "Unspecified",
    ):
        validate_non_negative_int(podcast_id)
        self._id = podcast_id
        self._author = author
        validate_non_empty_string(title, "Podcast title")
        self._title = title.strip()
        self._image = image
        self._description = description
        self._language = language
        self._website = website
        self._itunes_id = itunes_id
        self.categories = []
        self.episodes = []
        self._reviews = []
        self._in_playlist = False

    @property
    def id(self) -> int:
        return self._id

    @property
    def author(self) -> Author:
        return self._author

    @property
    def itunes_id(self) -> int:
        return self._itunes_id

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, new_title: str):
        validate_non_empty_string(new_title, "Podcast title")
        self._title = new_title.strip()

    @property
    def image(self) -> str:
        return self._image

    @image.setter
    def image(self, new_image: str):
        if new_image is not None and not isinstance(new_image, str):
            raise TypeError("Podcast image must be a string or None.")
        self._image = new_image

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, new_description: str):
        if not isinstance(new_description, str):
            validate_non_empty_string(new_description, "Podcast description")
        self._description = new_description

    @property
    def language(self) -> str:
        return self._language

    @language.setter
    def language(self, new_language: str):
        if not isinstance(new_language, str):
            raise TypeError("Podcast language must be a string.")
        self._language = new_language

    @property
    def website(self) -> str:
        return self._website

    @website.setter
    def website(self, new_website: str):
        validate_non_empty_string(new_website, "Podcast website")
        self._website = new_website

    @property
    def reviews(self):
        return self._reviews

    @reviews.setter
    def reviews(self, new_reviews):
        self._reviews = new_reviews

    @property
    def podcast_in_playlist(self):
        return self._in_playlist

    @podcast_in_playlist.setter
    def podcast_in_playlist(self, new_in_playlist_value):
        self._in_playlist = new_in_playlist_value

    def add_category(self, category: Category):
        if not isinstance(category, Category):
            raise TypeError("Expected a Category instance.")
        if category not in self.categories:
            self.categories.append(category)

    def remove_category(self, category: Category):
        if category in self.categories:
            self.categories.remove(category)

    def add_episode(self, episode: Episode):
        if not isinstance(episode, Episode):
            raise TypeError("Expected an Episode instance.")
        if episode not in self.episodes:
            self.episodes.append(episode)

    def remove_episode(self, episode: Episode):
        if episode in self.episodes:
            self.episodes.remove(episode)

    def add_review(self, review: Review):
        if not isinstance(review, Review):
            raise TypeError("Expected a Review instance.")
        if review not in self._reviews:
            self._reviews.append(review)

    def __repr__(self):
        return f"<Podcast {self.id}: '{self.title}' by {self.author.name}>"

    def __eq__(self, other):
        if not isinstance(other, Podcast):
            return False
        return self.id == other.id

    def __lt__(self, other):
        if not isinstance(other, Podcast):
            return False
        return self.title < other.title

    def __hash__(self):
        return hash(self.id)


class Category:
    def __init__(self, category_id: int, name: str):
        validate_non_negative_int(category_id)
        validate_non_empty_string(name, "Category name")
        self._id = category_id
        self._name = name.strip()

    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, new_name: str):
        validate_non_empty_string(new_name, "New name")
        self._name = new_name.strip()

    def __repr__(self) -> str:
        return f"<Category {self._id}: {self._name}>"

    def __eq__(self, other):
        if not isinstance(other, Category):
            return False
        return self.id == other.id

    def __lt__(self, other):
        if not isinstance(other, Category):
            return False
        return self._name < other.name

    def __hash__(self):
        return hash(self._id)


class User:
    next_user_id = 1

    def __init__(self, user_id: int, username: str, password: str):
        validate_non_negative_int(user_id)
        validate_non_empty_string(username, "Username")
        validate_non_empty_string(password, "Password")
        self._id = User.next_user_id
        User.next_user_id += 1
        self._username = username.lower().strip()
        self._password = password
        self._subscription_list = []

    @property
    def id(self) -> int:
        return self._id

    @property
    def username(self):
        return self._username

    @property
    def password(self):
        return self._password

    @property
    def subscription_list(self):
        return self._subscription_list

    def add_subscription(self, subscription: PodcastSubscription):
        if not isinstance(subscription, PodcastSubscription):
            raise TypeError("Subscription must be a PodcastSubscription object.")
        if subscription not in self._subscription_list:
            self._subscription_list.append(subscription)

    def remove_subscription(self, subscription: PodcastSubscription):
        if subscription in self._subscription_list:
            self._subscription_list.remove(subscription)

    def __repr__(self):
        return f"<User {self.id}: {self.username}>"

    def __eq__(self, other):
        if not isinstance(other, User):
            return False
        return self.id == other.id

    def __lt__(self, other):
        if not isinstance(other, User):
            return False
        return self.id < other.id

    def __hash__(self):
        return hash(self.id)


class PodcastSubscription:
    def __init__(self, sub_id: int, owner: User, podcast: Podcast):
        validate_non_negative_int(sub_id)
        if not isinstance(owner, User):
            raise TypeError("Owner must be a User object.")
        if not isinstance(podcast, Podcast):
            raise TypeError("Podcast must be a Podcast object.")
        self._id = sub_id
        self._owner = owner
        self._podcast = podcast

    @property
    def id(self) -> int:
        return self._id

    @property
    def owner(self) -> User:
        return self._owner

    @owner.setter
    def owner(self, new_owner: User):
        if not isinstance(new_owner, User):
            raise TypeError("Owner must be a User object.")
        self._owner = new_owner

    @property
    def podcast(self) -> Podcast:
        return self._podcast

    @podcast.setter
    def podcast(self, new_podcast: Podcast):
        if not isinstance(new_podcast, Podcast):
            raise TypeError("Podcast must be a Podcast object.")
        self._podcast = new_podcast

    def __repr__(self):
        return f"<PodcastSubscription {self.id}: Owned by {self.owner.username}>"

    def __eq__(self, other):
        if not isinstance(other, PodcastSubscription):
            return False
        return (
            self.id == other.id
            and self.owner == other.owner
            and self.podcast == other.podcast
        )

    def __lt__(self, other):
        if not isinstance(other, PodcastSubscription):
            return False
        return self.id < other.id

    def __hash__(self):
        return hash((self.id, self.owner, self.podcast))


class AudioTime:
    def __init__(self, hours: int, minutes: int, seconds: int):
        validate_time(hours, minutes, seconds)
        self.audio_hours: int = hours
        self.audio_minutes: int = minutes
        self.audio_seconds: int = seconds

    def __str__(self):
        return f"{self.audio_hours}h {self.audio_minutes}m {self.audio_seconds}s"

    def colon_format(self):
        return f"{self.audio_hours:02}:{self.audio_minutes:02}:{self.audio_seconds:02}"

    def __eq__(self, other):
        if not isinstance(other, AudioTime):
            return NotImplemented
        return (
            self.audio_hours == other.audio_hours
            and self.audio_minutes == other.audio_minutes
            and self.audio_seconds == other.audio_seconds
        )

    def __lt__(self, other):
        if not isinstance(other, AudioTime):
            return False
        return (self.audio_hours, self.audio_minutes, self.audio_seconds) < (
            other.audio_hours,
            other.audio_minutes,
            other.audio_seconds,
        )

    def add_time(self, other):
        if not isinstance(other, AudioTime):
            raise TypeError("Can only add AudioTime objects")

        total_seconds = self.audio_seconds + other.audio_seconds
        total_minutes = self.audio_minutes + other.audio_minutes + total_seconds // 60
        total_hours = self.audio_hours + other.audio_hours + total_minutes // 60

        new_seconds = total_seconds % 60
        new_minutes = total_minutes % 60
        new_hours = total_hours

        return AudioTime(new_hours, new_minutes, new_seconds)


class Episode:
    def __init__(
        self,
        episode_id: int,
        episode_podcast: Podcast,
        episode_title: str,
        episode_audio_link: str,
        episode_audio_length: AudioTime,
        episode_description: str,
        episode_publish_date: datetime,
    ):

        validate_non_negative_int(episode_id)
        validate_non_empty_string(episode_title, field_name="Episode Title")

        self._episode_id: int = episode_id
        self.episode_podcast: Podcast = episode_podcast
        self._episode_title: str = episode_title
        self._episode_audio_link: str = episode_audio_link
        self._episode_audio_length: AudioTime = episode_audio_length
        self._episode_description: str = episode_description
        self._episode_publish_date: datetime = episode_publish_date
        self._in_playlist: bool = False

    @property
    def episode_id(self) -> int:
        return self._episode_id

    @episode_id.setter
    def episode_id(self, new_episode_id: int):
        validate_non_negative_int(new_episode_id)
        self._episode_id = new_episode_id

    @property
    def episode_title(self) -> str:
        return self._episode_title

    @episode_title.setter
    def episode_title(self, new_episode_title: str):
        validate_non_empty_string(new_episode_title, field_name="Episode Title")
        self._episode_title = new_episode_title

    @property
    def episode_podcast(self) -> Podcast:
        return self._episode_podcast

    @episode_podcast.setter
    def episode_podcast(self, new_episode_podcast: Podcast):
        self._episode_podcast = new_episode_podcast

    @property
    def episode_audio_link(self) -> str:
        return self._episode_audio_link

    @episode_audio_link.setter
    def episode_audio_link(self, new_episode_audio_link: str):
        self._episode_audio_link = new_episode_audio_link

    @property
    def episode_audio_length(self) -> AudioTime:
        return self._episode_audio_length

    @episode_audio_length.setter
    def episode_audio_length(self, new_episode_audio_length: AudioTime):
        self._episode_audio_length = new_episode_audio_length

    @property
    def episode_description(self) -> str:
        return self._episode_description

    @episode_description.setter
    def episode_description(self, new_episode_description: str):
        self._episode_description = new_episode_description

    @property
    def episode_publish_date(self) -> datetime:
        return self._episode_publish_date

    @episode_publish_date.setter
    def episode_publish_date(self, new_episode_publish_date: datetime):
        self._episode_publish_date = new_episode_publish_date

    @property
    def episode_in_playlist(self):
        return self._in_playlist

    @episode_in_playlist.setter
    def episode_in_playlist(self, new_in_playlist_value):
        self._in_playlist = new_in_playlist_value

    def __repr__(self) -> str:
        return f"<Episode {self._episode_id}: {self._episode_title}, {self._episode_audio_length}>"

    def __str__(self) -> str:
        return f"""
            Episode ID: {self._episode_id}
            Episode Podcast: {self._episode_podcast}
            Episode Title: {self._episode_title}
            Episode Description: {self._episode_description}
            Episode Publish Date: {self._episode_publish_date}
            Episode Length: {str(self._episode_audio_length)}
            Episode Link: {self._episode_audio_link}
        """

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Episode):
            return False
        return self._episode_id == other._episode_id

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Episode):
            return False
        return self.episode_id < other.episode_id

    def __hash__(self) -> int:
        return hash(self._episode_id)


class Comment:
    next_comment_id = 1

    def __init__(self, owner: User, comment_text: str, comment_date: datetime):
        if not isinstance(owner, User):
            raise TypeError("Owner must be a User object.")
        validate_non_empty_string(comment_text, "New text")
        self._id = Comment.next_comment_id
        Comment.next_comment_id += 1
        self._owner = owner
        self._comment_text = comment_text.strip()
        self._comment_date = comment_date

    @property
    def id(self) -> int:
        return self._id

    @property
    def owner(self) -> User:
        return self._owner

    @owner.setter
    def owner(self, new_owner: User):
        if not isinstance(new_owner, User):
            raise TypeError("Owner must be a User object.")
        self._owner = new_owner

    @property
    def comment_text(self) -> str:
        return self._comment_text

    @comment_text.setter
    def comment_text(self, new_comment_text: str):
        validate_non_empty_string(new_comment_text, "New text")
        self._comment_text = new_comment_text.strip()

    @property
    def comment_date(self) -> datetime:
        return self._comment_date

    @comment_date.setter
    def comment_date(self, new_comment_date: datetime):
        self._comment_date = new_comment_date

    def __str__(self) -> str:
        return f"""
            Comment ID: {self._id}
            Comment Owner: {self._owner}
            Commented Date: {self._comment_date}
            Comment Text: {self._comment_text}
        """

    def __repr__(self) -> str:
        return f"<Comment {self._id}: Owned by {self.owner.username}>"

    def __eq__(self, other):
        if not isinstance(other, Comment):
            return False
        return self.id == other.id

    def __hash__(self):
        return None


class Review:
    next_id = 1

    def __init__(self, owner: User, comment: Comment, rating=1):
        if not isinstance(owner, User):
            raise TypeError("Owner must be a User object.")
        # self incrementing id
        self._id = Review.next_id
        Review.next_id += 1
        self._owner = owner
        self._rating = rating
        self._comment = comment

    @property
    def id(self) -> int:
        return self._id

    @property
    def owner(self) -> User:
        return self._owner

    @owner.setter
    def owner(self, new_owner: User):
        if not isinstance(new_owner, User):
            raise TypeError("Owner must be a User object.")
        self._owner = new_owner

    @property
    def rating(self) -> int:
        return self._rating

    @rating.setter
    def rating(self, new_rating: int):
        self._rating = new_rating

    @property
    def comment(self) -> Comment:
        return self._comment

    @property
    def comment_text(self) -> str:
        return self._comment.comment_text

    @comment.setter
    def comment(self, new_comment: Comment):
        self._comment = new_comment

    def __repr__(self) -> str:
        return f"<Review {self._id}: Owned by {self.owner.username}>"

    def __eq__(self, other):
        if not isinstance(other, Review):
            return False
        return self.id == other.id

    def __lt__(self, other):
        if not isinstance(other, Review):
            return False
        return self._rating < other.rating

    def __hash__(self):
        return None


class Playlist:
    next_playlist_id = 1

    def __init__(self, playlist_id: int, user: User, name: str = "Untitled"):
        validate_non_negative_int(playlist_id)
        if not isinstance(user, User):
            raise TypeError("User must be a User object.")
        self._id = Playlist.next_playlist_id
        Playlist.next_playlist_id += 1
        self._name = name.strip()
        self._user = user
        self._episodes = []
        self._podcasts = []

    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, new_name: str):
        validate_non_empty_string(new_name, "New name")
        self._name = new_name.strip()

    @property
    def user(self) -> User:
        return self._user

    @user.setter
    def user(self, new_user: User):
        if not isinstance(new_user, User):
            raise TypeError("User must be a User object.")
        self._user = new_user

    def add_episode(self, episode: Episode):
        if not isinstance(episode, Episode):
            raise TypeError("Expected an Episode instance.")
        if episode not in self._episodes:
            self._episodes.append(episode)

    def remove_episode(self, episode: Episode):
        if episode in self._episodes:
            self._episodes.remove(episode)

    def add_podcast_to_playlist(self, podcast: Podcast):
        if not isinstance(podcast, Podcast):
            raise TypeError("Expected an Episode instance.")
        if podcast not in self._podcasts:
            self._podcasts.append(podcast)
            podcast.podcast_in_playlist = True

    def remove_podcast_from_playlist(self, podcast: Podcast):
        if podcast in self._podcasts:
            self._podcasts.remove(podcast)
            podcast.podcast_in_playlist = False

    @property
    def episodes(self) -> [Episode]:
        return self._episodes

    @property
    def podcasts(self) -> [Podcast]:
        return self._podcasts

    def __repr__(self) -> str:
        return f"<Playlist {self._id}: {self._name}>"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Playlist):
            return False
        return self.id == other.id

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Playlist):
            return False
        return self.name < other.name

    def __hash__(self) -> int:
        return hash(self.id)
