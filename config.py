import argparse


def get_arguments():
    parser = argparse.ArgumentParser()
    
    #: Configuration options
    parser.add_argument('--tag', default='post-punk', help='Bandcamp genre tag')
    parser.add_argument('--download_type', default='mp3-v0',
                        help='Audio format: flac|aac-hi|mp3-v0|alac|vorbis|aiff-lossless|wav|mp3-320')
    parser.add_argument('--scrap-download-size', type=bool, default=False,
                        help='Fetch the size of the download. Requires Selenium')

    return parser
