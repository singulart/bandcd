import getopt
import json
import sys
import time
from collections import OrderedDict

import lxml.html
import requests
from lxml.cssselect import CSSSelector
from selenium import webdriver
from termcolor import colored

from album import Album

# Json Page Model
pagedata = CSSSelector('#pagedata')

# "name your price" text. This is an indicator of a free album
name_your_price = CSSSelector('span.buyItemExtra')
# Duration of all tracks
tracks_play_time = CSSSelector('div.title > span.time')
# Url of the release cover art
cover_art = CSSSelector('a.popupImage')
# Release year. Newer albums get more attention from seedboxes
get_year = CSSSelector('meta[itemprop = "datePublished"]')
# Next navigation page
has_next = CSSSelector('a.next')

driver = webdriver.Firefox()


def search_list_of_dicts(leezt, attr, value):
	"""
	Loops through a list of dictionaries and returns matching attribute value pair
	You can also pass it slug, silvermoon or type, pve
	returns a list containing all matching dictionaries
	"""
	matches = [record for record in leezt if attr in record and record[attr] == value]
	return matches


def main(argv):
	print(colored('FreeBand.py v0.6.0 (c) singulart@protonmail.com', 'yellow'))
	print(colored('Simple tool reporting which Bandcamp free albums are missing on What.CD', 'yellow'))

	bandcamptag = ''
	whatcdusername = ''
	try:
		opts, args = getopt.getopt(argv, "hb:u:", ["bandcamptag=", "whatcduser="])
	except getopt.GetoptError:
		usage()
	for opt, arg in opts:
		if opt == '-h':
			print('freeband.py -b <bandcamp tag> -u <whatcdusername>')
			sys.exit()
		elif opt in ("-b", "--bandcamptag"):
			bandcamptag = arg
		elif opt in ("-u", "--whatcduser"):
			whatcdusername = arg

	if bandcamptag == '' or whatcdusername == '':
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
		
		new_releases_tab = search_list_of_dicts(data_blob['hub']['tabs'][0]['collections'], 'name', 'new_releases')[0]['items']

		# get the text out of all the results
		url_data = [nr['tralbum_url'] for nr in new_releases_tab]
		alb_data = [nr['title'] for nr in new_releases_tab]
		artist_data = [nr['artist'] for nr in new_releases_tab]
		page_data = zip(alb_data, url_data, artist_data)

		really_free_page_data = []

		# For every album go to its page and
		# 1) check if this album actually free
		# 2) if it's free, calculate its total duration, size, release year etc
		for album, url, artist in page_data:
			# Sanitize the CSS selector
			v1 = album.replace("/(:|\.|\[|\]|,)/g", "\\$1").replace("\"", "\\\"")
			# Select a link to details page
			try:
				details = requests.get(url)
				details_tree = lxml.html.fromstring(details.text)
				buyMe = name_your_price(details_tree)[0].text
				if 'name your price' in buyMe:
					print(colored("Album %s -> %s is FREE!" % (album, url), 'green'))
					# TODO sanitise album names for better What.CD search accuracy (remove EP, LP, Free Download) and stuff like that
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
					# Trying to retrieve the album cover art url
					cover = cover_art(details_tree)[0].get('href')
					# Creating an Album class instance
					album = Album(artist, album, year, url, '0MB', cover)
					# Collecting tracks duration
					play_time = tracks_play_time(details_tree)
					for t in play_time:
						album.add_track(t.text)
					really_free_page_data.append(album)
			except IndexError:
				print(colored('Problem getting url for album %s' % album, 'red'))

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
	len_before = len(free_stuff)

	# Filter out small albums
	free_stuff = list(filter(lambda alb: alb.big(), free_stuff))
	len_after = len(free_stuff)

	if len_after == 0:
		exit(0)
	else:
		print(colored('Filtered out %d small albums' % (len_before - len_after), 'green'))


def get_size(url):
	try:
		driver.get(url)
		buy_now = driver.find_element_by_css_selector('h4 > button.download-link')
		buy_now.click()

		price_field = driver.find_element_by_css_selector("input[id='userPrice']")
		price_field.send_keys('0')

		# TODO FIX THIS SELECTOR
		dwnld_link = driver.find_element_by_css_selector("TralbumDownload.showButtonsSection(event); return false")
		dwnld_link.click()

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


def usage():
	print('freeband.py -b <bandcamp tag> -u <whatcdusername>')
	sys.exit(2)


if __name__ == "__main__":
	main(sys.argv[1:])
