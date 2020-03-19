import getopt
import json
import sys
import time

import lxml.html
import requests
from lxml.cssselect import CSSSelector
from termcolor import colored

from album import Album
from bandown import navigate_to_download_screen

pagedata = CSSSelector('#pagedata')  # Json Page Model
name_your_price = CSSSelector('span.buyItemExtra')  # "name your price" text. This is an indicator of a free album
tracks_play_time = CSSSelector('div.title > span.time')  # Duration of all tracks
cover_art = CSSSelector('a.popupImage')  # Url of the release cover art
get_year = CSSSelector('meta[itemprop = "datePublished"]')  # Release year
has_next = CSSSelector('a.next')  # Next navigation page


def main(argv):
    print(colored('Bandcamp automation tools v1.0.0 (c) singulart@protonmail.com', 'yellow'))

    bandcamptag = ''
    try:
        opts, args = getopt.getopt(argv, "hb:", ["bandcamptag="])
    except getopt.GetoptError:
        usage()
    for opt, arg in opts:
        if opt == '-h':
            print('freeband.py -b <bandcamp tag>')
            sys.exit()
        elif opt in ("-b", "--bandcamptag"):
            bandcamptag = arg

    if bandcamptag == '':
        usage()

    page = 1
    proceed = True
    free_stuff = []

    print(colored('Looking for free albums on BandCamp using tag %s...' % bandcamptag, 'green'))

    while proceed:
        r = requests.get('https://bandcamp.com/tag/%s?tab=all_releases&s=date' % bandcamptag)

        tree = lxml.html.fromstring(r.text)  # build the DOM tree
        page_data_div = pagedata(tree)  # apply CSS selector to find div with json page model (data-blob)
        data_blob = {}  # this is the json page model
        if not page_data_div or len(page_data_div) == 0:
            print('Json page model not found. Check the html structure and fix the CSS selector')
            exit(1)
        else:
            data_blob = json.loads(page_data_div[0].xpath('@data-blob')[0])
        
        new_releases_tab = search_list_of_dicts(data_blob['hub']['tabs'][0]['collections'],
                                                'name', 'new_releases')[0]['items']

        # get the text out of all the results
        tuples = [(nr['title'], nr['tralbum_url'], nr['artist']) for nr in new_releases_tab]

        really_free_page_data = []

        # For every album go to its page and
        # 1) check if this album actually free
        # 2) if it's free, calculate its total duration, size, release year etc
        for (album, url, artist) in tuples:
            try:
                details = requests.get(url)
                details_tree = lxml.html.fromstring(details.text)
                buyMe = name_your_price(details_tree)[0].text
                if 'name your price' in buyMe:
                    print(colored("Album %s -> %s is FREE!" % (album, url), 'green'))
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
                    # Trying to retrieve the album size
                    size = get_size(url).replace('size: ', '', 1)
                    cover = cover_art(details_tree)[0].get('href')  # Trying to retrieve the album cover art url
                    album = Album(artist, album, year, url, size, cover)  # Creating an Album class instance
                    play_time = tracks_play_time(details_tree)  # Collecting tracks duration
                    for t in play_time:
                        album.add_track(t.text)
                    really_free_page_data.append(album)
                    album.dump_json()
            except IndexError:
                print(colored('Problem processing album %s' % album, 'red'))

        free_stuff.extend(really_free_page_data)

        nextel = has_next(tree)
        if nextel:
            print(colored('Discovered %d albums so far' % (len(free_stuff)), 'green'))
            page += 1
        else:
            proceed = False
    else:
        print(colored('Found %d free albums' % len(free_stuff), 'green'))

    # Apply sorting by album size, largest albums first
    free_stuff = sorted(free_stuff, key=lambda x: x.size_bytes(), reverse=True)

    # Filter out small albums
    # free_stuff = list(filter(lambda alb: alb.big(), free_stuff))
    # len_after = len(free_stuff)

    # if len_after == 0:
    #   exit(0)
    # else:
    #   print(colored('Filtered out %d small albums' % (len_before - len_after), 'green'))


def get_size(url):
    """
    Retrieves the information about the download size. Back then, when the tool was used in conjunction with What.cd,
    this data was very useful (larger uploads yield better ratio), but at the moment it's almost useless IMO.
    Anyways, I decided to leave it, because this flow is kinda cool
    """
    try:
        driver = navigate_to_download_screen(url, initiate_download=False)
        flac = driver.find_element_by_css_selector("li[data-value='flac']")
        flac.click()
        return driver.find_element_by_xpath("//span[contains(text(), 'size')]").text
    except:
        # Some albums allow you to navigate to download page only after you provide an email address
        # Size of such albums cannot be retrieved
        return 'size: unknown'


def usage():
    print('freeband.py -b <bandcamp tag>')
    sys.exit(2)


def search_list_of_dicts(leezt, attr, value):
    """
    Loops through a list of dictionaries and returns matching attribute value pair
    You can also pass it slug, silvermoon or type, pve
    returns a list containing all matching dictionaries
    """
    matches = [record for record in leezt if attr in record and record[attr] == value]
    return matches


if __name__ == "__main__":
    main(sys.argv[1:])
