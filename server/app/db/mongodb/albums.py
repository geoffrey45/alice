"""
This file contains the Album class for interacting with
album documents in MongoDB.
"""
from bson import ObjectId
from app.models import Album
from app.db.mongodb import MongoAlbums
from app.db.mongodb import convert_many, convert_one


class Albums(MongoAlbums):
    """
    The class for all album-related database operations.
    """

    def insert_album(self, album: Album) -> str:
        album = album.__dict__
        upsert_id = self.collection.update_one(
            {"album": album["title"], "artist": album["artist"]},
            {"$set": album},
            upsert=True,
        ).upserted_id

        return str(upsert_id)

    def get_all_albums(self) -> list:
        albums = self.collection.find()
        return convert_many(albums)

    def get_album_by_id(self, id: str) -> dict:
        album = self.collection.find_one({"_id": ObjectId(id)})
        return convert_one(album)

    def get_album_by_name(self, name: str, artist: str) -> dict:
        album = self.collection.find_one({"album": name, "artist": artist})
        return convert_one(album)

    def get_album_by_artist(self, name: str) -> dict:
        album = self.collection.find_one({"albumartist": name})
        return convert_one(album)
