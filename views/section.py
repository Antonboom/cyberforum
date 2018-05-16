from flask import render_template, request

from app import app
from db import get_connector
from models import Section, Forum, Thread


__all__ = ('section_view',)


THREADS_PER_PAGE = 20


@app.route('/section/<section_id>/', methods=('GET',))
def section_view(section_id):
    section = Section.get(section_id)
    forum = Forum.get(section.forum)
    parent_section = Section.get(section.parent)
    subsections = Section.filter(parent=section.id)

    # Threads
    try:
        page = int(request.args.get('page'))
    except (TypeError, ValueError):
        page = 1

    if not page or page < 1:
        page = 1

    threads_count = len(Thread.filter(section=section.id))
    pages_count = threads_count // THREADS_PER_PAGE

    if page > pages_count:
        page = pages_count

    prev_page = page - 1
    next_page = page + 1
    if page == 1:
        prev_page = None
    if page == pages_count:
        next_page = None

    offset = (page - 1) * THREADS_PER_PAGE

    query = """
        SELECT
            thread.id thread_id,
            thread.title thread_title,
            thread.created_at thread_created_at,
            thread.last_answer_time thread_last_answer_time,
            user.id user_id,
            user.username username
        FROM thread
        INNER JOIN user ON thread.author = user.id
        WHERE section = %(section_id)s
        ORDER BY thread.last_answer_time DESC
        LIMIT %(limit)s
        OFFSET %(offset)s;
    """
    cursor = get_connector().cursor()

    cursor.execute(query, {
        'section_id': section.id,
        'limit': THREADS_PER_PAGE,
        'offset': offset,
    })
    threads = {
        thread_id: {
            'id': thread_id,
            'title': thread_title,
            'created_at': thread_created_at.strftime('%d %b %Y'),
            'created_at_h': thread_created_at.strftime('%d %b %Y\n%H:%M:%S'),
            'last_answer_time': (
                thread_last_answer_time.strftime('%d %b %Y\n%H:%M:%S')
                if thread_last_answer_time else None
            ),
            'user_id': user_id,
            'username': username,
        }
        for (
            thread_id,
            thread_title,
            thread_created_at,
            thread_last_answer_time,
            user_id,
            username,
        ) in cursor
    }

    answers_count_query = f"""
        SELECT
            thread.id,
            COUNT(*)
        FROM thread INNER JOIN answer on thread.id = answer.thread
        WHERE thread.id IN ({
            ', '.join(str(thread_id) for thread_id in threads)
        })
        GROUP BY thread.id;
    """
    cursor.execute(answers_count_query)
    for thread_id, answers_count in cursor:
        threads[thread_id]['answers_count'] = answers_count

    cursor.close()

    return render_template(
        'section.html',
        section=section,
        forum=forum,
        parent_section=parent_section,
        subsections=subsections,

        threads=threads.values(),
        next_page=next_page,
        curr_page=page,
        prev_page=prev_page,
    )
