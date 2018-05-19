from http import HTTPStatus

from flask import Flask
from flask_admin import Admin
from flask_cache import Cache
from flask_login import LoginManager

import settings
from models import User


__all__ = ('app',)


app = Flask(__name__)
app.secret_key = settings.SECRET_KEY

app.config['CACHE_TYPE'] = 'simple'
app.cache = Cache(app)

from views import errors
app.register_error_handler(HTTPStatus.NOT_FOUND, errors.page_not_found)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login_view'
login_manager.user_loader(lambda user_id: User.get(user_id))

admin = Admin(app, name=settings.PROJECT_NAME, template_mode='bootstrap3')

from views.admin import UserModelView
admin.add_view(UserModelView(User))

from models import User
admin_user = User.get(pk_field='username', pk=settings.ADMIN_USERNAME)
if not admin_user:
    User.create(
        username=settings.ADMIN_USERNAME,
        email=settings.ADMIN_EMAIL,
        password=settings.ADMIN_PASSWORD,
        is_staff=True,
        is_admin=True,
    )
