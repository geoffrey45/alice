"""
This file contains the Artists class for interacting with artist documents in MongoDB.
"""
from app.db.mongodb import MongoArtists
from bson import ObjectId


class Artists(MongoArtists):
    """
    The artist class for all artist related database operations.
    """

    def __init__(self):
        super(Artists, self).__init__()

    def insert_artist(self, artist_obj: dict) -> None:
        self.collection.update_one(
            artist_obj, {"$set": artist_obj}, upsert=True
        )

    def get_all_artists(self) -> list:
        return self.collection.find()

    def get_artist_by_id(self, artist_id: str) -> dict:
        return self.collection.find_one({"_id": ObjectId(artist_id)})

    def get_artists_by_name(self, query: str) -> list:
        return self.collection.find({"name": query}).limit(20)
