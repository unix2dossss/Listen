from podcast.adapters.repository import AbstractRepository

def get_popular_categories(repo: AbstractRepository):
    categories = repo.get_popular_categories()
    return categories

def get_editor_picks(repo: AbstractRepository):
    editor_picks = repo.get_editor_picks()
    return editor_picks

def get_podcast_search_list(repo: AbstractRepository):
    search_p_list = repo.get_podcast_search_list()
    return search_p_list


def format_podcast_list(podcasts):
    formatted_podcasts = []
    for i in range(len(podcasts)):
        about_podcast = dict()

        about_podcast['title'] = podcasts[i].title
        about_podcast['author'] = podcasts[i].author.name
        about_podcast['image_url'] = podcasts[i].image

        formatted_podcasts.append(about_podcast)

    return formatted_podcasts


def get_podcasts_in_category(category_name: str, repo: AbstractRepository):
    podcasts = repo.get_podcasts_in_category(category_name)
    formatted_podcasts = format_podcast_list(podcasts)
    return formatted_podcasts


def get_all_podcasts(repo: AbstractRepository):
    all_podcasts = repo.get_all_podcasts()
    formatted_podcasts = format_podcast_list(all_podcasts)
    # print(formatted_podcasts)
    return formatted_podcasts

def get_editor_picked_podcast(podcast_id: int, repo: AbstractRepository):
    editor_pick = repo.get_editor_picked_podcast(podcast_id)
    return editor_pick
