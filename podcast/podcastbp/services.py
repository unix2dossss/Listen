from podcast.adapters.repository import AbstractRepository
from flask import url_for


def get_podcast(podcast_id: int, repo: AbstractRepository):
    podcast = repo.get_podcast(podcast_id)
    return podcast


def podcast_about(podcast_id: int, repo: AbstractRepository):
    podcast = get_podcast(podcast_id, repo)

    about = dict()
    about["podcast_image"] = podcast.image
    about["podcast_title"] = podcast.title
    about["podcast_author"] = podcast.author
    about["podcast_description"] = podcast.description

    return about


def podcast_categories(podcast_id: int, repo: AbstractRepository):
    podcast = get_podcast(podcast_id, repo)

    categories_list = []

    for category in podcast.categories:
        print(category)
        category_dict = dict()
        category_dict["category_name"] = category.name
        # to be implemented later
        # categories["category_url"] = url_for()
        categories_list.append(category_dict)

    return categories_list
