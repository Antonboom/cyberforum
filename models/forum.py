from models.base import BaseModel


__all__ = ('Forum',)


class Forum(BaseModel):

    table_name = 'forum'
    fields = (
        'id', 'title', 'created_at', 'created_by'
    )
