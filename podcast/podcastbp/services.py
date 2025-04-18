from podcast import Podcast
from podcast.adapters.repository import AbstractRepository
from flask import url_for, session
from datetime import datetime
import podcast.adapters.repository as repo_i
from podcast.domainmodel.model import Episode

from podcast.utilities import utilities


def get_podcast(podcast_id: int, repo: AbstractRepository):
    podcast = repo.get_podcast(podcast_id)
    return podcast


def item_in_playist(podcast: Podcast = None, episode: Episode = None):
    if "username" not in session:
        return False
    username = session["username"]
    user = utilities.get_user_by_username(username, repo_i.repo_instance)
    if podcast is not None:
        if user in podcast.podcast_playlist_users:
            return True
    else:
        if user in episode.episode_playlist_users:
            return True
    return False


def podcast_about(podcast_id: int, repo: AbstractRepository):
    podcast = get_podcast(podcast_id, repo)

    about = dict()
    about["podcast_id"] = podcast.id

    about["podcast_image"] = podcast.image
    about["podcast_title"] = podcast.title
    about["podcast_author"] = podcast.author.name
    about["podcast_description"] = podcast.description
    about["podcast_language"] = podcast.language
    about["podcast_website"] = podcast.website
    about["podcast_in_playlist"] = item_in_playist(podcast=podcast)

    return about


def podcast_categories(podcast_id: int, repo: AbstractRepository):
    podcast = get_podcast(podcast_id, repo)

    categories_list = []

    for category in podcast.categories:
        category_dict = dict()
        category_dict["category_name"] = category.name
        # to be implemented later
        # categories["category_url"] = url_for()
        categories_list.append(category_dict)

    return categories_list


def podcast_episodes(podcast_id: int, repo: AbstractRepository):
    podcast = get_podcast(podcast_id, repo)

    episodes_list = []

    sorted_episodes = sorted(
        podcast.episodes, key=lambda ep: ep.episode_publish_date, reverse=True
    )

    ep_n = 1
    for episode in sorted_episodes:
        episode_dict = dict()

        episode_dict["episode_id"] = episode.episode_id
        episode_dict["episode_number"] = ep_n
        ep_n += 1
        episode_dict["episode_title"] = episode.episode_title
        episode_dict["episode_description"] = episode.episode_description
        episode_dict["episode_date"] = episode.episode_publish_date.strftime("%Y-%m-%d")
        episode_dict["episode_length"] = str(episode.episode_audio_length)
        episode_dict["episode_in_playlist"] = item_in_playist(episode=episode)

        episodes_list.append(episode_dict)

    return episodes_list


def get_podcast_average_rating(podcast_id: int, repo: AbstractRepository):
    average_rating = repo.get_podcast_average_rating(podcast_id)
    return average_rating


def get_podcast_review_count(podcast_id: int, repo: AbstractRepository):
    podcast_reviews = repo.get_reviews_of_podcast(podcast_id)
    return len(podcast_reviews)
