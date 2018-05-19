from flask import redirect, render_template, request
from mysql.connector import IntegrityError

from app import app
from models import User


__all__ = ('registration_view',)


PASSWORD_MIN_LENGTH = 6


@app.route('/registration/', methods=('GET', 'POST',))
def registration_view():
    errors = []

    if request.method == 'GET':
        return render_template('registration.html', data={})

    if request.method == 'POST':
        username = request.form.get('username')
        if not username:
            errors.append('Имя пользователя обязательно для заполнения')

        user = User.get(pk_field='username', pk=username)
        if user:
            errors.append('Пользователь с таким именем уже существует')

        email = request.form.get('email')
        if not email:
            errors.append('E-mail обязателен для заполнения')

        user = User.get(pk_field='email', pk=email)
        if user:
            errors.append('Пользователь с таким e-mail уже существует')

        password = request.form.get('password')
        if not password:
            errors.append('Пароль обязателен для заполнения')

        # TODO(a.telishev): Check password's complexity
        if len(password) < PASSWORD_MIN_LENGTH:
            errors.append('Пароль слишком короткий')

        password_repeat = request.form.get('password_repeat')
        if password != password_repeat:
            errors.append('Введённые пароли не совпадают')

        if errors:
            return render_template(
                'registration.html',
                data=request.form,
                errors=errors,
            )

        try:
            User.create(**{
                field: value
                for field, value in request.form.items()
            })

        except IntegrityError as err:
            return render_template(
                'registration.html',
                data=request.form,
                errors=[err],
            )

        return redirect('/login/')
