from podcast.adapters.repository import AbstractRepository


def get_all_authors(repo: AbstractRepository):
    authors = repo.get_all_authors()
    # print(authors)
    return authors
