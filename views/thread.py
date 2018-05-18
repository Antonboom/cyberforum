from http import HTTPStatus

from flask import abort, render_template, jsonify, request, redirect
from flask.ext.login import current_user

from app import app
from db import get_connector
from models import (
    ThreadLabel, Thread, User, Answer, Forum, Section,
    ThreadsLabels,
)


__all__ = (
    'create_thread_view',
    'thread_view',
    'thread_label_view',
    'thread_label_search_view',
)


THREADS_PER_PAGE = 20


@app.route('/thread/', methods=('POST',))
def create_thread_view():
    forum = request.form['forum']
    section = request.form['section']
    title = request.form['title']
    text = request.form['text']

    new_thread = Thread.create(
        author=current_user.id,
        forum=forum,
        section=section,
        title=title,
        text=text,
    )

    labels = [
        label.strip()
        for label in request.form['labels'].split(',')
        if label.strip()
    ]
    if labels:
        for label in labels:
            thread_label = ThreadLabel.filter(text=label)
            if thread_label:
                thread_label = thread_label[0]
            else:
                thread_label = ThreadLabel.create(text=label)

            ThreadsLabels.create(
                thread=new_thread.id,
                label=thread_label.id,
            )

    return redirect(f'/thread/{new_thread.id}')


@app.route('/thread/<thread_id>/', methods=('GET',))
def thread_view(thread_id):
    thread = Thread.get(thread_id)

    forum = Forum.get(thread.forum)
    section = Section.get(thread.section)
    parent_section = Section.get(section.parent)
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
        forum=forum,
        parent_section=parent_section,
        section=section,

        author=author,
        thread=thread,
        labels=labels,
        answers=answers,
    )


@app.route('/thread_label/<thread_id>/', methods=('GET',))
def thread_label_view(thread_id):
    thread = Thread.get(thread_id)

    if not thread:
        abort(HTTPStatus.BAD_REQUEST)

    labels = ThreadLabel.filter(thread=thread.id)

    return jsonify({
        'thread': thread_id,
        'labels': [label.text for label in labels],
    })


@app.route('/thread_label_search/', methods=('GET',))
def thread_label_search_view():
    label_query = request.args.get('query')
    if not label_query:
        abort(HTTPStatus.BAD_REQUEST)

    labels = ThreadLabel.find(field='text', query=label_query.strip())

    return jsonify({
        'query': label_query,
        'labels': [label.text for label in labels],
    })
