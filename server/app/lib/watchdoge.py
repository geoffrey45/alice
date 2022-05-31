"""
This library contains the classes and functions related to the watchdog file watcher.
"""
import os
import time

from app import api
from app import instances
from app import models
from app.helpers import create_album_hash
from app.lib import folderslib
from app.lib.albumslib import create_album
from app.lib.albumslib import find_album
from app.lib.taglib import get_tags
from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer


class OnMyWatch:
    """
    Contains the methods for initializing and starting watchdog.
    """

    directory = os.path.expanduser("~")

    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.directory, recursive=True)
        self.observer.start()

        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            print("Observer Stopped")

        self.observer.join()


def add_track(filepath: str) -> None:
    """
    Processes the audio tags for a given file ands add them to the music dict.

    Then creates a folder object for the added track and adds it to api.FOLDERS
    """
    tags = get_tags(filepath)

    if tags is not None:
        hash = create_album_hash(tags["album"], tags["albumartist"])
        tags["albumhash"] = hash
        api.DB_TRACKS.append(tags)

        albumindex = find_album(api.ALBUMS, hash)

        if albumindex is not None:
            album = api.ALBUMS[albumindex]
        else:
            album_data = create_album(tags, api.DB_TRACKS)
            album = models.Album(album_data)

            instances.album_instance.insert_album(album)
            api.ALBUMS.append(album)

        tags["image"] = album.image
        upsert_id = instances.tracks_instance.insert_track(tags)
        tags["_id"] = {"$oid": str(upsert_id)}

        api.TRACKS.append(models.Track(tags))

        folder = tags["folder"]

        if folder not in api.VALID_FOLDERS:
            api.VALID_FOLDERS.add(folder)
            f = folderslib.create_folder(folder)
            api.FOLDERS.append(f)


def remove_track(filepath: str) -> None:
    """
    Removes a track from the music dict.
    """
    fname = filepath.split("/")[-1]
    fpath = filepath.replace(fname, "")

    try:
        trackid = instances.tracks_instance.get_track_by_path(
            filepath)["_id"]["$oid"]
    except TypeError:
        print(f"💙 Watchdog Error: Error removing track {filepath} TypeError")
        return

    instances.tracks_instance.remove_track_by_id(trackid)

    for track in api.TRACKS:
        if track.trackid == trackid:
            api.TRACKS.remove(track)

    for folder in api.FOLDERS:
        if folder.path + "/" == fpath and folder.trackcount - 1 == 0:
            api.FOLDERS.remove(folder)
            api.VALID_FOLDERS.remove(folder.path)


class Handler(PatternMatchingEventHandler):
    files_to_process = []

    def __init__(self):
        print("💠 started watchdog 💠")
        PatternMatchingEventHandler.__init__(
            self,
            patterns=["*.flac", "*.mp3"],
            ignore_directories=True,
            case_sensitive=False,
        )

    def on_created(self, event):
        """
        Fired when a supported file is created.
        """
        print("🔵 created +++")
        self.files_to_process.append(event.src_path)

    def on_deleted(self, event):
        """
        Fired when a delete event occurs on a supported file.
        """
        print("🔴 deleted ---")
        remove_track(event.src_path)

    def on_moved(self, event):
        """
        Fired when a move event occurs on a supported file.
        """
        print("🔘 moved -->")
        tr = "share/Trash"

        if tr in event.dest_path:
            print("trash ++")
            remove_track(event.src_path)

        elif tr in event.src_path:
            add_track(event.dest_path)

        elif tr not in event.dest_path and tr not in event.src_path:
            add_track(event.dest_path)
            remove_track(event.src_path)

    def on_closed(self, event):
        """
        Fired when a created file is closed.
        """
        print("⚫ closed ~~~")
        try:
            self.files_to_process.remove(event.src_path)
        except ValueError:
            """
            The file was already removed from the list, or it was not in the list to begin with.
            """
            pass

        add_track(event.src_path)


watch = OnMyWatch()
