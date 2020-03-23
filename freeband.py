import json
import sys
import time

import lxml.html
import requests
from lxml.cssselect import CSSSelector
from termcolor import colored

from bandown import navigate_to_download_screen
from config import get_arguments
from storage.release_mongo_storage import MongoReleaseStorage

pagedata = CSSSelector('#pagedata')  # Json Page Model
name_your_price = CSSSelector('span.buyItemExtra')  # "name your price" text. This is an indicator of a free album
tracks_play_time = CSSSelector('div.title > span.time')  # Duration of all tracks
cover_art = CSSSelector('a.popupImage')  # Urls of the release cover art
get_year = CSSSelector('meta[itemprop = "datePublished"]')  # Release year
tracks_title = CSSSelector('.track-title')  # Track titles
album_about = CSSSelector('div.tralbum-about')  # Album description
album_tags = CSSSelector('a.tag')  # Album tags


def main(argv):
    print(colored('Bandcamp automation tools v2.2.0 (c) singulart@protonmail.com', 'yellow'))

    parser = get_arguments()
    opt = parser.parse_args()
    
    storage = MongoReleaseStorage()

    cursor = ''   # Cursor-based pagination
    proceed = True
    num_free = 0  # Counter of free releases

    while proceed:

        album_page = storage.load_all(cursor, 50)  # Load from persistent storage in batches

        if len(album_page.page) == 0:
            proceed = False
            continue
        else:
            cursor = album_page.cursor

        # For every album go to its page and
        # 1) check if this release can be downloaded for free
        # 2) fetch additional metadata: total duration, size, release year, tags, about etc
        for album in album_page.page:
            try:
                details = requests.get(album.tralbum_url)
                details_tree = lxml.html.fromstring(details.text)

                try:
                    album.about = album_about(details_tree)[0].text
                except IndexError:
                    pass

                buy_me = name_your_price(details_tree)[0].text
                if 'name your price' in buy_me:
                    print(colored("Album %s -> %s is FREE!" % (album.title, album.tralbum_url), 'green'))
                    album.is_free = True
                    num_free += 1
                else:
                    album.is_free = False

                year_element = get_year(details_tree)
                year = 1970
                try:
                    if year_element is not None:
                        year_s = year_element[0].attrib['content']
                        year = time.strptime(year_s, '%Y%m%d').tm_year
                    else:
                        print(colored('       no release year found', 'yellow'))
                except KeyError:
                    print(colored('       error getting release year', 'red'))
                album.year = year

                if album.size == '0MB' or album.size == 'unknown':
                    size = get_size(album.tralbum_url, opt).replace('size: ', '', 1)  # see docstring
                    album.size = size

                cover = cover_art(details_tree)[0].get('href')  # Trying to retrieve the album cover art url
                album.cover_art = cover

                if not album.tracklist:
                    play_time = tracks_play_time(details_tree)  # Collecting tracks duration
                    track_titles = tracks_title(details_tree)  # Collecting tracks titles
                    for (title, play) in zip(track_titles, play_time):
                        album.add_track(title.text, play.text)

                if not album.tags:
                    album.tags = [a.text for a in album_tags(details_tree)]

            except IndexError:
                print(colored('Problem processing album %s' % album.title, 'red'))

        storage.save_all(album_page.page)

        all_tags = []
        for a in album_page.page:
            all_tags += a.tags
        storage.save_tags(set(all_tags))
        print(colored('Discovered %d albums so far' % num_free, 'green'))
    else:
        print(colored('Found %d free albums' % num_free, 'green'))


def get_size(url, opt):
    """
    Retrieves the information about the download size. Back then, when the tool was used in conjunction with What.cd,
    this data was very useful (larger uploads yield better ratio), but at the moment it's almost useless IMO.
    Anyways, I decided to leave it, because this flow is kinda cool
    """
    
    if not opt.scrap_download_size:
        return 'size: unknown'

    audio_format = opt.download_type
    try:
        driver = navigate_to_download_screen(url, initiate_download=False)
        dom = lxml.html.fromstring(driver.page_source)  # build the DOM tree
        page_model = pagedata(dom)
        data_blob = json.loads(page_model[0].xpath('@data-blob')[0])
        downloads = data_blob['download_items'][0]['downloads']
        if audio_format in downloads.keys():
            return downloads[audio_format]['size_mb']
        else:
            print('Audio format %s is not available. This release can be downloaded as %s' %
                  (audio_format, ",".join(downloads.keys())))
            return 'size: unknown'
    except:
        # Some albums allow you to navigate to download page only after you provide an email address
        # Size of such albums cannot be retrieved
        return 'size: unknown'


if __name__ == "__main__":
    main(sys.argv[1:])
