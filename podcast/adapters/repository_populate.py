from podcast.adapters.datareader.csvdatareader import CSVDataReader
from pathlib import Path
from podcast.adapters.repository import AbstractRepository


def populate(data_path: Path, repo: AbstractRepository, database_mode: bool):
    # create instance of csvreader
    podcasts_csv_path = data_path / "podcasts.csv"
    episodes_csv_path = data_path / "episodes.csv"

    csvdatareader_instance = CSVDataReader(podcasts_csv_path, episodes_csv_path)

    repo.podcasts = csvdatareader_instance.podcasts
    repo.episodes = csvdatareader_instance.episodes
    repo.authors = csvdatareader_instance.authors
    repo.categories = csvdatareader_instance.categories
    repo.podcasts_by_category = csvdatareader_instance.podcasts_by_category