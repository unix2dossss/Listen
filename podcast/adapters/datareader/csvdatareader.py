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

    def create_podcasts(self):
        for row in self.read_csv("../data/podcasts.csv"):
            # pc = podcast - using these variables as keyword arguments for better readability
            pc_id, pc_title = int(row[0]), row[1]
            pc_image, pc_description = row[2], row[3]
            pc_language = row[4]
            pc_categories, pc_website = row[5], row[6]
            pc_author, pc_itunes_id = row[7], int(row[8])

            new_podcast = Podcast(
                podcast_id=pc_id, title=pc_title,
                image=pc_image, description=pc_description,
                language=pc_language,
                website=pc_website, author=pc_author,
                itunes_id= pc_itunes_id
            )


a = CSVDataReader()