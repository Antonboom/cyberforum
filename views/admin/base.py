from flask.ext.login import current_user
from flask_admin.model import BaseModelView


__all__ = ('ModelView',)


class AdminPermissionsMixin:

    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin


class ModelView(AdminPermissionsMixin, BaseModelView):

    simple_list_pager = True
    can_set_page_size = True
    can_delete = False

    def get_pk_value(self, model):
        return model.id

    def scaffold_list_columns(self):
        return self.model.fields

    def scaffold_sortable_columns(self):
        return self.model.sort_fields

    def init_search(self):
        return True

    def scaffold_form(self):
        return self.form

    def get_list(self, page, sort_field, sort_desc, search, filters, page_size=None):
        results = self.model.filter(
            order_by=sort_field,
            asc=not sort_desc,
            search=search,
            limit=page_size,
            offset=page * ((page_size or 1) - 1),
        )
        return self.model.count(), results

    def get_one(self, id):
        return self.model.get(id)

    def create_model(self, form):
        """
        :type form: wtforms.Form
        """
        self.model.create(**form.data)

    def update_model(self, form, model):
        pass

    def delete_model(self, model):
        model.delete()

    def is_valid_filter(self, filter):
        pass

    def scaffold_filters(self, name):
        pass

    def _create_ajax_loader(self, name, options):
        pass

    def scaffold_list_form(self, widget=None, validators=None):
        pass
