def test_repository_can_retrieve_a_podcast_by_id(in_memory_repo):
    id_no = 1
    podcast = in_memory_repo.get_podcast(id_no)
    assert podcast == in_memory_repo.podcasts[0]


def test_repository_can_retrieve_popular_categories(in_memory_repo):
    popular_categories = in_memory_repo.get_popular_categories()
    assert popular_categories == [list(in_memory_repo.categories.values())[1],
                                  list(in_memory_repo.categories.values())[5],
                                  list(in_memory_repo.categories.values())[16]]


def test_can_retrieve_editor_picks(in_memory_repo):
    editor_picks = in_memory_repo.get_editor_picks()
    expected_picks = [in_memory_repo.podcasts[106], in_memory_repo.podcasts[503],
                      in_memory_repo.podcasts[829]]

    assert editor_picks == expected_picks


def test_can_get_podcasts_in_specified_category(in_memory_repo):
    comedy_podcasts = in_memory_repo.get_podcasts_in_category('Comedy')
    assert comedy_podcasts == in_memory_repo.podcasts_by_category['Comedy']


def test_can_retrieve_podcasts_by_specified_author(in_memory_repo):
    author_name = "Audioboom"
    audioboom_podcasts = in_memory_repo.get_podcasts_by_author(author_name)
    assert audioboom_podcasts == in_memory_repo.authors[author_name].podcast_list


def test_can_retrieve_all_podcasts(in_memory_repo):
    all_podcasts = in_memory_repo.get_all_podcasts()
    assert all_podcasts == in_memory_repo.podcasts


def test_can_retrieve_all_categories(in_memory_repo):
    all_categories = in_memory_repo.get_all_categories()
    assert all_categories == list(in_memory_repo.categories.values())


def test_can_retrieve_all_authors(in_memory_repo):
    all_authors = in_memory_repo.get_all_authors()
    assert all_authors == list(in_memory_repo.authors.values())


def test_can_retrieve_top_podcasts(in_memory_repo):
    top_podcasts = in_memory_repo.get_top_podcasts()
    assert top_podcasts == [in_memory_repo.podcasts[771], in_memory_repo.podcasts[531],
                            in_memory_repo.podcasts[88], in_memory_repo.podcasts[438]]


def test_can_retrieve_recently_played_podcasts(in_memory_repo):
    recent_podcasts = in_memory_repo.get_recently_played()
    assert recent_podcasts == [in_memory_repo.podcasts[670], in_memory_repo.podcasts[219],
                               in_memory_repo.podcasts[728], in_memory_repo.podcasts[8]]


def test_can_retrieve_new_podcasts(in_memory_repo):
    new_podcasts = in_memory_repo.get_new_podcasts()
    assert new_podcasts == [in_memory_repo.podcasts[739], in_memory_repo.podcasts[268],
                            in_memory_repo.podcasts[639], in_memory_repo.podcasts[200]]


def test_can_retrieve_continue_listening_podcasts(in_memory_repo):
    cl_podcasts = in_memory_repo.get_continue_listening_podcasts()
    assert cl_podcasts == [in_memory_repo.podcasts[546], in_memory_repo.podcasts[823],
                           in_memory_repo.podcasts[908], in_memory_repo.podcasts[675]]


def test_can_retrieve_top_authors(in_memory_repo):
    top_authors = in_memory_repo.get_top_authors()
    assert top_authors == [list(in_memory_repo.authors.values())[22],
                           list(in_memory_repo.authors.values())[45],
                           list(in_memory_repo.authors.values())[52]]


def test_can_retrieve_list_of_top_podcasts(in_memory_repo):
    top_podcasts = in_memory_repo.get_top_podcasts_list()
    assert top_podcasts == in_memory_repo.podcasts[162:174]


def test_can_retrieve_list_of_recently_played_podcasts(in_memory_repo):
    recent_podcasts = in_memory_repo.get_recently_played_list()
    assert recent_podcasts == in_memory_repo.podcasts[44:56]


def test_can_retrieve_list_of_new_podcasts(in_memory_repo):
    new_podcasts = in_memory_repo.get_new_podcasts_list()
    assert new_podcasts == in_memory_repo.podcasts[280:292]
