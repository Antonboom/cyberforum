import mysql.connector


__all__ = ('get_connector',)


connector = None


def get_connector():
    global connector

    if connector is None:
        connector = mysql.connector.connect(user='root', password='mysqlboom', database='cyberforum')

    return connector
