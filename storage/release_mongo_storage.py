from storage.release_storage import IReleaseStore
from pymongo import MongoClient
import os


class MongoReleaseStorage(IReleaseStore):

    def __init__(self):
        self.mongo = MongoClient(os.environ['MONGO_URL'])['bandcamp']  # 'bandcamp' is a name of the database

    def save(self, album):
        self.mongo.releases_initial.insert_one(self.album_to_dict(album))

    def save_all(self, albums):
        serialized = [self.album_to_dict(a) for a in albums]
        self.mongo.releases_initial.insert_many(serialized)

    def load(self, title):
        self.mongo.releases_initial.find_one({'title': title})

    def load_all(self):
        releases_initial = self.mongo.releases_initial
        releases_initial.find({})

    def album_to_dict(self, album):
        return album.__dict__
