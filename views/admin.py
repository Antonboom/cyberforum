from flask import Blueprint
from flask.ext.login import login_required

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/forum')
@login_required
def forum_admin():
    return 'Hello from forum admin'
