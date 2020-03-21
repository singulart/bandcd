# bandcd
Bandcamp.com automation tools written in Python and Selenium

Main features:

1. release_meta.py - Scraps and persists releases meta-information  
2. freeband.py - Detects 'Name your Price' (free) Bandcamp albums
3. bandown.py - Downloads free albums. Requires Selenium driver

### Usage
>       python release_meta.py --tag jazz
>       python freeband.py
>       python bandown.py

### Other files/scripts

1. tracklist.py - generates album track list
2. config.py - command line config options listed here
2. album.py - data model for Bandcamp album
