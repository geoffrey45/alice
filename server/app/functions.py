"""
This module contains functions for the server
"""
import os
import time
from io import BytesIO

import requests
from app import helpers
from app import settings
from app.lib import watchdoge
from app.lib.populate import Populate, CreateAlbums
from PIL import Image
from concurrent.futures import ThreadPoolExecutor

from app.lib import trackslib


@helpers.background
def reindex_tracks():
    """
    Checks for new songs every 5 minutes.
    """

    while True:
        trackslib.validate_tracks()

        Populate()
        CreateAlbums()
        CheckArtistImages()()

        time.sleep(60)


@helpers.background
def start_watchdog():
    """
    Starts the file watcher.
    """
    watchdoge.watch.run()


class getArtistImage:
    """
    Returns an artist image url.
    """

    def __init__(self, artist: str):
        self.artist = artist

    def __call__(self):
        try:
            url = f"https://api.deezer.com/search/artist?q={self.artist}"
            response = requests.get(url)
            data = response.json()

            return data["data"][0]["picture_medium"]
        except requests.exceptions.ConnectionError:
            time.sleep(5)
            return None
        except (IndexError, KeyError):
            return None


class useImageDownloader:
    def __init__(self, url: str, dest: str) -> None:
        self.url = url
        self.dest = dest

    def __call__(self) -> None:
        try:
            img = Image.open(BytesIO(requests.get(self.url).content))
            img.save(self.dest, format="webp")
            img.close()
        except requests.exceptions.ConnectionError:
            print("🔴🔴🔴🔴🔴🔴🔴")
            time.sleep(5)


class CheckArtistImages:
    def __init__(self):
        self.artists: list[str] = []
        print("Checking for artist images")

    @staticmethod
    def check_if_exists(img_path: str):
        """
        Checks if an image exists on disk.
        """

        if os.path.exists(img_path):
            return True
        else:
            return False

    @classmethod
    def download_image(cls, artistname: str):
        """
        Checks if an artist image exists and downloads it if not.

        :param artistname: The artist name
        """

        img_path = (
            helpers.app_dir
            + "/images/artists/"
            + helpers.create_safe_name(artistname)
            + ".webp"
        )

        if cls.check_if_exists(img_path):
            return

        url = getArtistImage(artistname)()

        if url is None:
            return

        useImageDownloader(url, img_path)()

    def __call__(self):
        self.artists = helpers.Get.get_all_artists()

        with ThreadPoolExecutor() as pool:
            pool.map(self.download_image, self.artists)

        print("Done fetching images")


def fetch_album_bio(title: str, albumartist: str) -> str | None:
    """
    Returns the album bio for a given album.
    """
    last_fm_url = "http://ws.audioscrobbler.com/2.0/?method=album.getinfo&api_key={}&artist={}&album={}&format=json".format(
        settings.LAST_FM_API_KEY, albumartist, title
    )

    try:
        response = requests.get(last_fm_url)
        data = response.json()
    except:
        return None

    try:
        bio = data["album"]["wiki"]["summary"].split('<a href="https://www.last.fm/')[0]
    except KeyError:
        bio = None

    return bio


class FetchAlbumBio:
    """
    Returns the album bio for a given album.
    """

    def __init__(self, title: str, albumartist: str):
        self.title = title
        self.albumartist = albumartist

    def __call__(self):
        return fetch_album_bio(self.title, self.albumartist)


# TODO
# - Move the populate function to a new file and probably into a new class
# - Start movement from functional programming to OOP to OOP
