from typing import List, Tuple, Optional
import textract
from django.db.models import Q
from mutagen.mp4 import MP4
from mutagen.mp3 import EasyMP3 as MP3
from mutagen.id3 import ID3
from nas.models import Folder, File, MusicMetaData
import os
from pathlib import PurePath
from django.core.files.uploadedfile import SimpleUploadedFile, InMemoryUploadedFile

from nas.utils.utils2 import VIDEO_EXT, AUDIO_EXT, is_document, DOCUMENT_EXT

"""
This file contains utils which use models
"""


def get_list_files(folder: Folder) -> List[File]:
    """
    Get list of files within the given folder. Also will return
    any file within sub folders
    :param folder: the folder you want
    :return: list of files
    """
    files = File.objects.filter(parent=folder).all()
    folders = Folder.objects.filter(parent=folder).all()
    for f in folders:
        sub_files = get_list_files(f)
        files = sub_files | files

    return files


def has_parent(path: str) -> bool:
    """
    Return whether the path has parent
    :param path: path like object. Ex: /a/b/c.txt
    :return: true, if path has parent
    """
    p = PurePath(path)
    parts = p.parts
    return len(parts) > 1


def create_folders(paths: List[str], parent: Optional[Folder]) -> Tuple[str, Folder]:
    """
    Recursively create folder.
    For example, if you have path a/b/c.txt in folder root. It will first create
    folder a, then create folder b and then return c.txt and folder b object
    :param paths: list of file paths
    :param parent: parent folder, None if parent is root
    :return: path base name and last folder object
    """
    if len(paths) == 1:
        return paths[0], parent

    sub_folders = Folder.objects.filter(parent=parent).all()
    sub_parent = None
    folder_name = paths[0]
    rest_paths = paths[1:]
    for folder in sub_folders:
        if folder.name == folder_name:
            sub_parent = folder
            break

    if not sub_parent:
        sub_parent = Folder.objects.create(name=folder_name, parent=parent)
        sub_parent.save()

    return create_folders(rest_paths, sub_parent)


def get_mp4_metadata(path: str) -> Tuple[str, str, str, str, int, int, SimpleUploadedFile, int, str, str]:
    """
    Return title, album, artist, year, genre, cover, duration, album_artist, track
    :param path: mp4 file
    :return:
    """
    info = MP4(path)
    title = info.tags.get("\xa9nam")
    album = info.tags.get('\xa9alb')
    artist = info.tags.get('\xa9ART')
    year = info.tags.get('\xa9day')
    genre = info.tags.get('\xa9gen')
    lyrics = info.get('\xa9lyr')
    cover = info.tags.get('covr')
    duration = info.info.length
    album_artist = info.tags.get('aART')
    track = info.tags.get('trkn')

    if album:
        album = album.pop()

    if lyrics:
        lyrics = lyrics.pop()

    if title:
        title = title.pop()

    if artist:
        artist = artist.pop()

    if year:
        year = year.pop()

    if genre:
        genre = genre.pop()

    if album_artist:
        album_artist = album_artist.pop()

    if track:
        trk, total = track[0]
        track = trk

    if cover:
        cover = cover[0]
        cover = SimpleUploadedFile(f'${title}-cover.jpg', bytes(cover), 'image/jpeg')

    return title, album, artist, year, genre, cover, duration, album_artist, track, lyrics


def get_mp3_metadata(path: str):
    info = ID3(path)
    mp3_info = MP3(path)
    lyrics = info.get("USLT::eng")
    cover = info.get('APIC:')
    duration = mp3_info.info.length
    title = mp3_info.get('title')
    album = mp3_info.get('album')
    artist = mp3_info.get('artist')
    year = mp3_info.get('date')
    genre = mp3_info.get('genre')
    track = mp3_info.get('tracknumber')
    album_artist = mp3_info.get('albumartist')

    if album:
        album = album.pop()

    if title:
        title = title.pop()

    if artist:
        artist = artist.pop()

    if year:
        year = year.pop()

    if genre:
        genre = genre.pop()

    if cover:
        cover = cover.data
        cover = SimpleUploadedFile(f'${title}-cover.jpg', bytes(cover), 'image/jpeg')

    if album_artist:
        album_artist = album_artist.pop()

    if track:
        try:
            track: str = track.pop()
            track = track.split('/')
            track = track[0]
        except Exception as e:
            track = 0

    return title, album, artist, year, genre, cover, duration, album_artist, track, lyrics


def get_and_create_music_metadata(file: File):
    """
    Create meta data for given file
    :param file:
    :return:
    """
    filename, ext = os.path.splitext(file.file.path)
    title: Optional[str] = None
    album: Optional[str] = None
    lyrics: Optional[str] = None
    artist: Optional[str] = None
    year: Optional[int] = None
    genre: Optional[str] = None
    cover: Optional[SimpleUploadedFile] = None
    duration: Optional[int] = None
    album_artist = None
    track = None

    if ext == ".m4a":
        title, album, artist, year, \
        genre, cover, duration, album_artist, track, lyrics = get_mp4_metadata(file.file.path)
    elif ext == ".mp3":
        title, album, artist, year, genre, \
        cover, duration, album_artist, track, lyrics = get_mp3_metadata(file.file.path)

    if title:
        if MusicMetaData.objects.filter(file=file).exists():
            metadata: MusicMetaData = MusicMetaData.objects.filter(file=file).first()
            metadata.title = title
            metadata.album = album
            metadata.year = year
            metadata.picture = cover
            metadata.genre = genre
            metadata.duration = duration
            metadata.album_artist = album_artist
            if lyrics:
                metadata.lyrics = lyrics
            try:
                metadata.track = int(track)
            except:
                pass
            metadata.save()
        else:
            metadata = MusicMetaData.objects.create(
                title=title,
                album=album,
                artist=artist,
                year=year,
                picture=cover,
                genre=genre,
                duration=duration,
                file=file,
                track=track,
                album_artist=album_artist,
                lyrics=lyrics
            )


def extra_text_content(file: File):
    try:
        content = textract.process(file.file.path)
        return content
    except Exception as e:
        return None


def extra_text_from_current_files() -> int:
    """
    Extra text from existing files
    :return: number of files
    """
    queryset = None
    for doc_ext in DOCUMENT_EXT:
        if not queryset:
            queryset = Q(file__icontains=doc_ext)
        else:
            queryset = queryset | Q(file__icontains=doc_ext)

    files = File.objects.filter(queryset).all()
    num = 0
    for file in files:
        try:
            file.save()
            num += 1
        except Exception as e:
            pass
    return num
