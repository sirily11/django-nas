from typing import List

from nas.models import Folder, File
from pathlib import PurePath


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


