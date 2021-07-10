from pathlib import Path
from schema import Schema, And, Use, SchemaError
from src import pistachio


import pytest


DESCRIBE_SCHEMA = Schema({
    'abspath': And(Use(str)),
    'exists': And(Use(bool)),
    'is_directory': And(Use(bool)),
    'is_file': And(Use(bool)),
    'is_symlink': And(Use(bool)),
    'name': And(Use(str))
})


def schema_validation(example, schema):
    """
    Method to confirm with a dictionary matches a schema.
    """
    try:
        schema.validate(example)
        return True
    except SchemaError:
        return False


def setup_module():
    """
    Setup the required resources neccessary to run all the tests.
    """
    pass


def teardown_module():
    """
    Remove anything generated by testing.
    """
    Path('README.doc').unlink()


def test_describe_schema_directory():
    """
    Test to validate the describe method response for a directory.
    """
    example = pistachio.describe('tests')
    assert schema_validation(example, DESCRIBE_SCHEMA) is True


def test_describe_schema_file():
    """
    Test to validate the describe method response for a file.
    """
    example = pistachio.describe('README.md')
    assert schema_validation(example, DESCRIBE_SCHEMA) is True


def test_describe_schema_symlink():
    """
    Test to validate the describe method response for a symbolic link.
    """
    example = pistachio.describe('README.rst')
    assert schema_validation(example, DESCRIBE_SCHEMA) is True


def test_exists_true():
    """
    Test to confirm the exists method returns True.
    """
    assert pistachio.exists('README.md') is True


def test_exists_false():
    """
    Test to confirm the exists method returns False.
    """
    assert pistachio.exists('LICENSE.md') is False


def test_is_directory_true():
    """
    Test to confirm the is_directory method returns True.
    """
    assert pistachio.is_directory('tests') is True


def test_is_directory_false():
    """
    Test to confirm the is_directory method returns False.
    """
    assert pistachio.is_directory('LICENSE.md') is False


def test_is_file_true():
    """
    Test to confirm the is_file method returns True.
    """
    assert pistachio.is_file('README.md') is True


def test_is_file_false():
    """
    Test to confirm the is_file method returns False.
    """
    assert pistachio.is_file('tests') is False


def test_touch_new_file_true():
    """
    Test to confirm the touch method returns True.
    """
    assert pistachio.touch('README.doc') is True


def test_touch_file_exists_false():
    """
    Test to confirm the touch method returns True.
    """
    assert pistachio.touch('README.md') is False


def test_touch_directory_does_not_exist_false():
    """
    Test to confirm the touch method raised FileNotFoundError exception.
    """
    with pytest.raises(FileNotFoundError):
        pistachio.touch('docs/README.doc')