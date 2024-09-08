import csv
import os
from datetime import datetime
from pathlib import Path

from podcast.domainmodel.model import Podcast, Episode, Author, Category, AudioTime


class CSVDataReader:
    def __init__(
        self,
        relative_podcastcsv_path: Path = None,
        relative_episodecsv_path: Path = None,
        testing: bool = False,
    ):
        if testing is True:
            relative_podcastcsv_path = "./podcast/adapters/data/podcasts.csv"
            relative_episodecsv_path = "./podcast/adapters/data/episodes.csv"

        self._podcasts, self._episodes = [], []
        self._authors, self._categories = dict(), dict()
        self._podcasts_by_category = {}

        self.create_podcasts(str(relative_podcastcsv_path))
        self.create_episodes(str(relative_episodecsv_path))

    @staticmethod
    def read_csv(input_file: str):
        with open(input_file, mode="r") as file_in:
            csv_data = csv.reader(file_in, delimiter=",")
            next(csv_data)  # read the headers

            for row in csv_data:
                # Strip any leading/trailing white space.
                row = [item.strip() for item in row]
                yield row

    def create_podcasts(self, podcast_file):
        a_id = 1
        c_id = 1
        try:
            for row in self.read_csv(podcast_file):
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
                        name=pc_author if len(pc_author) > 0 else "Author Not Provided",
                    )
                    a_id += 1
                    self._authors[pc_author] = author

                # Create Podcast Object
                new_podcast = Podcast(
                    podcast_id=pc_id,
                    title=pc_title,
                    image=pc_image,
                    description=pc_description,
                    language=pc_language,
                    website=pc_website,
                    author=self._authors[pc_author],
                    itunes_id=pc_itunes_id,
                )

                for c in pc_categories.split(" | "):
                    category: Category
                    if c in self._categories:
                        category = self._categories[c]
                    else:
                        category = Category(category_id=c_id, name=c)
                        c_id += 1
                        self._categories[c] = category

                    if c in self._podcasts_by_category:
                        self._podcasts_by_category[c].append(new_podcast)
                    else:
                        self._podcasts_by_category[c] = [new_podcast]

                    # Add Category to Podcast
                    new_podcast.add_category(category)

                # Add podcast to authors podcast list
                self._authors[pc_author].add_podcast(new_podcast)
                self._podcasts.append(new_podcast)
        except ValueError as e:
            print(f"Skipping row (invalid data): {e}")

    def create_episodes(self, episode_file: str):
        try:
            for row in self.read_csv(episode_file):
                # ep = episode
                ep_id, pc_id = int(row[0]), int(row[1])
                ep_title, ep_audio_link = row[2], row[3]
                ep_audio_length = row[4]
                ep_description, ep_pub_date = row[5], row[6]

                ep_pub_date = ep_pub_date.replace("+00", "+0000")
                ep_pub_date_object = datetime.strptime(
                    ep_pub_date, "%Y-%m-%d %H:%M:%S%z"
                )

                hours = int(ep_audio_length) // 3600
                minutes = (int(ep_audio_length) % 3600) // 60
                seconds = int(ep_audio_length) % 60
                ep_audio_length_object = AudioTime(hours, minutes, seconds)

                episode_pcast = self._podcasts[pc_id - 1]

                # Create Episode Object
                new_episode = Episode(
                    episode_id=ep_id,
                    episode_podcast=episode_pcast,
                    episode_title=ep_title,
                    episode_audio_link=ep_audio_link,
                    episode_audio_length=ep_audio_length_object,
                    episode_description=ep_description,
                    episode_publish_date=ep_pub_date_object,
                )

                self._episodes.append(new_episode)
                episode_pcast.add_episode(new_episode)

        except Exception as e:
            print(f"Skipping row (invalid data): {e}")

    @property
    def podcasts(self):
        return self._podcasts

    @property
    def episodes(self):
        return self._episodes

    @property
    def authors(self):
        return self._authors

    @property
    def categories(self):
        return self._categories

    @property
    def podcasts_by_category(self):
        return self._podcasts_by_category


# a = CSVDataReader()
