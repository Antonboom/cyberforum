from db import get_connector


__all__ = ('BaseModel',)


class BaseModel:

    table_name = ''
    pk = 'id'
    fields = []

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

        return cls.get(pk=inserted_id)
