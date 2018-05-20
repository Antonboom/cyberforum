import wtforms as wt

from models import User, Forum, Section
from views.admin.base import ModelView


__all__ = ('ThreadModelView',)


class ThreadForm(wt.Form):

    title = wt.StringField(validators=(wt.validators.required(),))
    text = wt.TextAreaField(validators=(wt.validators.required(),))
    forum = wt.SelectField(choices=[
        (forum.id, forum.title)
        for forum in Forum.all()
    ], coerce=int)
    # TODO(a.telishev): Section relates from forum
    section = wt.SelectField(choices=[
        (section.id, section.title)
        for section in Section.all()
    ], coerce=int)


class ThreadModelView(ModelView):

    form = ThreadForm

    column_sortable_list = (
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
    can_set_page_size = False
    page_size = 50

    def get_list(self, *args, **kwargs):
        count, threads = super().get_list(*args, **kwargs)

        for thread in threads:
            thread.forum = Forum.get(thread.forum).title
            thread.section = Section.get(thread.section).title
            thread.author = User.get(thread.author).username

        return count, threads
