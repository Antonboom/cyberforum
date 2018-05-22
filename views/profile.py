from http import HTTPStatus

from flask import abort
from flask import render_template
from flask_login import current_user

from app import app
from models import User, Thread


__all__ = ('profile_view',)


@app.route('/profile/<profile_id>/', methods=('GET',))
def profile_view(profile_id):
    if not current_user.is_authenticated:
        abort(HTTPStatus.NOT_FOUND)

    profile_id = int(profile_id)

    user = User.get(profile_id)
    if not user:
        abort(HTTPStatus.NOT_FOUND)

    threads_count = len(Thread.filter(author=profile_id))

    return render_template(
        'profile.html',
        user=user,
        threads_count=threads_count,
    )
