from flask import request, redirect, abort, render_template
from flask.ext.login import login_user, logout_user

from app import app
from models import User


@app.route('/login/', methods=('GET', 'POST',))
def login_view():
    next_page = request.args.get('next', '/')

    if request.method == 'POST':
        username = request.form['email']
        password = request.form['password']
        next_page = request.form['next']

        user = User.authenticate(username, password)
        if user:
            login_user(user)
            return redirect(next_page)

        errors = ('Проверьте правильность ведённых данных',)
        return render_template(
            'login.html',
            username=username,
            password=password,
            next=next_page,
            errors=errors,
        )

    return render_template('login.html', next=next_page)


@app.route('/logout/', methods=('GET',))
def logout_view():
    logout_user()
    return redirect('/login/')
