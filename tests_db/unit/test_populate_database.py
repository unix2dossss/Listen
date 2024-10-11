from sqlalchemy import select, inspect

from podcast.adapters.orm import mapper_registry


def test_database_populate_inspect_table_names(database_engine):
    # Get table information
    inspector = inspect(database_engine)
    assert inspector.get_table_names() == ['authors', 'categories', 'episodes', 'podcast_categories', 'podcasts', 'reviews', 'users']
