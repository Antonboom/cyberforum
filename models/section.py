from models.base import BaseModel


__all__ = ('Section',)


class Section(BaseModel):

    table_name = 'section'
    fields = (
        'id', 'forum', 'title', 'parent', 'created_at', 'created_by'
    )
