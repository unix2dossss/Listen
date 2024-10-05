"""Initialize Flask app."""

from pathlib import Path
from flask import Flask

from podcast.adapters.orm import mapper_registry, map_model_to_tables
from podcast.domainmodel.model import Podcast, Author
import podcast.adapters.repository as repo
from podcast.adapters.memory_repository import MemoryRepository
from podcast.adapters import memory_repository, database_repository, repository_populate

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers
from sqlalchemy.pool import NullPool


def create_app(testing_config=None):
    """Construct the core application."""

    # Create the Flask app object.
    app = Flask(__name__)

    # set configuration
    app.config.from_object("config.Config")
    data_path = Path("podcast") / "adapters" / "data"

    if testing_config is not None:
        # set testing config
        app.config.from_mapping(testing_config)
        data_path = app.config["TEST_DATA_PATH"]

    # # Create the MemoryRepository implementation for a memory-based repository.
    # repo.repo_instance = MemoryRepository()
    #
    # # fill the content with the repository from the provided csv files
    # populate(data_path, repo.repo_instance)

    # We can easily switch between in memory data and
    # persistent database data storage for our application.

    if app.config['REPOSITORY'] == 'memory':

        # Create the MemoryRepository implementation for a memory-based repository.
        repo.repo_instance = memory_repository.MemoryRepository()

        # fill the content of the repository from the provided csv files (has to be done every time we start app!)
        database_mode = False
        repository_populate.populate(data_path, repo.repo_instance, database_mode)

    elif app.config['REPOSITORY'] == 'database':
        # Configure database.
        database_uri = app.config['SQLALCHEMY_DATABASE_URI']

        # We create a comparatively simple SQLite database, which is based on a single file (see .env for URI).
        # Note that create_engine does not establish any actual DB connection directly!
        database_echo = app.config['SQLALCHEMY_ECHO']

        # Please do not change the settings for connect_args and poolclass!
        database_engine = create_engine(database_uri, connect_args={"check_same_thread": False}, poolclass=NullPool,
                                        echo=database_echo)

        # Create the database session factory using sessionmaker (this has to be done once, in a global manner)
        session_factory = sessionmaker(autocommit=False, autoflush=True, bind=database_engine)
        # Create the SQLAlchemy DatabaseRepository instance for an sqlite3-based repository.
        repo.repo_instance = database_repository.SqlAlchemyRepository(session_factory)

        if app.config['TESTING'] == 'True' or len(database_engine.table_names()) == 0:
            print("REPOPULATING DATABASE...")

            # For testing, or first-time use of the web application, reinitialise the database.
            clear_mappers()

            mapper_registry.metadata.create_all(database_engine)  # Conditionally create database tables.
            for table in reversed(mapper_registry.metadata.sorted_tables):  # Remove any data from the tables.
                database_engine.execute(table.delete())

            # Generate mappings that map domain model classes to the database tables.
            map_model_to_tables()

            database_mode = True
            repository_populate.populate(data_path, repo.repo_instance, database_mode)
            print("REPOPULATING DATABASE... FINISHED")

        else:
            # Solely generate mappings that map domain model classes to the database tables.
            map_model_to_tables()



    # Build the application - these steps require an application context.

    with app.app_context():
        from .utilities import utilities

        app.register_blueprint(utilities.utilities_blueprint)

        from .podcastbp import podcastbp

        app.register_blueprint(podcastbp.podcast_blueprint)

        from .home import home

        app.register_blueprint(home.home_blueprint)

        from .discover import discover

        app.register_blueprint(discover.discover_blueprint)

        from .category import category

        app.register_blueprint(category.category_blueprint)

        from .author import author

        app.register_blueprint(author.author_blueprint)

        from .authentication import authentication

        app.register_blueprint(authentication.auth_blueprint)

        from .review import review

        app.register_blueprint(review.review_blueprint)

        from .playlist import playlist

        app.register_blueprint(playlist.playlist_blueprint)

    return app
