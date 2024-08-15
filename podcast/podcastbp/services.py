from podcast.adapters.repository import AbstractRepository


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
