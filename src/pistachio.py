from pathlib import Path


import errno
import hashlib
import os


def describe(path_str):
    """
    Method to describe the type of resources.
    """
    return {
        "abspath": os.path.abspath(path_str),
        "exists": exists(path_str),
        "is_directory": is_directory(path_str),
        "is_file": is_file(path_str),
        "is_symlink": is_symlink(path_str),
        "name": path_str.split("/")[-1],
        "md5": "CHEESE"
    }


def exists(path_str):
    """
    Method to return True or False whether a resource exists.
    """
    return Path(path_str).exists()


def get_md5_hash(path_str):
    """
    Method to return the MD5 hash of a file.
    """
    if exists(path_str) is True:
        md5_hash = hashlib.md5()
        with open(path_str, "rb") as fh:
            for block in iter(lambda: fh.read(4096), b""):
                md5_hash.update(block)
            fh.close()
        return md5_hash.hexdigest()
    else:
        raise FileNotFoundError(
            errno.ENOENT, os.strerror(errno.ENOENT), path_str
        )


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


def touch(path_str):
    """
    Method to generated an empty file.
    """
    if exists(path_str) is False:
        try:
            open(path_str, "a").close()
            return True
        except FileNotFoundError:
            raise FileNotFoundError(
                errno.ENOENT, os.strerror(errno.ENOENT), path_str
            )
    else:
        return False
