#!/usr/bin/env python3
# coding: utf-8


'''
cliTube plays Internet-Music from CLI on Windows with preinstalled VLC
It builds Tube-URLS from artist & title arguments
'''


__version__ = '0.2' # minor readme changes and improvments, removed the secrets.py approach
__author__ = 'oryon/dominik'
__date__ = 'November 28, 2018'
__updated__ = 'December 31, 2020'


import json
import numpy as np
import subprocess
import os

from argparse import ArgumentParser, RawTextHelpFormatter
from pathlib import Path

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'


def get_key():
    return os.environ['GOOGLE_DEVELOPER_KEY']


def stringify(args):
    return ' '.join(args.search)


def get_search_results_from_youtube(search):
    """ returns actual data of results from SearchString """

    youtube = build(
        YOUTUBE_API_SERVICE_NAME,
        YOUTUBE_API_VERSION,
        developerKey=DEVELOPER_KEY
    )

    search_response = youtube.search().list(
        q=search,
        part='id,snippet',
        maxResults=10
    ).execute()

    return search_response


def choose(results):
    """ chooses the video randomly """
    probabilities = [.3, .25, .2, .1, .05, .025, .025, .025, .0125, .0125]

    try:
        assert 'items' in results, 'No items found in search result'

        matches = [
            match for match in results['items']
            if 'id' in match and 'snippet' in match and 'videoId' in match['id'] and 'title' in match['snippet']
        ]
        hits = {}
        for match in matches:
            ident = match['id']['videoId']
            title = match['snippet']['title']
            hits.update({
                f'{ident}': title
            })

        # print(json.dumps(hits, indent=4))  # these are the Videos concerned
        videos = [f'https://www.youtube.com/watch?v={hit}' for hit in hits]
        assert videos, "No results for searchTerm"

        if len(videos) >= 10:
            choice = np.random.choice(videos, p=probabilities)
        else:
            choice = np.random.choice(videos)
    except AssertionError as e:
        print(e)
        choice = ''

    return choice


def play(url):
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.wShowWindow = 4  # this sends the window into the background on windows
    subprocess.run(["vlc", f"{url}"], startupinfo=startupinfo)


# handling the arguments
parser = ArgumentParser(
    description=__doc__, prog='cliTube',
    epilog='Have fun tubing!',
    formatter_class=RawTextHelpFormatter,
    )

parser.add_argument('--version', action='version', version=__version__)
parser.add_argument('search', metavar='Searchterm', help='the searchstring (Artist & Title) you are looking for', nargs='*')


if __name__ == '__main__':
    args = parser.parse_args()

    DEVELOPER_KEY = get_key()

    if not DEVELOPER_KEY:
        raise SystemExit('Did not find environment variable DEVELOPER_KEY')

    if not args.search:
        parser.print_help()

    else:
        search = stringify(args)
        results = get_search_results_from_youtube(search)
        match = choose(results)
        if match:
            play(match)
