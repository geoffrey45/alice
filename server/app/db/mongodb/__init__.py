"""
This module creates and initiliazes a MongoDB instance. 

It also contains the `convert_one()` and `conver_many()` 
methods for converting MongoDB cursors to Python dicts.
"""

import json

import pymongo
from app.db import AlbumsMethods, ArtistsMethods, PlaylistsMethods, TrackMethods
from bson import json_util


class Mongo:
    """
    The base class for all mongodb classes.
    """

    def __init__(self, database):
        print("Connecting to MongoDB...")
        mongo_uri = pymongo.MongoClient()
        self.db = mongo_uri[database]


class MongoTracks(Mongo, TrackMethods):
    """
    The class for all track-related database operations.
    """

    def __init__(self):
        super(MongoTracks, self).__init__("ALICE_MUSIC_TRACKS")
        self.collection = self.db["ALL_TRACKS"]


class MongoArtists(Mongo, ArtistsMethods):
    """
    Class for interacting with artist documents in MongoDB.
    """

    def __init__(self):
        super(MongoArtists, self).__init__("ALICE_ARTISTS")
        self.collection = self.db["ALL_ARTISTS"]


class MongoPlaylists(Mongo, PlaylistsMethods):
    """
    Class for interacting with playlist documents in MongoDB.
    """

    def __init__(self):
        super(MongoPlaylists, self).__init__("ALICE_PLAYLISTS")
        self.collection = self.db["ALL_PLAYLISTS"]


class MongoAlbums(Mongo, AlbumsMethods):
    """
    Class for interacting with album documents in MongoDB.
    """

    def __init__(self):
        super(MongoAlbums, self).__init__("ALICE_ALBUMS")
        self.collection = self.db["ALL_ALBUMS"]



def convert_one(track: dict) -> dict:
    """
    Converts a single mongodb cursor to a json object.
    """
    data = json.dumps(track, default=json_util.default)
    track: dict = json.loads(data)

    return track


def convert_many(tracks: list[dict]) -> list[dict]:
    """
    Converts a list of mongodb cursors to a list of json objects.
    """

    tracks = []

    for track in tracks:
        data = json.dumps(track, default=json_util.default)
        track = json.loads(data)

        tracks.append(track)

    return tracks
