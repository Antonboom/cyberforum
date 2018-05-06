from functools import wraps
from flask import g, request, redirect, url_for


def login_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        if g.user is None:
            return redirect(url_for('login', next=request.url))
        return func(*args, **kwargs)
    return decorated
