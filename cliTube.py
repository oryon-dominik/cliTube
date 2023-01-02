#!/usr/bin/env python3
# coding: utf-8

import subprocess
import os

from argparse import ArgumentParser, RawTextHelpFormatter
from pathlib import Path


__version__ = '0.6'  # python update to >=3.11
__author__ = 'oryon/dominik'
__date__ = 'November 28, 2018'
__updated__ = 'January 02, 2023'


REQUIREMENTS = "google-api-python-client numpy httpx python-dotenv"

__doc__ = f'''
cliTube plays Internet-Music from CLI on Windows with preinstalled VLC
It builds Tube-URLS from artist & title arguments

requires a GOOGLE_YOUTUBE_API_KEY set as dotenv or environment variable
if it doesn't play, try to update the youtube.lua from github (run clitube with
the --update flag and permissions)

required modules:
    python -m pip install {REQUIREMENTS}

to build as exe:
    python -m pip install pyinstaller
    pyinstaller.exe --onefile cliTube.py --distpath . --clean
    # have to clean up the mess manually..
    rm clitube.spec; rm build
'''

try:
    import httpx
    from dotenv import load_dotenv
    import numpy as np
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
except ImportError as error:
    raise SystemExit(f"Import failed. {error}. 'python -m pip install {REQUIREMENTS}'.")


CUSTOM_DOTENV_PATH: Path | str = ".env"  # custom path to your own dotenvs-location


def get_google_api_key():
    """Grab the API_KEY. Key's precedence: 1. os 2. dotfiles, 3. .env"""

    key = os.environ.get('GOOGLE_YOUTUBE_API_KEY')
    if key is not None:
        return key

    dotfiles = os.environ.get('DOTFILES')
    directory: Path = Path(__file__).parent if dotfiles is None else Path(dotfiles)
    dotenv = directory / CUSTOM_DOTENV_PATH

    if not dotenv.exists():
        print('.env not found')
        raise SystemExit('.env not found. Setup failed.')

    load_dotenv(dotenv)

    key = os.environ.get('GOOGLE_YOUTUBE_API_KEY')
    if key is None:
        raise SystemExit('Did not find GOOGLE_YOUTUBE_API_KEY in .env')
    return key


def stringify(args):
    return ' '.join(args.search)


def get_search_results_from_youtube(search, api_key, youtube_api_service_name="youtube", youtube_api_version="v3"):
    """
    returns actual data of results from SearchString

    docs on all available APIs:
    https://github.com/googleapis/google-api-python-client/blob/main/docs/dyn/index.md
    docs on the YouTube API:
    https://googleapis.github.io/google-api-python-client/docs/dyn/youtube_v3.html
    """
    try:
        youtube = build(
            youtube_api_service_name,
            youtube_api_version,
            developerKey=api_key,
        )
    except Exception as error:
        raise SystemExit(f'{error}\nYoutube API-setup failed.')

    search_request = youtube.search().list(
        q=search,
        part='id,snippet',
        maxResults=10
    )
    try:
        response = search_request.execute()
    except HttpError as error:
        raise SystemExit(f'{error}\nConnection failed.')

    # youtube.close()  # TODO: custom context-manager class
    return response


def choose(results):
    """ chooses the video randomly """
    probabilities = [.3, .25, .2, .1, .05, .025, .025, .025, .0125, .0125]

    hits = {}
    try:
        assert 'items' in results, 'No items found in search result'

        matches = [
            match for match in results['items']
            if 'id' in match and 'snippet' in match and 'videoId' in match['id'] and 'title' in match['snippet']
        ]

        for match in matches:
            ident = match['id']['videoId']
            title = match['snippet']['title']
            hits.update({
                f'{ident}': title
            })

        # these are the Videos concerned:
        # import json
        # print(json.dumps(hits, indent=4))

        videos = [f'https://www.youtube.com/watch?v={hit}' for hit in hits]
        assert videos, "No results for searchTerm"

        if len(videos) >= 10:
            choice_url = np.random.choice(videos, p=probabilities)
        else:
            choice_url = np.random.choice(videos)
    except AssertionError as e:
        print(e)
        choice_url = ""

    try:
        hit = choice_url.split('watch?v=')[-1]
    except IndexError:
        hit = ""
    name = hits.get(hit, '')
    return choice_url, name


def play(url, name):
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.wShowWindow = 4  # this sends the window into the background on windows
    try:
        subprocess.Popen(["vlc", f"{url}"], startupinfo=startupinfo)
    except FileNotFoundError:
        raise SystemExit(f"Could not find VLC on Path")
    raise SystemExit(f"Playing {name}\n{url}")


def update():
    """update vlc youtube.lua from github"""
    lua_url =  "https://raw.githubusercontent.com/videolan/vlc/master/share/lua/playlist/youtube.lua"
    vlc_path = Path("C:/Program Files/VideoLAN/VLC")
    playlist_path = vlc_path / "lua" / "playlist"
    lua_path = playlist_path / "youtube.lua"

    try:
        response = httpx.get(lua_url)
        response.raise_for_status()
    except httpx.RequestError as exc:
        raise SystemExit(f"An error occurred while requesting a new 'youtube.lua' from github.")
    except httpx.HTTPStatusError as exc:
        raise SystemExit(f"Error response {exc.response.status_code} while requesting a new 'youtube.lua' from github.")

    if not vlc_path.exists():
        raise SystemExit(f"Can't find VLC (expected to be in: {vlc_path.resolve()}).")

    playlist_path.mkdir(parents=True, exist_ok=True)
    try:
        with open(lua_path, 'wb') as lua:
            lua.write(response.content)
    except OSError as exc:
        raise SystemExit(f"An error occurred while writing to {lua_path.resolve()}: {exc}.")


# handling the arguments
parser = ArgumentParser(
    description=__doc__, prog='cliTube',
    epilog='Have fun tubing!',
    formatter_class=RawTextHelpFormatter,
    )

parser.add_argument('--version', action='version', version=__version__)
parser.add_argument('search', metavar='Searchterm', help='the searchstring (Artist & Title) you are looking for', nargs='*')
parser.add_argument('--update', action="store_true", default=False)


if __name__ == '__main__':
    args = parser.parse_args()

    if args.update:
        update()
        raise SystemExit(f"Successfully updated 'youtube.lua'.")

    if not args.search:
        parser.print_help()
        raise SystemExit(f'')

    # play
    api_key = get_google_api_key()
    search = stringify(args)
    results = get_search_results_from_youtube(search, api_key)
    url, name = choose(results)
    if url:
        play(url, name)
