from db import get_connector


__all__ = ('BaseModel',)


class BaseModel:

    table_name = ''
    pk = 'id'
    fields = []

    def __repr__(self):
        return f'<{self.__class__.__name__} id={self.id}>'

    @classmethod
    def _make_list_from_cursor(cls, cursor):
        results = []
        for result in cursor:
            instance = cls()

            for field, value in zip(cls.fields, result):
                setattr(instance, field, value)

            results.append(instance)
        return results

    @classmethod
    def count(cls):
        cursor = get_connector().cursor()
        query = f"""
            SELECT COUNT(*) FROM {cls.table_name};
        """

        cursor.execute(query)
        count = next(cursor)[0]
        cursor.close()

        return count

    @classmethod
    def all(cls):
        cursor = get_connector().cursor()
        query = f"""
            SELECT * FROM {cls.table_name};
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

        fields = kwargs.keys()
        values = [
            f'%({field})s'
            for field in fields
        ]
        query = f"""
            INSERT INTO {cls.table_name}
            ({', '.join(fields)})
            VALUES({', '.join(values)});
        """

        cursor.execute(query, kwargs)
        inserted_id = cursor.lastrowid

        connector.commit()
        cursor.close()

        # TODO(a.telishev): Just build instance
        return cls.get(pk=inserted_id)

    @classmethod
    def bulk_create(cls, objs):
        connector = get_connector()
        cursor = connector.cursor()

        fields = kwargs.keys()
        values = [
            f'%({field})s'
            for field in fields
        ]
        query = f"""
            INSERT INTO {cls.table_name}
            ({', '.join(fields)})
            VALUES({', '.join(values)});
        """

    @classmethod
    def filter(cls, **kwargs):
        connector = get_connector()
        cursor = connector.cursor()

        fields = kwargs.keys()
        conditions = [
            f'{field} = %({field})s'
            for field in fields
        ]
        query = f"""
            SELECT * FROM {cls.table_name}
            WHERE {' AND '.join(conditions)};
        """
        cursor.execute(query, kwargs)
        results = cls._make_list_from_cursor(cursor)
        cursor.close()

        return results
