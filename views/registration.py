from flask import request, Response

from app import app


# @app.route('/register', methods=('GET', 'POST',))
# def register():
#     if request.method == 'POST':
#         # username = request.form['username']
#         # password = request.form['password']
#         # if password == username + "_secret":
#         #     id = username.split('user')[1]
#         #     user = User(id)
#         #     login_user(user)
#         #     return redirect(request.args.get("next"))
#         # else:
#         #     pass
#         #     return abort(401)
#     else:
#         return Response('''
#             <form action="/login" method="POST">
#                 <p><input type=text name=username>
#                 <p><input type=password name=password>
#                 <p><input type=submit value=Login>
#             </form>
#         ''')
