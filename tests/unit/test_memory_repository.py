import pytest
from podcast.domainmodel.model import AudioTime


def test_repository_can_retrieve_a_podcast_by_id(in_memory_repo):
    # Test retrieval of a podcast by its ID.
    id_no = 1
    podcast = in_memory_repo.get_podcast(id_no)
    assert podcast == in_memory_repo.podcasts[0]


def test_repository_can_retrieve_popular_categories(in_memory_repo):
    # Test retrieval of the most popular categories.
    popular_categories = in_memory_repo.get_popular_categories()
    assert popular_categories == [
        list(in_memory_repo.categories.values())[1],
        list(in_memory_repo.categories.values())[5],
        list(in_memory_repo.categories.values())[16],
    ]


def test_can_retrieve_editor_picks(in_memory_repo):
    # Test retrieval of podcasts that are editor's picks.
    editor_picks = in_memory_repo.get_editor_picks()
    expected_picks = [
        in_memory_repo.podcasts[106],
        in_memory_repo.podcasts[503],
        in_memory_repo.podcasts[829],
    ]
    assert editor_picks == expected_picks


def test_can_retrieve_podcast_search_list(in_memory_repo):
    # Test retrieval of a list of podcasts for search functionality.
    podcast_search_list = in_memory_repo.get_podcast_search_list()
    assert podcast_search_list == [
        in_memory_repo.podcasts[288],
        in_memory_repo.podcasts[162],
        in_memory_repo.podcasts[799],
        in_memory_repo.podcasts[317],
    ]


def test_can_get_podcasts_in_specified_category(in_memory_repo):
    # Test retrieval of podcasts within a specified category.
    comedy_podcasts = in_memory_repo.get_podcasts_in_category("Comedy")
    assert comedy_podcasts == in_memory_repo.podcasts_by_category["Comedy"]


def test_can_retrieve_podcasts_by_specified_author(in_memory_repo):
    # Test retrieval of podcasts by a specific author.
    author_name = "Audioboom"
    audioboom_podcasts = in_memory_repo.get_podcasts_by_author(author_name)
    assert audioboom_podcasts == in_memory_repo.authors[author_name].podcast_list


def test_can_retrieve_all_podcasts(in_memory_repo):
    # Test retrieval of all podcasts in the repository.
    all_podcasts = in_memory_repo.get_all_podcasts()
    assert all_podcasts == in_memory_repo.podcasts


def test_can_retrieve_all_categories(in_memory_repo):
    # Test retrieval of all categories in the repository.
    all_categories = in_memory_repo.get_all_categories()
    assert all_categories == list(in_memory_repo.categories.values())


def test_can_retrieve_all_authors(in_memory_repo):
    # Test retrieval of all authors in the repository.
    all_authors = in_memory_repo.get_all_authors()
    assert all_authors == list(in_memory_repo.authors.values())


def test_can_retrieve_top_podcasts(in_memory_repo):
    # Test retrieval of top podcasts based on some criteria.
    top_podcasts = in_memory_repo.get_top_podcasts()
    assert top_podcasts == [
        in_memory_repo.podcasts[771],
        in_memory_repo.podcasts[531],
        in_memory_repo.podcasts[88],
        in_memory_repo.podcasts[438],
    ]


def test_can_retrieve_recently_played_podcasts(in_memory_repo):
    # Test retrieval of recently played podcasts.
    recent_podcasts = in_memory_repo.get_recently_played()
    assert recent_podcasts == [
        in_memory_repo.podcasts[670],
        in_memory_repo.podcasts[219],
        in_memory_repo.podcasts[728],
        in_memory_repo.podcasts[8],
    ]


def test_can_retrieve_new_podcasts(in_memory_repo):
    # Test retrieval of newly added podcasts.
    new_podcasts = in_memory_repo.get_new_podcasts()
    assert new_podcasts == [
        in_memory_repo.podcasts[739],
        in_memory_repo.podcasts[268],
        in_memory_repo.podcasts[639],
        in_memory_repo.podcasts[200],
    ]


