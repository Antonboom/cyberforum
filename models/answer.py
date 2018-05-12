from models.base import BaseModel


__all__ = ('Answer',)


class Answer(BaseModel):

    table_name = 'answer'
    fields = (
        'id',
        'text',
        'thread',
        'author',
        'created_at',
        'rating',
        'is_off_topic',
    )
