from flask import request, Response

from app import app


@app.route('/registration/', methods=('GET', 'POST',))
def register():
    if request.method == 'POST':
        pass
        # username = request.form['username']
        # password = request.form['password']
        # if password == username + "_secret":
        #     id = username.split('user')[1]
        #     user = User(id)
        #     login_user(user)
        #     return redirect(request.args.get("next"))
        # else:
        #     pass
        #     return abort(401)
    else:
        return Response('''
            <form action="/login" method="POST">
                <p><input type=text name=username>
                <p><input type=password name=password>
                <p><input type=submit value=Login>
            </form>
        ''')

#
# INSERT INTO `cyberforum`.`user`
# (`id`,
# `username`,
# `email`,
# `reputation`,
# `registered_at`,
# `avatar_url`,
# `real_name`,
# `birthday`,
# `location`,
# `msg_signature`,
# `msg_count`)
# VALUES
# (<{id: }>,
# <{username: }>,
# <{email: }>,
# <{password_hash: }>,
# <{password_salt: }>,
# <{reputation: }>,
# <{registered_at: }>,
# <{avatar_url: }>,
# <{real_name: }>,
# <{birthday: }>,
# <{location: }>,
# <{msg_signature: }>,
# <{msg_count: 0}>);
