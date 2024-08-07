import os
import csv
from podcast.domainmodel.model import Podcast, Episode, Author, Category


class CSVDataReader:
    def __init__(self):
        self._podcasts, self._episodes = [], []
        self._authors, self._categories = dict(), dict()

        self.create_podcasts()

    def read_csv(self, episodes_file: str):
        with open(episodes_file, mode='r') as file_in:
            csv_data = csv.reader(file_in, delimiter=',')
            headers = next(csv_data)  # read the headers

            for row in csv_data:
                # Strip any leading/trailing white space.
                row = [item.strip() for item in row]
                yield row

    def create_podcasts(self):
        a_id = 1
        for row in self.read_csv("../data/podcasts.csv"):
            # pc = podcast - using these variables as keyword arguments for better readability
            pc_id, pc_title = int(row[0]), row[1]
            pc_image, pc_description = row[2], row[3]
            pc_language = row[4]
            pc_categories, pc_website = row[5], row[6]
            pc_author, pc_itunes_id = row[7], int(row[8])

            # Create Author Object if it doesn't already exist
            if pc_author not in self._authors:
                author = Author(
                    author_id=a_id,
                    name=pc_author if len(pc_author) > 0 else "Author Not Provided"
                )
                a_id += 1
                self._authors[pc_author] = author

            # Create Podcast Object
            new_podcast = Podcast(
                podcast_id=pc_id, title=pc_title,
                image=pc_image, description=pc_description,
                language=pc_language,
                website=pc_website, author=self._authors[pc_author],
                itunes_id=pc_itunes_id
            )

            # Add podcast to authors podcast list
            self._authors[pc_author].add_podcast(new_podcast)

            # Create Categories
            c_id = 1
            for c in pc_categories.split(' | '):
                category: Category = None
                if c in self._categories:
                    category = self._categories[c]
                else:
                    category = Category(
                        category_id=c_id,
                        name=c
                    )
                    c_id += 1
                    self._categories[c] = category

                # Add Category to Podcast
                new_podcast.add_category(category)

            self._podcasts.append(new_podcast)

        for at in self._authors:
            print(repr(at))


a = CSVDataReader()
