from typing import List, Tuple, Optional

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
