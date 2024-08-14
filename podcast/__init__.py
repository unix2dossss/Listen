"""Initialize Flask app."""
from pathlib import Path
from flask import Flask, render_template
from podcast.domainmodel.model import Podcast, Author
import podcast.adapters.repository as repo
from podcast.adapters.memory_repository import MemoryRepository, populate

# Remove later
def create_some_podcast():
    some_author = Author(1, "TED")
    some_podcast = Podcast(66, some_author, "TED Talks Daily")
    some_podcast.description = "Want TED Talks on the go? Every weekday, this feed brings you our latest talks in audio format. Hear thought-provoking ideas on every subject imaginable -- from Artificial Intelligence to Zoology, and everything in between -- given by the world's leading thinkers and doers. This collection of talks, given at TED and TEDx conferences around the globe, is also available in video format."
    some_podcast.image_url = "http://is4.mzstatic.com/image/thumb/Music128/v4/d5/c6/50/d5c65035-505e-b006-48e5-be3f0f8f19f8/source/600x600bb.jpg"
    return some_podcast


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
        # Register blueprints.
        pass

    @app.route('/')
    def home():
        some_podcast = create_some_podcast()
        # Use Jinja to customize a predefined html page rendering the layout for showing a single podcast.
        return render_template('podcastDescription.html', podcast=some_podcast)

    return app
