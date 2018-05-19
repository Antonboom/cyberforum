from http import HTTPStatus

from flask import render_template


__all__ = ('page_not_found',)


def page_not_found(e):
    return render_template('error.html')
