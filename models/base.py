from mysql.connector import IntegrityError

from db import get_connector


__all__ = ('BaseModel',)


class BaseModel:

    table_name = ''
    pk = 'id'

    fields = []
    sort_fields = []

    def __repr__(self):
        return f'<{self.__class__.__name__} id={self.id}>'

    def __init__(self, **kwargs):
        for field, value in kwargs.items():
            if field in self.fields:
                setattr(self, field, value)

    @classmethod
    def _make_list_from_cursor(cls, cursor):
        results = []
        for result in cursor:
            instance = cls()

            for field, value in zip(cls.fields, result):
                setattr(instance, field, value)

            results.append(instance)
        return results

    def save(self):
        connector = get_connector()
        cursor = connector.cursor()

        fields = []
        fields_values = {}
        for field in self.fields:
            if hasattr(self, field):
                fields.append(f'{field} = %({field})s')
                fields_values[field] = getattr(self, field)

        query = f"""
            UPDATE {self.table_name}
            SET {', '.join(fields)}
            WHERE {self.pk} = {getattr(self, self.pk)};
        """
        cursor.execute(query, fields_values)

        connector.commit()
        cursor.close()

        return self

    def delete(self):
        cursor = get_connector().cursor()
        query = f"""
            DELETE FROM {self.table_name}
            WHERE {self.pk} = {getattr(self, self.pk)};
        """

        cursor.execute(query)
        cursor.close()

    @classmethod
    def count(cls):
        cursor = get_connector().cursor()
        query = f"""
            SELECT COUNT(*) FROM {cls.table_name};
        """

        cursor.execute(query)
        cnt = next(cursor)[0]
        cursor.close()

        return cnt

    @classmethod
    def first(cls):
        cursor = get_connector().cursor()
        query = f"""
            SELECT * FROM {cls.table_name} LIMIT 1;
        """

        cursor.execute(query)
        result = cls._make_list_from_cursor(cursor)[0]
        cursor.close()

        return result

    @classmethod
    def all(cls, limit=None):
        cursor = get_connector().cursor()
        query = f"""
            SELECT * FROM {cls.table_name}
            {f'LIMIT {limit}' if limit else ''};
        """

        cursor.execute(query)
        results = cls._make_list_from_cursor(cursor)
        cursor.close()

        return results

    @classmethod
    def get(cls, pk, pk_field=None):
        pk_field = pk_field or cls.pk

        cursor = get_connector().cursor()
        query = f"""
            SELECT * FROM {cls.table_name}
            WHERE {pk_field} = %(pk)s;
        """
        cursor.execute(query, {'pk': pk})

        try:
            result = next(cursor)

            instance = cls()
            for field, value in zip(cls.fields, result):
                setattr(instance, field, value)

            return instance

        except StopIteration:
            pass

        cursor.close()

    @classmethod
    def create(cls, **kwargs):
        connector = get_connector()
        cursor = connector.cursor()

        fields = [
            field
            for field, value in kwargs.items()
            if field in cls.fields and value
        ]
        values = [
            f'%({field})s'
            for field in fields
        ]
        query = f"""
            INSERT INTO {cls.table_name}
            ({', '.join(fields)})
            VALUES({', '.join(values)});
        """

        try:
            cursor.execute(query, kwargs)
        except IntegrityError:
            return
        inserted_id = cursor.lastrowid

        connector.commit()
        cursor.close()

        # TODO(a.telishev): Just build instance
        return cls.get(pk=inserted_id)

    @classmethod
    def filter(cls,
               order_by=None, asc=True, search=None,
               limit=None, offset=None, **kwargs):
        connector = get_connector()
        cursor = connector.cursor()

        fields = kwargs.keys()
        conditions = [
            f'{field} = %({field})s'
            for field in fields
        ]
        likes = [
            f'{field} LIKE "{search}%"'
            for field in cls.fields
        ] if search else []

        where = (
            f"WHERE {' AND '.join(conditions)} {' OR '.join(likes)}"
            if conditions or likes
            else ''
        )
        order = 'ASC' if asc else 'DESC'
        query = f"""
            SELECT * FROM {cls.table_name}
            { where }
            {f'ORDER BY {order_by} {order}' if order_by else ''}
            {f'LIMIT {limit}' if limit else ''}
            {f'OFFSET {offset}' if offset else ''};
        """

        cursor.execute(query, kwargs)
        results = cls._make_list_from_cursor(cursor)
        cursor.close()

        return results

    @classmethod
    def find(cls, field, query):
        connector = get_connector()
        cursor = connector.cursor()

        query = f"""
            SELECT * FROM {cls.table_name}
            WHERE {field} LIKE '{query}%'
        """

        cursor.execute(query)
        results = cls._make_list_from_cursor(cursor)
        cursor.close()

        return results
