from datetime import datetime
from http import HTTPStatus

from flask import abort, request, jsonify
from flask_admin import BaseView, expose

from app import app
from db import get_connector
from models import Forum, Section, Thread, ThreadLabel, Answer, User
from views.admin.mixins import AdminPermissionsMixin


__all__ = ('StatisticsView',)


class StatisticsView(AdminPermissionsMixin, BaseView):

    @expose('/')
    @app.cache.cached(timeout=60 * 60)
    def index(self):
        counts = {
            'forums': Forum.count(),
            'sections': Section.count(),
            'threads': Thread.count(),
            'labels': ThreadLabel.count(),
            'answers': Answer.count(),
            'users': User.count(),
        }
        for item, count in counts.items():
            counts[item] = '{:,}'.format(counts[item])

        date = datetime.now().strftime('%d.%m.%Y %H:%M')

        return self.render(
            'admin/statistics.html',
            date=date,
            counts=counts,
        )

    @expose('/years/')
    def years(self):
        """
        Statistics by years
        """
        start_year = request.args.get('start', 2000)
        end_year = request.args.get('end', 2018)

        if end_year <= start_year:
            abort(HTTPStatus.BAD_REQUEST)

        threads_query = f"""
            SELECT
                COUNT(*),
                YEAR(created_at) as year
            FROM thread
            WHERE YEAR(created_at) BETWEEN {start_year} AND {end_year}
            GROUP BY YEAR(created_at)
            ORDER BY year;
        """
        cursor = get_connector().cursor()
        cursor.execute(threads_query)

        years = []
        created_threads = []
        for threads_count, year in cursor:
            years.append(year)
            created_threads.append(threads_count)

        users_query = f"""
            SELECT
                COUNT(*),
                YEAR(registered_at) as year
            FROM user
            WHERE YEAR(registered_at) BETWEEN {start_year} AND {end_year}
            GROUP BY YEAR(registered_at)
            ORDER BY year;
        """
        cursor.execute(users_query)

        registered_users = []
        for users_count, year in cursor:
            if year in years:
                registered_users.append(users_count)

        return jsonify({
            'years': years,
            'created_threads': created_threads,
            'registered_users': registered_users,
        })
