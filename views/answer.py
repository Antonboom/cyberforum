from datetime import datetime
from http import HTTPStatus

from flask import request, redirect, abort, jsonify
from flask_login import current_user

from app import app
from models import Answer, Thread


__all__ = (
    'create_answer_view',
    'inc_answer_rating_view',
    'flag_answer_as_off_topic',
)


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


@app.route('/inc_answer_rating/<answer_id>/', methods=('GET',))
def inc_answer_rating_view(answer_id):
    answer_id = int(answer_id)

    answer = Answer.get(answer_id)
    if not answer:
        return abort(HTTPStatus.NOT_FOUND)

    if answer.is_off_topic:
        return abort(HTTPStatus.BAD_REQUEST)

    answer.increment_rating()

    return jsonify({
        'answer': answer_id,
        'rating': answer.rating,
    })


@app.route('/flag_answer_as_off_topic/<answer_id>/', methods=('GET',))
def flag_answer_as_off_topic(answer_id):
    if not (current_user.is_staff or current_user.is_admin):
        return abort(HTTPStatus.BAD_REQUEST)

    answer_id = int(answer_id)
    answer = Answer.get(answer_id)
    if not answer:
        return abort(HTTPStatus.NOT_FOUND)

    answer.flag_as_off_topic()

    return jsonify({
        'answer': answer_id,
        'is_off_topic': answer.is_off_topic,
    })
