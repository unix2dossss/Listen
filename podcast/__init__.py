"""Initialize Flask app."""
from pathlib import Path
from flask import Flask
from podcast.domainmodel.model import Podcast, Author
import podcast.adapters.repository as repo
from podcast.adapters.memory_repository import MemoryRepository, populate


def create_app():
    """Construct the core application."""

    # Create the Flask app object.
    app = Flask(__name__)

    data_path = Path('podcast') / 'adapters' / 'data'

    # Create the MemoryRepository implementation for a memory-based repository.
    repo.repo_instance = MemoryRepository()

    # fill the content with the repository from the provided csv files
    populate(data_path, repo.repo_instance)

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

    return app
