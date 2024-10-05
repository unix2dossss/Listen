from podcast.adapters.datareader.csvdatareader import CSVDataReader
from pathlib import Path
from podcast.adapters.repository import AbstractRepository


def populate(data_path: Path, repo: AbstractRepository, database_mode: bool):
    # create instance of csvreader
    podcasts_csv_path = data_path / "podcasts.csv"
    episodes_csv_path = data_path / "episodes.csv"

    csvdatareader_instance = CSVDataReader(podcasts_csv_path, episodes_csv_path)

    if not database_mode:
        repo.podcasts = csvdatareader_instance.podcasts
        repo.episodes = csvdatareader_instance.episodes
        repo.authors = csvdatareader_instance.authors
        repo.categories = csvdatareader_instance.categories
        repo.podcasts_by_category = csvdatareader_instance.podcasts_by_category

    else:
        authors = csvdatareader_instance.authors
        podcasts = csvdatareader_instance.podcasts
        categories = csvdatareader_instance.categories
        episodes = csvdatareader_instance.episodes

        # Add authors to the repo
        repo.add_multiple_authors(authors)

        # Add categories to the repo
        repo.add_multiple_categories(categories)

        # # Add podcasts to the repo
        repo.add_multiple_podcasts(podcasts)

        # Add episodes to the repo
        repo.add_multiple_episodes(episodes)
