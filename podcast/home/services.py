from podcast.adapters.repository import AbstractRepository


def format_facet_podcasts(podcasts=None, condition=None, authors=None, repo=None):
    formatted_podcasts = []
    formatted_authors = []

    if authors is not None:
        for i in range(3):
            author_info = dict()
            author_info["name"] = authors[i].name
            author_info["bg"] = authors[i].podcast_list[0].image
            formatted_authors.append(author_info)
        return formatted_authors

    for i in range(len(podcasts)):
        about_podcast = dict()

        about_podcast["title"] = podcasts[i].title
        about_podcast["image_url"] = podcasts[i].image
        about_podcast["id"] = podcasts[i].id

        category_list = [category.name for category in podcasts[i].categories]
        if len(category_list) > 1:
            category_list = " · ".join(category_list)
        else:
            category_list = podcasts[i].categories[0].name

        about_podcast["categories"] = category_list

        if condition == "continue_listening":
            about_podcast["id"] = podcasts[i].id
            about_podcast["author"] = podcasts[i].author.name
            about_podcast["language"] = podcasts[i].language
            if len(podcasts[i].episodes) > 0:
                audio_times = [
                    episode.episode_audio_length for episode in podcasts[i].episodes
                ]
                total_time = repo.get_total_audio_time(audio_times)
                about_podcast["duration"] = total_time.colon_format()
            else:
                about_podcast["duration"] = "8:32:25"

        formatted_podcasts.append(about_podcast)

    return formatted_podcasts


def get_top_podcasts(repo: AbstractRepository):
    podcasts = repo.get_top_podcasts()
    formatted_podcasts = format_facet_podcasts(podcasts)
    return formatted_podcasts


def get_recently_played(repo: AbstractRepository):
    podcasts = repo.get_recently_played()
    formatted_podcasts = format_facet_podcasts(podcasts)
    return formatted_podcasts


def get_new_podcasts(repo: AbstractRepository):
    podcasts = repo.get_new_podcasts()
    formatted_podcasts = format_facet_podcasts(podcasts)
    return formatted_podcasts


def get_continue_listening_podcasts(repo: AbstractRepository):
    podcasts = repo.get_continue_listening_podcasts()
    formatted_podcasts = format_facet_podcasts(
        sorted(podcasts), "continue_listening", repo=repo
    )
    return formatted_podcasts


def get_top_authors(repo: AbstractRepository):
    authors_list = repo.get_top_authors()
    formatted_authors = format_facet_podcasts(authors=authors_list)
    return formatted_authors
