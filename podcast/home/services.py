from podcast.adapters.repository import AbstractRepository


def get_top_podcasts(repo: AbstractRepository):
    podcasts = repo.get_top_podcasts()
    # formatted_podcasts = format_podcast_list(podcasts)
    return podcasts

def get_recently_played(repo: AbstractRepository):
    podcasts = repo.get_recently_played()
    # formatted_podcasts = format_podcast_list(podcasts)
    return podcasts


def get_new_podcasts(repo: AbstractRepository):
    podcasts = repo.get_new_podcasts()
    # formatted_podcasts = format_podcast_list(podcasts)
    return podcasts

