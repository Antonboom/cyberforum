from flask import render_template, request

from app import app
from db import get_connector
from models import ThreadLabel, Thread, User, Answer


__all__ = ('thread_view',)


THREADS_PER_PAGE = 20


@app.route('/thread/<thread_id>/', methods=('GET',))
def thread_view(thread_id):
    thread = Thread.get(thread_id)
    author = User.get(thread.author)

    answers_query = """
        SELECT
            answer.id answer_id,
            answer.text answer_text,
            answer.rating answer_rating,
            answer.created_at answer_created_at,
            answer.is_off_topic answer_is_off_topic,

            user.id user_id,
            user.username username,
            user.msg_count user_msg_count,
            user.msg_signature user_signature,
            user.registered_at user_registered_at
        FROM answer
        INNER JOIN user ON answer.author = user.id
        WHERE answer.thread = %(thread_id)s
        ORDER BY answer.created_at;
    """
    cursor = get_connector().cursor()
    cursor.execute(answers_query, {'thread_id': thread.id})

    answers = [
        Answer(
            id=answer_id,
            text=answer_text,
            rating=answer_rating,
            created_at=answer_created_at,
            is_off_topic=answer_is_off_topic,
            author=User(
                id=user_id,
                username=username,
                msg_count=user_msg_count,
                msg_signature=user_signature,
                registered_at=user_registered_at,
            )
        )
        for (
            answer_id,
            answer_text,
            answer_rating,
            answer_created_at,
            answer_is_off_topic,

            user_id,
            username,
            user_msg_count,
            user_signature,
            user_registered_at,
        ) in cursor
    ]

    labels_query = """
        SELECT
            thread_label.id label_id,
            thread_label.text label_text
        FROM threads_labels
        INNER JOIN thread_label ON threads_labels.label = thread_label.id
        WHERE threads_labels.thread = %(thread_id)s;
    """
    cursor = get_connector().cursor()
    cursor.execute(labels_query, {'thread_id': thread.id})

    labels = [
        ThreadLabel(id=label_id, text=label_text)
        for label_id, label_text in cursor
    ]

    cursor.close()

    return render_template(
        'thread.html',
        author=author,
        thread=thread,
        labels=labels,
        answers=answers,
    )
