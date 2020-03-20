import json
import sys
import requests
import jsonpickle
from json.decoder import JSONDecodeError
from album import Album
from config import get_arguments
from storage.release_storage import IReleaseStore
from storage.release_mongo_storage import MongoReleaseStorage

def main(sysv):
    parser = get_arguments()
    opt = parser.parse_args()
    proceed = True
    page = 1
    storage = MongoReleaseStorage()
    while proceed:
        print('Processing page %s for %s' % (page, opt.tag))
        body = jsonpickle.encode(DigDeeperPostBody(DigDeeperFilter(opt.tag), page))
        try:
            hub_page = json.loads(requests.post('https://bandcamp.com/api/hub/2/dig_deeper', body).text)
            if not hub_page['more_available']:
                proceed = False
            else:
                page += 1
            to_save_bulk = []
            for release in hub_page['items']:
                album = Album(
                    release['artist'],
                    release['title'],
                    release['tralbum_url'],
                    release['band_url'],
                    release['slug_text'],
                    release['num_comments'],
                    release['tralbum_id'],
                    release['art_id'],
                    release['genre'],
                    release['band_id'],
                    release['genre_id']
                )
                # storage.save(album)
                to_save_bulk.append(album)
                if len(to_save_bulk) == 50:
                    storage.save_all(to_save_bulk)
                    to_save_bulk = []

            if len(to_save_bulk) > 0:
                storage.save_all(to_save_bulk)
                
        except JSONDecodeError as e:
            print(e.msg)
        

class DigDeeperFilter:
    def __init__(self, tags, bc_format='all', location=0, sort='date'):
        self.format = bc_format
        self.location = location
        self.sort = sort
        self.tags = tags.split(',')


class DigDeeperPostBody:
    def __init__(self, dd_filter, page):
        self.filters = dd_filter
        self.page = page
    

if __name__ == "__main__":
    main(sys.argv[1:])
