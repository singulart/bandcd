import sys, getopt
import time
import getpass
import requests
import time
import lxml.html
from selenium import webdriver
from album import Album
from lxml.cssselect import CSSSelector
from collections import OrderedDict
from pygazelle.api import GazelleAPI
from termcolor import colored

try:
	from html import escape  # python 3.x
except ImportError:
	from cgi import escape  # python 2.x

# Release titles
alb_css = CSSSelector('.itemtext')
# Artist names
art_css = CSSSelector('.itemsubtext')
# "name your price" text. This is an indicator of a free album
name_your_price = CSSSelector('span.buyItemExtra')
# Duration of all tracks
tracks_play_time = CSSSelector('div.title > span.time')
# Release year. Newer albums get more attention from seedboxes
get_year = CSSSelector('meta[itemprop = "datePublished"]')
# Next navigation page
has_next = CSSSelector('a.next')

driver = webdriver.Firefox()


def main(argv):
	print colored('FreeBand.py v0.5.0 (c) singulart@i.ua', 'yellow')
	print colored('Simple tool reporting which Bandcamp free albums are missing on What.CD', 'yellow')

	bandcamptag = ''
	whatcdusername = ''
	try:
		opts, args = getopt.getopt(argv,"hb:u:",["bandcamptag=","whatcduser="])
	except getopt.GetoptError:
		print 'freeband.py -b <bandcamp tag> -u <whatcdusername>'
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print 'freeband.py -b <bandcamp tag> -u <whatcdusername>'
			sys.exit()
		elif opt in ("-b", "--bandcamptag"):
			bandcamptag = arg
		elif opt in ("-u", "--whatcduser"):
			whatcdusername = arg

	if bandcamptag == '':
		print 'freeband.py -b <bandcamp tag> -u <whatcdusername>'
		sys.exit(2)

	if whatcdusername == '':
		print 'freeband.py -b <bandcamp tag> -u <whatcdusername>'
		sys.exit(2)

	page = 1
	proceed = True
	free_stuff = []

	print colored('Looking for free albums on BandCamp using tag %s...' % bandcamptag, 'green')

	while proceed:
		r = requests.get('https://bandcamp.com/tag/%s?page=%dsort_asc=0&sort_field=date' % (bandcamptag, page))

		# build the DOM Tree
		tree = lxml.html.fromstring(r.text)

		# Apply selectors to the DOM tree.
		art_results = art_css(tree)
		alb_results = alb_css(tree)

		if len(art_results) != len(alb_results):
			print colored('Albums don\'t match artists', 'red')
			exit(1)

		# get the text out of all the results
		art_data = [result.text for result in art_results]
		alb_data = [result.text for result in alb_results]
		page_data = OrderedDict(zip(alb_data, art_data))
		print colored('Page %d has %d albums to analyse' % (page, len(page_data)), 'blue')

		really_free_page_data = []

		# For every album go to its page and
		# 1) check if this album actually free
		# 2) if it's free, calculate its total duration
		for album, artist in page_data.iteritems():
			# Sanitize the CSS selector
			v1 = album.replace("/(:|\.|\[|\]|,)/g", "\\$1").replace("\"", "\\\"")
			# Select a link to details page
			get_details_url = CSSSelector('a[title="%s"]' % v1)
			try:
				details_url = get_details_url(tree)[0].get('href')
				print colored("checking album %s -> %s" % (album, details_url), 'green')
				details = requests.get(details_url)
				details_tree = lxml.html.fromstring(details.text)
				buyMe = name_your_price(details_tree)[0].text
				if not 'name your price' in buyMe:
					print colored('         album %s isn\'t free' % album, 'yellow')
				else:
					# TODO sanitise album names for better What.CD search accuracy (remove EP, LP, Free Download) and stuff like that
					year_element = get_year(details_tree)
					year = 1970
					try:
						if year_element is not None:
							year_s = year_element[0].attrib['content']
							year = time.strptime(year_s, '%Y%m%d').tm_year
						else:
							print colored('       no release year found', 'yellow')
					except KeyError:
						print colored('       error getting release year', 'red')
					# Trying to retrieve the album size
					size = get_size(details_url).replace('size: ', '', 1)
					print size
					# Create an Album class instance
					album = Album(artist, album, year, details_url, size)
					play_time = tracks_play_time(details_tree)
					for t in play_time:
						album.add_track(t.text)
					really_free_page_data.append(album)
			except IndexError:
				print colored('Problem getting url for album %s' % album, 'red')

		free_stuff.extend(really_free_page_data)

		nextel = has_next(tree)
		if nextel:
			print colored('Discovered %d albums so far' % (len(free_stuff)), 'green')
			page += 1
		else:
			proceed = False
	else:
		print colored('Found %d free albums' %len(free_stuff), 'green')

	if len(free_stuff) == 0:
		exit(0)

	# Apply sorting by album size, largest albums first
	free_stuff = sorted(free_stuff, key=lambda x: x.size_bytes(), reverse=True)
	len_before = len(free_stuff)

	# Filter out small albums
	free_stuff = filter(lambda alb: alb.big(), free_stuff)
	len_after = len(free_stuff)

	print colored('Filtered out %d small albums' % (len_before - len_after), 'green')

	# pygazelle is a Python API on top of Gazelle REST API (Gazelle is the engine What.CD runs on)
	whatcdpwd = getpass.getpass('What.CD password:')
	api = GazelleAPI(whatcdusername, whatcdpwd)
	api.request('announcements')  # just to log in
	print colored('Logged in to What.CD: %s' % (api.logged_in()), 'yellow')

	whatcd_missing = 0.0
	for a in free_stuff:
		time.sleep(2)
		try:
			albumsCallResult = api.search_torrents(groupname=a.album, artistname=a.artist)  # search by album and artist
			if not albumsCallResult['results']:
				whatcd_missing += 1
				print colored('Album %s is missing' % (a.to_str()), 'cyan')
		except KeyError:
			print colored('Error searching for album %s. Please look up manually' % (a.to_str()), 'red')
	print str(whatcd_missing / len(free_stuff) * 100) + '% discovered albums is missing'


def get_size(url):
	try:
		driver.get(url)
		buy_now = driver.find_element_by_css_selector('h4 > button.download-link')
		buy_now.click()

		price_field = driver.find_element_by_css_selector("input[id='userPrice']")
		price_field.send_keys('0')

		dnow = driver.find_element_by_css_selector("button[onclick='TralbumDownload.checkout(); return false']")
		dnow.click()

		format_drop_down = driver.find_element_by_id('downloadFormatMenu0')
		format_drop_down.click()
		flac = driver.find_element_by_css_selector("li[data-value='flac']")
		flac.click()
		return driver.find_element_by_xpath("//span[contains(text(), 'size')]").text
	except:
		# Some albums allow you to navigate to download page only after you provide an email address
		# Size of such albums cannot be retrieved
		return 'size: unknown'

if __name__ == "__main__":
	main(sys.argv[1:])