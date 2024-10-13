from sqlalchemy import select, inspect

from podcast.adapters.orm import mapper_registry


def test_database_populate_inspect_table_names(database_engine):
    # Get table information
    inspector = inspect(database_engine)
    print(inspector.get_table_names())
    assert inspector.get_table_names() == ['audio_times', 'authors', 'categories', 'comments', 'episode_users',
                                           'episodes', 'playlists', 'podcast_categories', 'podcast_users', 'podcasts',
                                           'reviews', 'users']


def test_database_populate_select_all_authors(database_engine):
    # Get table information
    inspector = inspect(database_engine)
    name_of_authors_table = inspector.get_table_names()[1]

    with database_engine.connect() as connection:
        # query for records in authors table
        select_statement = select([mapper_registry.metadata.tables[name_of_authors_table]])
        result = connection.execute(select_statement)

        all_authors = []
        for row in result:
            all_authors.append(row['name'])

        assert all_authors[0] == 'D Hour Radio Network'
        assert all_authors[1] == 'Brian Denny'


def test_database_populate_select_all_categories(database_engine):
    # Get table information
    inspector = inspect(database_engine)
    name_of_categories_table = inspector.get_table_names()[2]

    with database_engine.connect() as connection:
        # query for records in categories table
        select_statement = select([mapper_registry.metadata.tables[name_of_categories_table]])
        result = connection.execute(select_statement)

        all_categories = []
        for row in result:
            all_categories.append(row['category_name'])

        assert all_categories[0] == 'Society & Culture'
        assert all_categories[1] == 'Personal Journals'
        assert all_categories[2] == 'Professional'


def test_database_populate_select_all_podcasts(database_engine):
    # Get table information
    inspector = inspect(database_engine)
    name_of_podcasts_table = inspector.get_table_names()[9]

    with database_engine.connect() as connection:
        # query for records in podcasts table
        select_statement = select([mapper_registry.metadata.tables[name_of_podcasts_table]])
        result = connection.execute(select_statement)

        all_podcasts = []
        for row in result:
            all_podcasts.append(row['title'])

        assert all_podcasts[0] == 'D-Hour Radio Network'
        assert all_podcasts[1] == 'Brian Denny Radio'


def test_database_populate_select_all_episodes(database_engine):
    # Get table information
    inspector = inspect(database_engine)
    name_of_episodes_table = inspector.get_table_names()[5]

    with database_engine.connect() as connection:
        # query for records in episodes table
        select_statement = select([mapper_registry.metadata.tables[name_of_episodes_table]])
        result = connection.execute(select_statement)

        all_episodes = []
        for row in result:
            all_episodes.append(row['episode_id'])

        assert all_episodes[0] == 70
        assert all_episodes[1] == 4885
        assert len(all_episodes) == 11
