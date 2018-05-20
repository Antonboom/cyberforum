import wtforms as wt

from views.admin.base import ModelView


__all__ = ('UserModelView',)


class UserForm(wt.Form):

    # TODO(a.telyshev): Password
    username = wt.StringField(validators=(wt.validators.required(),))
    email = wt.StringField(validators=(wt.validators.required(), wt.validators.email()))
    real_name = wt.StringField()
    birthday = wt.DateTimeField(format='%d.%m.%Y', description='Формат: 29.11.1996')
    location = wt.StringField()
    msg_signature = wt.TextAreaField()
    is_staff = wt.BooleanField()
    is_admin = wt.BooleanField()


class UserModelView(ModelView):

    form = UserForm

    column_exclude_list = (
        'avatar_url',
        'password_hash',
        'password_salt',
    )
    column_sortable_list = (
        'id',
        'username',
        'email',
        'reputation',
        'registered_at',
        'real_name',
        'birthday',
        'msg_count',
        'is_staff',
        'is_admin',
    )

