from app import greet


def test_greet():
    assert greet() == "Hello Sean, world!"
