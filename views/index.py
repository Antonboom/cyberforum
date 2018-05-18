from flask import render_template

from app import app
from db import get_connector


__all__ = ('index_view',)


@app.route('/', methods=('GET',))
@app.cache.cached(timeout=60 * 60)
def index_view():
    # TODO(a.telishev): More ORM!
    threads_count_query = """
        SELECT
            forum.id forum_id,
            forum.title forum_title,
            section.id section_id,
            section.title section_title,
            parent_section.id parent_section_id,
            parent_section.title parent_section_title
        FROM section
        LEFT JOIN section parent_section ON section.parent = parent_section.id
        INNER JOIN forum ON section.forum = forum.id;
    """
    cursor = get_connector().cursor()
    cursor.execute(threads_count_query)

    # forums = {
    #   forum_id: {
    #       'id': forum_id,
    #       'title': forum_title,
    #       'sections': {
    #           'section_title': {
    #               'title': section_title,
    #               'threads_count': section_threads_count,
    #               'answers_count': section_answers_count,
    #               'subsections': [{
    #                   'id': subsection_id,
    #                   'title': subsection_title,
    #               }, ...],
    #           },
    #           ...
    #       },
    #   },
    #   ...
    # }
    #
    forums = {}
    for forum_id, forum_title, section_id, section_title, parent_section_id, parent_section_title in cursor:
        if forum_id not in forums:
            forums[forum_id] = {
                'id': forum_id,
                'title': forum_title,
                'sections': {},
            }
        else:
            if not parent_section_id:
                continue

            # TODO(a.telyshev): Oh, my God :(
            forums[forum_id]['sections'].setdefault(parent_section_id, {
                'id': parent_section_id,
                'title': parent_section_title,
                'subsections': [],
            })['subsections'].append({
                'id': section_id,
                'title': section_title
            })

    for _, forum in forums.items():
        for section_title, section in forum['sections'].items():
            # TODO(a.telishev): More ORM!
            threads_count_query = """
                SELECT COUNT(*)
                FROM thread
                INNER JOIN section ON section.id = thread.section
                WHERE (
                    section.id = %(parent_section)s OR
                    section.parent = %(parent_section)s
                )
            """
            cursor.execute(threads_count_query, {'parent_section': section['id']})
            forum['sections'][section_title]['threads_count'] = next(cursor)[0]

            answers_count_query = """
                SELECT COUNT(*)
                FROM answer
                INNER JOIN thread ON thread.id = answer.thread
                INNER JOIN section ON section.id = thread.section
                WHERE (
                    section.id = %(parent_section)s OR
                    section.parent = %(parent_section)s
                )
            """
            cursor.execute(answers_count_query, {'parent_section': section['id']})
            forum['sections'][section_title]['answers_count'] = next(cursor)[0]

    cursor.close()
    return render_template('index.html', forums=forums)
