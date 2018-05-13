from werkzeug.utils import cached_property

from db import get_connector
from models.base import BaseModel


__all__ = ('Section',)


class Section(BaseModel):

    table_name = 'section'
    fields = (
        'id', 'forum', 'title', 'parent', 'created_at', 'created_by'
    )

    @cached_property
    def threads_count(self):
        cursor = get_connector().cursor()

        query = """
            SELECT COUNT(*)
            FROM thread
            INNER JOIN section ON section.id = thread.section
            WHERE (
                section.id = %(parent_section)s OR
                section.parent = %(parent_section)s
            )
        """
        cursor.execute(query, {'parent_section': self.id})
        count = next(cursor)[0]
        cursor.close()

        return count

    @cached_property
    def answers_count(self):
        cursor = get_connector().cursor()

        query = """
            SELECT COUNT(*)
            FROM answer
            INNER JOIN thread ON thread.id = answer.thread
            INNER JOIN section ON section.id = thread.section
            WHERE (
                section.id = %(parent_section)s OR
                section.parent = %(parent_section)s
            )
        """
        cursor.execute(query, {'parent_section': self.id})
        count = next(cursor)[0]
        cursor.close()

        return count
