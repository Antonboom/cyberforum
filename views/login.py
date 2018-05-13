from flask import request, redirect, abort, Response
from flask.ext.login import login_user, logout_user

from app import app
from models import User


@app.route('/login/', methods=('GET', 'POST',))
def login_view():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.authenticate(username, password)
        if user:
            login_user(user)
            return redirect('/')

        return abort(401)

    return Response('''
        <form action="/login" method="POST">
            <p><input type=text name=username>
            <p><input type=password name=password>
            <p><input type=submit value=Login>
        </form>
    ''')


@app.route('/logout', methods=('GET',))
def logout_view():
    logout_user()
    return redirect('/')
