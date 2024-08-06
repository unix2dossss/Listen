import os
import csv
from podcast.domainmodel.model import Podcast, Episode, Author, Category


class CSVDataReader:
    def __init__(self):
        self._podcasts, self._episodes = [], []
        self._authors, self._categories = set(), set()

        self.create_podcasts()

        # self.read_csv('episodes.csv')
        # self.read_csv('episodes.csv')

    def read_csv(self, episodes_file: str):
        with open(episodes_file, encoding='utf-8-sig') as file_in:
            csv_data = csv.reader(file_in, delimiter=',')
            headers = next(csv_data)  # read the headers

            for row in csv_data:
                # Strip any leading/trailing white space.
                row = [item.strip() for item in row]
                yield row





a = CSVDataReader()