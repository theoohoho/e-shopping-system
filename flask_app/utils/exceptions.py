"""Defined exception
"""


def crud_exception_handler(func):
    """A decorator to handle exception from db crud operation
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception:
            raise
    return wrapper
