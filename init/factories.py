import random
from faker import Faker
from mysql.connector import IntegrityError

import settings
from models import User, Thread


__all__ = ('UserFactory', 'ThreadFactory',)


fake = Faker()


class UserFactory:

    MAX_REPUTATION = 100000
    MAX_SIGNATURE_SIZE = 100

    @classmethod
    def create(cls):
        def user_create():
            profile = fake.profile()
            return User.create(**{
                'username': profile['username'],
                'email': profile['mail'],
                'password': settings.USER_PASSWORD,
                'reputation': random.randint(0, cls.MAX_REPUTATION + 1),
                'registered_at': fake.date_time_this_century(before_now=True, after_now=False),
                'real_name': profile['name'],
                'birthday': fake.date_time_between(start_date='-60y', end_date='-15y'),
                'location': profile['residence'],
                'msg_signature': fake.text(max_nb_chars=cls.MAX_SIGNATURE_SIZE),
            })

        for _ in range(100):
            try:
                return user_create()

            except IntegrityError as exc:
                # print(f'IntegrityError while user creating: {exc}')
                pass

        return user_create()


class ThreadFactory:

    MAX_TITLE_SIZE = 255
    MAX_TEXT_SIZE = 255

    @classmethod
    def create(cls, forum_id, section_id, author_id):
        return Thread.create(**{
            'title': fake.text(max_nb_chars=cls.MAX_TITLE_SIZE),
            'text': fake.text(max_nb_chars=cls.MAX_TEXT_SIZE),
            'forum': forum_id,
            'section': section_id,
            'author': author_id,
            'created_at': fake.date_time_this_century(before_now=True, after_now=False),
        })
