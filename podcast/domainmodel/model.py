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
    def __init__(self, podcast_id: int, author: Author, title: str = "Untitled", image: str = None,
                 description: str = "", website: str = "", itunes_id: int = None, language: str = "Unspecified"):
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
    def __init__(self, user_id: int, username: str, password: str):
        validate_non_negative_int(user_id)
        validate_non_empty_string(username, "Username")
        validate_non_empty_string(password, "Password")
        self._id = user_id
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
        return self.id == other.id and self.owner == other.owner and self.podcast == other.podcast

    def __lt__(self, other):
        if not isinstance(other, PodcastSubscription):
            return False
        return self.id < other.id

    def __hash__(self):
        return hash((self.id, self.owner, self.podcast))


class AudioTime:
    def __init__(self, hours: int, minutes: int, seconds: int):
        validate_time(hours, minutes, seconds)
        self.hours = hours
        self.minutes = minutes
        self.seconds = seconds

    def __str__(self):
        return f"{self.hours}h {self.minutes}m {self.seconds}s"


class Episode:
    def __init__(self, episode_title: str, episode_audio_link: str, episode_audio_length: AudioTime,
                 episode_description: str, episode_publish_date: datetime):
        pass




class Review:
    def __init__(self, review_id: int, owner: User, content: str):
        validate_non_negative_int(review_id)
        if not isinstance(owner, User):
            raise TypeError("Owner must be a User object.")
        validate_non_empty_string(content, "New content")
        self._id = review_id
        self._owner = owner
        self._rating = ""
        self._content = content

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
    def rating(self) -> str:
        return self._rating

    @rating.setter
    def rating(self, new_rating: str):
        validate_non_empty_string(new_rating, "New rating")
        self._rating = new_rating.strip()

    @property
    def content(self) -> str:
        return self._content

    @content.setter
    def content(self, new_content: str):
        validate_non_empty_string(new_content, "New content")
        self._content = new_content.strip()

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

    # Use to group reviews by rating
    def __hash__(self):
        return None


class Playlist:
    def __init__(self, playlist_id: int, user: User, name: str = "Untitled"):
        validate_non_negative_int(playlist_id)
        self._id = playlist_id
        self._name = name
        self._user = user
        self._episodes = []

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

    def add_episode(self, episode: Episode):
        if not isinstance(episode, Episode):
            raise TypeError("Expected an Episode instance.")
        if episode not in self._episodes:
            self._episodes.append(episode)

    def remove_episode(self, episode: Episode):
        if episode in self._episodes:
            self._episodes.remove(episode)

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








