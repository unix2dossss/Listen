from podcast.adapters.repository import AbstractRepository

def get_all_categories(repo: AbstractRepository):
    categories = repo.get_all_categories()
    return categories
