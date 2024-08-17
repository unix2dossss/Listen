from podcast.adapters.repository import AbstractRepository


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
    formatted_podcasts_list = format_podcast_list(podcasts)
    print('tmdkjiwf')
    print(formatted_podcasts_list)
    return formatted_podcasts_list


def get_all_podcasts():
    pass
