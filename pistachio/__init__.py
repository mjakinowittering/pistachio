"""
Pistachio aims to simplify reoccurring tasks when working with the file system.
"""

__version__ = "0.7.0"


from dataclasses import dataclass
from pathlib import Path


import errno
import hashlib
import os
import shutil


# Classes ---------------------------------------------------------------------
@dataclass
class Pistachio:
    """
    Pistachio class describing a record in the file system.
    """
    # pylint: disable=too-many-instance-attributes
    # Eight is completely neccessary 😉
    path: str
    exists: bool
    is_directory: bool
    is_file: bool
    is_symlink: bool
    name: str
    stem: str
    suffix: str


@dataclass
class Tree:
    """
    Tree class describing the hierarchy of records in the file system.
    """
    path: str
    exists: bool
    is_directory: bool
    results: list


# Methods ---------------------------------------------------------------------
def copy(source_path_str, target_path_str):
    """
    Method to copy and paste a resource from one location to another.
    """
    if is_directory(source_path_str):
        shutil.copytree(
            source_path_str,
            target_path_str,
            symlinks=True,
            copy_function=shutil.copy
        )

    if is_file(source_path_str):
        shutil.copy(
            source_path_str,
            target_path_str
        )

    if is_symlink(source_path_str):
        Path(target_path_str).symlink_to(os.readlink(source_path_str))

    return exists(target_path_str)


def describe(path_str):
    """
    Method to describe the type of resources.
    """
    return Pistachio(
        path=path_str,
        exists=exists(path_str),
        is_directory=is_directory(path_str),
        is_file=is_file(path_str),
        is_symlink=is_symlink(path_str),
        name=name(path_str),
        stem=stem(path_str),
        suffix=suffix(path_str)
    )


def exists(path_str):
    """
    Method to return True or False whether a resource exists.
    """
    return True if is_symlink(path_str) else Path(path_str).exists()


def get_md5_hash(path_str):
    """
    Method to return the MD5 hash of a file.
    """
    md5_hash_str = None

    if exists(path_str) is True and is_file(path_str) is True:
        md5_hash = hashlib.md5()

        with open(path_str, "rb") as file_handle:
            for block in iter(lambda: file_handle.read(4096), b""):
                md5_hash.update(block)
            file_handle.close()

        md5_hash_str = md5_hash.hexdigest()

    return md5_hash_str


def is_directory(path_str):
    """
    Method to return True or False whether a resource is a directory.
    """
    return Path(path_str).is_dir()


def is_file(path_str):
    """
    Method to return True or False whether a resource is a file.
    """
    return Path(path_str).is_file()


def is_symlink(path_str):
    """
    Method to return True or False whether a resource is a symbolic link.
    """
    return Path(path_str).is_symlink()


def mkdir(path_str):
    """
    Method to create a new directory or directories recursively.
    """
    return Path(path_str).mkdir(parents=True, exist_ok=True)


def mklink(link_path_str, source_path_str):
    """
    Method to make a Symbolic Link.
    """
    Path(link_path_str).symlink_to(source_path_str)

    return exists(link_path_str)


def move(source_path_str, target_path_str):
    """
    Method to move a resource from one location to another.
    """
    shutil.move(source_path_str, target_path_str)

    return exists(target_path_str)


def name(path_str):
    """
    Method to return the name of a resource.
    """
    return os.path.basename(path_str)


def path_builder(path_type, root, *args):
    """
    Method to build a clear relative or absolute path to a resource.
    """
    path_str = None

    if path_type == "abs":
        path_str = os.path.join(root, os.path.normpath("/".join(args)))
    elif path_type == "rel":
        path_str = os.path.normpath("/".join(args))
    else:
        raise ValueError("""{type} but be 'abs' or 'rel'.""")

    return path_str


def scan_fs(path_str):
    """
    Private method to walk through a directory tree and discover all files
    and directories on the file system.
    """
    results_lst = []

    if exists(path_str) and is_directory(path_str):
        initial_path_str = os.getcwd()

        os.chdir(path_str)

        for base_str, directories_lst, filenames_lst in os.walk("."):
            for directory_str in directories_lst:
                results_lst.append(
                    describe(
                        path_builder(
                            "abs",
                            os.getcwd(),
                            *[
                                base_str,
                                directory_str
                            ]
                        )
                    )
                )
            for filename_str in filenames_lst:
                results_lst.append(
                    describe(
                        path_builder(
                            "abs",
                            os.getcwd(),
                            *[
                                base_str,
                                filename_str
                            ]
                        )
                    )
                )
        os.chdir(initial_path_str)
    else:
        raise FileNotFoundError(
            errno.ENOENT, os.strerror(errno.ENOENT), path_str
        )

    return results_lst


def stem(path_str):
    """
    Return the stem of the last item in the path.
    """
    return Path(path_str).stem


def suffix(path_str):
    """
    Return the file extension suffix of the last item in the path.
    """
    suffix_str = Path(path_str).suffix

    clean = [
        (".", "")
    ]

    for old, new in clean:
        suffix_str = suffix_str.replace(old, new)

    return suffix_str if suffix_str != '' else None


def touch(path_str):
    """
    Method to generated an empty file.
    """
    created = False

    if exists(path_str) is False:
        try:
            with open(path_str, "a", encoding="utf-8") as file_handle:
                file_handle.write("\n")
            created = exists(path_str)
        except FileNotFoundError as exc:
            raise FileNotFoundError(
                errno.ENOENT, os.strerror(errno.ENOENT), path_str
            ) from exc

    return created


def tree(path_str):
    """
    Method to walk through a directory tree and discover all files
    and directories on the file system. Returns a Tree object with a list of
    Pistachio results.
    """
    tree_obj = Tree(
        path=os.path.realpath(path_str),
        exists=exists(path_str),
        is_directory=is_directory(path_str),
        results=[]
    )

    if exists(path_str) and is_directory(path_str):
        tree_obj.results = scan_fs(path_str)
    else:
        raise FileNotFoundError(
            errno.ENOENT, os.strerror(errno.ENOENT), path_str
        )

    return tree_obj
