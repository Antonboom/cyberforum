import hashlib
from datetime import datetime

from models.base import BaseModel


__all__ = ('User',)


class User(BaseModel):

    table_name = 'user'
    fields = (
        'id',
        'username',
        'email',
        'password_hash',
        'password_salt',
        'reputation',
        'registered_at',
        'avatar_url',
        'real_name',
        'birthday',
        'location',
        'msg_signature',
        'msg_count',
        'is_staff',
        'is_admin',
    )

    @classmethod
    def _get_password_data(cls, password):
        password_salt = str(datetime.now().timestamp())
        password_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
        return password_salt, password_hash

    @classmethod
    def create(cls, **kwargs):
        password = kwargs.pop('password')
        password_salt, password_hash = cls._get_password_data(password)
        kwargs.update({
            'password_hash': password_hash,
            'password_salt': password_salt,
        })
        return super(cls, User).create(**kwargs)

    @classmethod
    def authenticate(cls, username, password):
        user = cls.get(pk_field='username', pk=username)
        if not user:
            return None

        _, password_hash = cls._get_password_data(password)
        if password_hash == user.password_hash:
            return user

        return None

    def get_id(self):
        return self.id

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True
