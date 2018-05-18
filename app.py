from flask import Flask
from flask.ext.login import LoginManager
from flask.ext.cache import Cache

import settings


__all__ = ('app',)

app = Flask(__name__)
app.secret_key = settings.SECRET_KEY

app.config['CACHE_TYPE'] = 'simple'
app.cache = Cache(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login_view'
login_manager.user_loader(lambda user_id: User.get(user_id))


from views.admin import admin_bp
app.register_blueprint(admin_bp, url_prefix='/admin')

from models import User
admin = User.get(pk_field='username', pk=settings.ADMIN_USERNAME)
if not admin:
    User.create(
        username=settings.ADMIN_USERNAME,
        email=settings.ADMIN_EMAIL,
        password=settings.ADMIN_PASSWORD,
    )
