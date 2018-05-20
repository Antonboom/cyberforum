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

    @property
    def created_at_pretty(self):
        return self.created_at.strftime('%d.%m.%Y, %H:%M:%S')

    def increment_rating(self):
        self.rating += 1
        self.save()

    def flag_as_off_topic(self):
        self.is_off_topic = 1
        self.save()
