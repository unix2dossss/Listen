from podcast.adapters.repository import AbstractRepository
from flask import url_for
import datetime


def get_podcast(podcast_id: int, repo: AbstractRepository):
    podcast = repo.get_podcast(podcast_id)
    return podcast


def podcast_about(podcast_id: int, repo: AbstractRepository):
    podcast = get_podcast(podcast_id, repo)

    about = dict()
    about["podcast_image"] = podcast.image
    about["podcast_title"] = podcast.title
    about["podcast_author"] = podcast.author.name
    about["podcast_description"] = podcast.description

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

    ep_n = 1
    for episode in podcast.episodes:
        episode_dict = dict()

        episode_dict["episode_number"] = ep_n
        ep_n += 1
        episode_dict["episode_title"] = episode.episode_title
        episode_dict["episode_description"] = episode.episode_description
        episode_dict["episode_date"] = episode.episode_publish_date.strftime('%Y-%m-%d')
        episode_dict["episode_length"] = str(episode.episode_audio_length)

        episodes_list.append(episode_dict)

    return episodes_list
