from functools import wraps

from flask import current_app, request
from src.api.exceptions.http import (
    HTTPInternalServerErrorException,
    HTTPUnauthorizedException,
)


def check_secret(fn):
    """Decorator that requires a valid secret in the headers"""

    @wraps(fn)
    def decorator(*args, **kwargs):
        if not request.method == "OPTIONS":
            _check_secret()
        return fn(*args, **kwargs)

    return decorator


def _check_secret():
    secret_header = request.headers.get("secret", "").strip()
    if not secret_header:
        raise HTTPUnauthorizedException("No secret header was found")

    my_secret = current_app.config.get("MY_SECRET")
    if not my_secret:
        raise HTTPInternalServerErrorException()

    if secret_header != my_secret:
        raise HTTPUnauthorizedException("Invalid secret")
