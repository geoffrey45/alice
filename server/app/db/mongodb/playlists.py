"""
This file contains the Playlists class for interacting with the playlist documents in MongoDB.
"""
from app.db.mongodb import MongoPlaylists
from app.db.mongodb import convert_many, convert_one
from bson import ObjectId

from app.helpers import create_new_date


class Playlists(MongoPlaylists):
    """
    The class for all playlist-related database operations.
    """

    def insert_playlist(self, playlist: dict) -> None:
        return self.collection.update_one(
            {"name": playlist["name"]},
            {"$set": playlist},
            upsert=True,
        ).upserted_id

    def get_all_playlists(self) -> list:
        playlists = self.collection.find()
        return convert_many(playlists)

    def get_playlist_by_id(self, id: str) -> dict:
        playlist = self.collection.find_one({"_id": ObjectId(id)})
        return convert_one(playlist)

    def add_track_to_playlist(self, playlistid: str, track: dict) -> None:
        date = create_new_date()

        return self.collection.update_one(
            {
                "_id": ObjectId(playlistid),
            },
            {"$push": {"pre_tracks": track}, "$set": {"lastUpdated": date}},
        )

    def get_playlist_by_name(self, name: str) -> dict:
        playlist = self.collection.find_one({"name": name})
        return convert_one(playlist)

    def update_playlist(self, playlistid: str, playlist: dict) -> None:
        return self.collection.update_one(
            {"_id": ObjectId(playlistid)},
            {"$set": playlist},
        )
