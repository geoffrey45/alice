from typing import List
from app import models, functions, helpers
from app import trackslib, api


@helpers.background
def create_everything() -> List[models.Track]:
    """
    Creates album objects for all albums and returns
    a list of track objects
    """
    albums: list[models.Album] = functions.get_all_albums()

    api.ALBUMS.clear()
    api.ALBUMS.extend(albums)
    trackslib.create_all_tracks()



def get_album_duration(album: list) -> int:
    """
    Gets the duration of an album.
    """

    album_duration = 0

    for track in album:
        album_duration += track["length"]

    return album_duration


def get_album_image(album: list) -> str:
    """
    Gets the image of an album.
    """

    for track in album:
        img = functions.extract_thumb(track["filepath"])

        if img is not None:
            return img

    return functions.use_defaults()


def find_album(albumtitle, artist):
    for album in api.ALBUMS:
        if album.album == albumtitle and album.artist == artist:
            return album


def search_albums_by_name(query: str) -> List[models.Album]:
    """
    Searches albums by album name.
    """
    title_albums: List[models.Album] = []
    artist_albums: List[models.Album] = []

    for album in api.ALBUMS:
        if query.lower() in album.album.lower():
            title_albums.append(album)

    for album in api.ALBUMS:
        if query.lower() in album.artist.lower():
            artist_albums.append(album)

    return [*title_albums, *artist_albums]