def test_can_retrieve_continue_listening_podcasts(in_memory_repo):
    # Test retrieval of podcasts in the continue listening list.
    cl_podcasts = in_memory_repo.get_continue_listening_podcasts()
    assert cl_podcasts == [
        in_memory_repo.podcasts[546],
        in_memory_repo.podcasts[823],
        in_memory_repo.podcasts[908],
        in_memory_repo.podcasts[675],
    ]


def test_total_audio_time_addition(in_memory_repo):
    # Test the addition of audio times for a list of podcasts.
    audio_time_1 = AudioTime(1, 30, 0)
    audio_time_2 = AudioTime(0, 30, 0)
    total_time = in_memory_repo.get_total_audio_time([audio_time_1, audio_time_2])
    assert total_time.colon_format() == "02:00:00"

    # Test handling of incorrect types in audio time addition.
    with pytest.raises(TypeError):
        total_time2 = in_memory_repo.get_total_audio_time([audio_time_1, 1])


def test_can_retrieve_top_authors(in_memory_repo):
    # Test retrieval of top authors based on some criteria.
    top_authors = in_memory_repo.get_top_authors()
    assert top_authors == [
        list(in_memory_repo.authors.values())[22],
        list(in_memory_repo.authors.values())[45],
        list(in_memory_repo.authors.values())[52],
    ]


def test_can_retrieve_list_of_top_podcasts(in_memory_repo):
    # Test retrieval of a list of top podcasts.
    top_podcasts = in_memory_repo.get_top_podcasts_list()
    assert top_podcasts == in_memory_repo.podcasts[162:174]


def test_can_retrieve_list_of_recently_played_podcasts(in_memory_repo):
    # Test retrieval of a list of recently played podcasts.
    recent_podcasts = in_memory_repo.get_recently_played_list()
    assert recent_podcasts == in_memory_repo.podcasts[44:56]


def test_can_retrieve_list_of_new_podcasts(in_memory_repo):
    # Test retrieval of a list of newly added podcasts.
    new_podcasts = in_memory_repo.get_new_podcasts_list()
    assert new_podcasts == in_memory_repo.podcasts[280:292]


def test_can_add_new_user(my_user, in_memory_repo):
    # Test user is added to memory repo
    in_memory_repo.add_user(my_user)
    assert my_user in in_memory_repo.users


def test_can_add_playlist(my_playlist, in_memory_repo):
    # Test if playlist can be added to list of playlists
    in_memory_repo.add_playlist(my_playlist)
    assert my_playlist in in_memory_repo.playlists

def test_can_get_user(my_user, in_memory_repo):
    # Test if user does not exist
    user = in_memory_repo.get_user(my_user.username)
    assert user == None

    #Add user
    in_memory_repo.add_user(my_user)
    user = in_memory_repo.get_user(my_user.username)
    assert user == my_user

def test_can_get_podcast_reviews(my_podcast, my_review, in_memory_repo):
    # Test if podcast has no reviews
    reviews = in_memory_repo.get_reviews_of_podcast(my_podcast.id)
    assert reviews == []

    # Add review to podcast
    in_memory_repo.add_review(my_review, my_podcast.id)
    reviews = in_memory_repo.get_reviews_of_podcast(my_podcast.id)
    assert len(reviews) == 1

def test_can_add_review(my_review, my_podcast, in_memory_repo):
    # Test if review is added successfully
    init_reviews = len(in_memory_repo.get_reviews_of_podcast(my_podcast.id))
    in_memory_repo.add_review(my_review, my_podcast.id)
    new_reviews = len(in_memory_repo.get_reviews_of_podcast(my_podcast.id))
    assert init_reviews + 1 == new_reviews


def test_can_add_podcast(my_podcast, in_memory_repo):
    # Test if podcast is added successfully
    in_memory_repo.add_podcast(my_podcast)
    assert my_podcast in in_memory_repo.podcasts

def test_can_add_episode(my_episode, in_memory_repo):
    # Test if episode is added successfully
    in_memory_repo.add_episode(my_episode)
    assert my_episode in in_memory_repo.episodes