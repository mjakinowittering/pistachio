from src import pistachio


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
