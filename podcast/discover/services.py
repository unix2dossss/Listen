from podcast.adapters.repository import AbstractRepository

def format_podcast_list(podcasts):
    formatted_podcasts = []
    for i in range(len(podcasts)):
        about_podcast = dict()

        about_podcast['id'] = podcasts[i].id
        about_podcast['title'] = podcasts[i].title
        about_podcast['author'] = podcasts[i].author.name
        about_podcast['image_url'] = podcasts[i].image
        about_podcast['language'] = podcasts[i].language
        if len(podcasts[i].episodes) > 0:
            about_podcast['duration'] = podcasts[i].episodes[0].episode_audio_length.colon_format()
        else:
            about_podcast['duration'] = "58:32:25"

        category_list = [category.name for category in podcasts[i].categories]
        if len(category_list) > 1:
            category_list = ' | '.join(category_list)
        else:
            category_list = podcasts[i].categories[0].name

        about_podcast['categories'] = category_list

        formatted_podcasts.append(about_podcast)

    return formatted_podcasts


def get_popular_categories(repo: AbstractRepository):
    categories = repo.get_popular_categories()
    return categories

def get_editor_picks(repo: AbstractRepository):
    editor_picks = repo.get_editor_picks()
    formatted_podcasts = format_podcast_list(editor_picks)
    return formatted_podcasts

def get_podcast_search_list(repo: AbstractRepository):
    search_p_list = repo.get_podcast_search_list()
    formatted_podcasts = format_podcast_list(search_p_list)
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

def get_top_podcasts(repo: AbstractRepository):
    podcasts = repo.get_top_podcasts_list()
    formatted_podcasts = format_podcast_list(podcasts)
    return formatted_podcasts


def get_recently_played(repo: AbstractRepository):
    podcasts = repo.get_recently_played_list()
    formatted_podcasts = format_podcast_list(podcasts)
    return formatted_podcasts


def get_new_podcasts(repo: AbstractRepository):
    podcasts = repo.get_new_podcasts_list()
    formatted_podcasts = format_podcast_list(podcasts)
    return formatted_podcasts
