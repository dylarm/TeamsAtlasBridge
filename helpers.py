from functools import wraps
from pathlib import Path

from constants import VALID_EXTENSIONS


def add_method(cls):
    """
    Helper decorator to add methods to classes

    From https://medium.com/@mgarod/dynamically-add-a-method-to-a-class-in-python-c49204b85bd6
    """

    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            return func(*args, **kwargs)

        setattr(cls, func.__name__, wrapper)
        # Note we are not binding func, but wrapper which accepts self but does exactly the same as func
        return func

    return decorator


def valid_extension(file: Path) -> bool:
    return bool([ext for ext in VALID_EXTENSIONS if (ext in file.name)])
