from datetime import datetime

from flask_login import current_user
from werkzeug.utils import cached_property

from db import get_connector
from models.base import BaseModel


__all__ = ('Thread', 'ThreadLabel', 'ThreadsLabels')


class Thread(BaseModel):

    table_name = 'thread'
    fields = (
        'id',
        'title',
        'text',
        'forum',
        'section',
        'author',
        'created_at',
        'last_answer_time',
    )
    search_fields = (
        'title',
        'text',
        'author',
    )

    @classmethod
    def create(cls, **kwargs):
        kwargs['created_at'] = datetime.now()

        # TODO(a.telishev): Remove implicitness
        if 'author' not in kwargs:
            kwargs['author'] = current_user.id

        return super().create(**kwargs)

    @cached_property
    def answers_count(self):
        cursor = get_connector().cursor()

        query = """
            SELECT COUNT(*)
            FROM answer
            INNER JOIN thread ON thread.id = answer.thread
            WHERE thread.id = %(thread_id)s
        """
        cursor.execute(query, {'thread_id': self.id})
        count = next(cursor)[0]
        cursor.close()

        return count

    def set_last_answer_time(self):
        cursor = get_connector().cursor()

        query = """
            SELECT created_at
            FROM answer
            WHERE thread = %(thread_id)s
            ORDER BY created_at DESC
            LIMIT 1
        """
        cursor.execute(query, {'thread_id': self.id})

        try:
            self.last_answer_time = next(cursor)[0]
            self.save()

        except StopIteration:
            pass

    @property
    def created_at_pretty(self):
        return self.created_at.strftime('%d.%m.%Y, %H:%M:%S')


class ThreadLabel(BaseModel):

    table_name = 'thread_label'
    fields = (
        'id',
        'text',
    )


class ThreadsLabels(BaseModel):

    table_name = 'threads_labels'
    fields = (
        'id',
        'thread',
        'label',
    )
