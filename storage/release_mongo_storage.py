import os
from pymongo import MongoClient
from pymongo.operations import UpdateOne
from bson.objectid import ObjectId

from storage.release_storage import PagedData
from storage.release_storage import IReleaseStore
from album import Album


class MongoReleaseStorage(IReleaseStore):

    STARTING_CURSOR = '000000000000000000000000'  # used in the first pageable query

    def __init__(self):
        self.mongo = MongoClient(os.environ['MONGO_URL'])['bandcamp']  # 'bandcamp' is a name of the database

    def save(self, album):
        self.mongo.releases_initial.insert_one(self.album_to_dict(album))

    def save_all(self, albums):
        """Upserts a number of albums"""

        serialized = [self.album_to_dict(a) for a in albums]
        updates = [
            UpdateOne({'tralbum_id': d['tralbum_id']}, {'$set': d}, upsert=True) for d in serialized
        ]
        self.mongo.releases_initial.bulk_write(updates)

    def load(self, title):
        self.mongo.releases_initial.find_one({'title': title})

    def load_all(self, cursor, limit):
        if cursor == '':
            cursor = self.STARTING_CURSOR
        releases_initial = self.mongo.releases_initial
        return self.cursor_to_page(releases_initial.find({'_id': {"$gt": ObjectId(cursor)}}).limit(limit))

    def cursor_to_page(self, cursor):
        dicts = [fr for fr in cursor]  # this extra step allows to get '_id' to be used as cursor
        albums = [self.dict_to_album(fr) for fr in dicts]  # convert Mongo objects to Albums
        return PagedData(albums, str(dicts[len(dicts) - 1]['_id']))  # create Page object

    @staticmethod
    def album_to_dict(album):
        return album.__dict__

    @staticmethod
    def dict_to_album(mongo_dict={}):
        a = Album('', '', '')
        a.__dict__ = mongo_dict
        return a