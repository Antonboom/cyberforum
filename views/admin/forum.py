import wtforms as wt

from models import User
from views.admin.base import ModelView


__all__ = ('ForumModelView',)


class ForumForm(wt.Form):

    title = wt.StringField(validators=(wt.validators.required(),))


class ForumModelView(ModelView):

    form = ForumForm

    column_sortable_list = (
        'id',
        'title',
        'created_at',
        'created_by',
    )

    def get_list(self, *args, **kwargs):
        count, forums = super().get_list(*args, **kwargs)
        for forum in forums:
            forum.created_by = User.get(forum.created_by).username
        return count, forums
