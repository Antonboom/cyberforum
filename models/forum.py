from datetime import datetime

from flask_login import current_user

from models.base import BaseModel


__all__ = ('Forum',)


class Forum(BaseModel):

    table_name = 'forum'
    fields = (
        'id', 'title', 'created_at', 'created_by'
    )
    search_fields = ('title',)

    @classmethod
    def create(cls, **kwargs):
        kwargs['created_at'] = datetime.now()

        # TODO(a.telishev): Remove implicitness
        if 'created_by' not in kwargs:
            kwargs['created_by'] = current_user.id

        return super().create(**kwargs)
