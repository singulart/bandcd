# bandcd
What.CD automation tools

Main features:

1. Tells you which Bandcamp free albums are missing on What.CD
2. Downloads Bandcamp FLAC albums
3. TODO fully automated torrent generation

Written in Python and Selenium


### Files

1. freeband.py - main analysing tool
2. bandown.py - selenium-based album downloader
3. tracklist.py - generates album track list
4. album.py - data model for Bandcamp album

### External dependencies

1. Selenium 
2. pygazelle
3. lxml
4. termcolor 
5. bitmath
6. json
7. wget
8. requests


### Recommended dependency installation

cd into git project

>		sudo pip install virtualenv
>		source .venv/bin/activate
>		pip install -U selenium
>		pip install -U requests
>		pip install -U lxml
>		pip install -U bitmath
>		pip install -U cssselect
>		pip install -U termcolor
>		python freeband.py -b indie -u serpian
>		brew install geckodriver
>		brew update
>		brew install geckodriver

Notes on pygazelle.api

Download latest [pygazelle](https://github.com/cohena/pygazelle)

Fix torrent.py: instead of 

>         self.remastered = search_torrent_json_response['remastered']
>         self.remaster_year = search_torrent_json_response['remasterYear']
>         self.remaster_title = search_torrent_json_response['remasterTitle']
>         self.remaster_catalogue_number = search_torrent_json_response['remasterCatalogueNumber']
>         self.media = search_torrent_json_response['media']
>         self.format = search_torrent_json_response['format']
>         self.encoding = search_torrent_json_response['encoding']
>         self.has_log = search_torrent_json_response['hasLog']
>         self.has_cue = search_torrent_json_response['hasCue']
>         self.log_score = search_torrent_json_response['logScore']
>         self.scene = search_torrent_json_response['scene']
>         self.file_count = search_torrent_json_response['fileCount']
>         self.size = search_torrent_json_response['size']
>         self.seeders = search_torrent_json_response['seeders']
>         self.leechers = search_torrent_json_response['leechers']
>         self.snatched = search_torrent_json_response['snatches']
>         self.free_torrent = search_torrent_json_response['isFreeleech'] or search_torrent_json_response['isPersonalFreeleech']
>         self.time = search_torrent_json_response['time']


put this
 
>        	if('remastered' in search_torrent_json_response):
>        		self.remastered = search_torrent_json_response['remastered']
>         if('remasterYear' in search_torrent_json_response):
> 	        self.remaster_year = search_torrent_json_response['remasterYear']
>         if('remasterTitle' in search_torrent_json_response):
>     	    self.remaster_title = search_torrent_json_response['remasterTitle']
>         if('remasterCatalogueNumber' in search_torrent_json_response):
>         	self.remaster_catalogue_number = search_torrent_json_response['remasterCatalogueNumber']
>         if('media' in search_torrent_json_response):
> 	        self.media = search_torrent_json_response['media']
>         if('format' in search_torrent_json_response):
>     	    self.format = search_torrent_json_response['format']
>         if('encoding' in search_torrent_json_response):
>         	self.encoding = search_torrent_json_response['encoding']
>         if('hasLog' in search_torrent_json_response):
>         	self.has_log = search_torrent_json_response['hasLog']
>         if('hasCue' in search_torrent_json_response):
> 	        self.has_cue = search_torrent_json_response['hasCue']
>         if('logScore' in search_torrent_json_response):
>     	    self.log_score = search_torrent_json_response['logScore']
>         if('scene' in search_torrent_json_response):
>         	self.scene = search_torrent_json_response['scene']
>         if('fileCount' in search_torrent_json_response):
>         	self.file_count = search_torrent_json_response['fileCount']
>         if('size' in search_torrent_json_response):
>         	self.size = search_torrent_json_response['size']
>         if('seeders' in search_torrent_json_response):
>         	self.seeders = search_torrent_json_response['seeders']
>         if('leechers' in search_torrent_json_response):
>         	self.leechers = search_torrent_json_response['leechers']
>         if('snatches' in search_torrent_json_response):
>         	self.snatched = search_torrent_json_response['snatches']
>         if('isFreeleech' in search_torrent_json_response and 'isPersonalFreeleech' in search_torrent_json_response):
>         	self.free_torrent = search_torrent_json_response['isFreeleech'] or search_torrent_json_response['isPersonalFreeleech']
>         if('time' in search_torrent_json_response):
>         	self.time = search_torrent_json_response['time']

Build pygazelle: 

>		 python setup.py install --home=/tmp

Return to your project dir and copy /tmp/lib/pygazelle* into .venv/lib/python<your version of python>


