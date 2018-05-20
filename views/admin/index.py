from flask_admin import AdminIndexView

from views.admin.mixins import AdminPermissionsMixin


__all__ = ('IndexView',)


class IndexView(AdminPermissionsMixin, AdminIndexView):
    pass
