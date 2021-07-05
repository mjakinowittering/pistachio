from pathlib import Path
import os


def describe(path_str):
    """
    Method to describe the type of resources.
    """
    return {
        'abspath': os.path.abspath(path_str),
        'exists': exists(path_str),
        'is_directory': is_directory(path_str),
        'is_file': is_file(path_str),
        'is_symlink': is_symlink(path_str)
    }


def exists(path_str):
    """
    Method to return True or False whether a resource exists.
    """
    return Path(path_str).exists()


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
