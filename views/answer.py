from datetime import datetime
from http import HTTPStatus

from flask import request, redirect, abort
from flask_login import current_user

from app import app
from models import Answer, Thread


__all__ = ('create_answer_view',)


@app.route('/answer/', methods=('POST',))
def create_answer_view():
    next_page = request.form['next']

    text = request.form['text']
    thread_id = request.form['thread']

    if not (text and thread_id):
        abort(HTTPStatus.BAD_REQUEST)

    answer = Answer.create(
        text=text[:65535],
        thread=thread_id,
        author=current_user.id,
        created_at=datetime.now(),
    )

    current_user.msg_count += 1
    current_user.save()

    thread = Thread.get(thread_id)
    thread.last_answer_time = answer.created_at
    thread.save()

    return redirect(next_page)
