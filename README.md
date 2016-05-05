# bandcd
What.CD automation tools

Main features:

1. Tells you which Bandcamp free albums are missing on What.CD
2. Downloads Bandcamp FLAC albums
3. TODO fully automated torrent generation

Written in Python and Selenium


# Files

1. freeband.py - main analysing tool
2. bandown.py - selenium-based album downloader
3. tracklist.py - generates album track list
4. album.py - data model for Bandcamp album

# External dependencies

1. Selenium 
2. pygazelle
3. lxml
4. termcolor 
5. bitmath
6. json
7. wget
8. requests