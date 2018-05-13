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
        'is_important',
        'rating',
        'last_answer_time',
    )


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
