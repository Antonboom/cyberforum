import mysql.connector

import settings


__all__ = ('get_connector',)


connector = None


def get_connector():
    global connector

    if connector is None:
        connector = mysql.connector.connect(
            user=settings.DB_USER,
            password=settings.DB_PASSWORD,
            database=settings.DB_NAME,
        )

    return connector
