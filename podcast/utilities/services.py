from podcast.adapters.repository import AbstractRepository


def get_n_podcasts(quantity=3):
    pass


def get_user_by_username(username: str, repo: AbstractRepository):
    user = repo.get_user(username)
    return user
