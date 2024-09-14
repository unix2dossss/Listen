from podcast.adapters.repository import AbstractRepository
from podcast.domainmodel.model import User, Playlist


def format_podcast_list(podcasts, repo=None):
    formatted_podcasts = []
    for i in range(len(podcasts)):
        about_podcast = dict()

        about_podcast["id"] = podcasts[i].id
        about_podcast["title"] = podcasts[i].title
        about_podcast["author"] = podcasts[i].author.name
        about_podcast["image_url"] = podcasts[i].image
        about_podcast["language"] = podcasts[i].language
        about_podcast["podcast_in_playlist"] = podcasts[i].podcast_in_playlist

        if repo is not None:
            if len(podcasts[i].episodes) > 0:
                audio_times = [
                    episode.episode_audio_length for episode in podcasts[i].episodes
                ]
                total_time = repo.get_total_audio_time(audio_times)
                about_podcast["duration"] = total_time.colon_format()
            else:
                about_podcast["duration"] = "8:32:25"

        category_list = [category.name for category in podcasts[i].categories]
        if len(category_list) > 1:
            category_list = " | ".join(category_list)
        else:
            category_list = podcasts[i].categories[0].name

        about_podcast["categories"] = category_list

        formatted_podcasts.append(about_podcast)

    return formatted_podcasts


def get_user_playlist_podcasts(user: User, repo_instance):
    user_playlist: Playlist = get_user_playlist(user, repo_instance)
    podcasts = user_playlist.podcasts
    formatted_podcasts = format_podcast_list(sorted(podcasts))
    return formatted_podcasts


def get_user_playlist_episodes(user: User, repo_instance):
    user_playlist: Playlist = get_user_playlist(user, repo_instance)
    playlist_episodes = user_playlist.episodes

    playlist_episodes_out = []

    ep_n = 1
    for episode in playlist_episodes:
        episode_dict = dict()

        episode_dict["episode_in_playlist"] = episode.episode_in_playlist
        episode_dict["podcast_image"] = episode.episode_podcast.image
        episode_dict["episode_id"] = episode.episode_id
        episode_dict["episode_number"] = ep_n
        ep_n += 1
        episode_dict["episode_title"] = episode.episode_title
        episode_dict["episode_description"] = episode.episode_description
        episode_dict["episode_date"] = episode.episode_publish_date.strftime("%Y-%m-%d")
        episode_dict["episode_length"] = str(episode.episode_audio_length)

        playlist_episodes_out.append(episode_dict)

    return playlist_episodes_out


def get_user_playlist(user: User, repo: AbstractRepository):
    return repo.get_user_playlist(user)


def add_to_podcast_playlist(user: User, podcast_id, repo: AbstractRepository):
    playlist = get_user_playlist(user, repo)
    print(playlist)
    podcast = repo.get_podcast(int(podcast_id))
    playlist.add_podcast_to_playlist(podcast)
    print(playlist.podcasts)
    return None


def remove_from_podcast_playlist(user, podcast_id, repo_instance: AbstractRepository):
    playlist = get_user_playlist(user, repo_instance)
    podcast = repo_instance.get_podcast(int(podcast_id))
    print(podcast)
    playlist.remove_podcast_from_playlist(podcast)
    return None


def add_to_episode_playlist(user: User, episode_id, repo: AbstractRepository):
    playlist: Playlist = get_user_playlist(user, repo)
    print(playlist)
    episode = repo.get_episode(int(episode_id))
    playlist.add_episode(episode)
    print(playlist.episodes)
    return None


def remove_from_episode_playlist(user, episode_id, repo_instance: AbstractRepository):
    playlist: Playlist = get_user_playlist(user, repo_instance)
    episode = repo_instance.get_episode(int(episode_id))
    playlist.remove_episode(episode)
    return None
