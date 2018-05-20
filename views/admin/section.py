import wtforms as wt

from models import User, Forum, Section
from views.admin.base import ModelView


__all__ = ('SectionModelView',)


class SectionForm(wt.Form):

    title = wt.StringField(validators=(wt.validators.required(),))
    forum = wt.SelectField(choices=[
        (forum.id, forum.title)
        for forum in Forum.all()
    ], coerce=int)
    # TODO(a.telishev): Section relates from forum
    parent = wt.SelectField(choices=[
        (section.id, section.title)
        for section in Section.all()
    ], coerce=int)


class SectionModelView(ModelView):

    form = SectionForm

    column_sortable_list = (
        'id',
        'forum',
        'title',
        'parent',
        'created_at',
        'created_by',
    )
    can_set_page_size = False
    page_size = 10

    def get_list(self, *args, **kwargs):
        count, sections = super().get_list(*args, **kwargs)

        for section in sections:
            section.forum = Forum.get(section.forum).title
            parent = Section.get(section.parent)
            if parent:
                section.parent = parent.title
            section.created_by = User.get(section.created_by).username

        return count, sections
