from podcast.adapters.repository import AbstractRepository


def get_podcasts_by_category(category_id: int, repo: AbstractRepository):
    podcasts = repo.get_podcasts_in_category(category_id)
    # print(podcasts)
    return podcasts
