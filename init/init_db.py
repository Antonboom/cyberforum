import datetime
import json
import os
import random

import faker

import settings

from models import (
    User, Forum, Section, Thread, ThreadLabel, ThreadsLabels, Answer,
)
from init.factories import UserFactory, ThreadFactory


USERS_COUNT = 100_000

THREADS_COUNT = 1_000_000
THREAD_LABELS_COUNT = 10_000
MAX_LABELS_FOR_ONE_THREAD = 5

ANSWERS_COUNT = 5_000_000

SET_LAST_ANSWERS_TIME = False
SET_USER_MSG_COUNT = True


fake = faker.Faker()


# Create users
print('Create users...')
current_users_count = User.count()
if current_users_count < USERS_COUNT:
    for i in range(USERS_COUNT - current_users_count):
        if i and (i % 10000 == 0):
            print(f' - Created {i} users')
        UserFactory.create()

# Create forums and sections
admin = User.get(pk_field='username', pk=settings.ADMIN_USERNAME)
if not admin:
    admin = User.create(
        username=settings.ADMIN_USERNAME,
        email=settings.ADMIN_EMAIL,
        password=settings.ADMIN_PASSWORD,
    )

current_dir = os.path.dirname(os.path.abspath(__file__))
forums_data_path = os.path.join(current_dir, 'forum.json')

with open(forums_data_path) as forums_data:
    forums = json.load(forums_data)['forums']

print('Create forums and sections...')
for fdata in forums:
    is_forum_exist = len(Forum.filter(title=fdata['title']))
    if is_forum_exist:
        print(f' - Skip initialization for forum `{fdata["title"]}`')
        continue

    forum = Forum.create(**{
        'title': fdata['title'],
        'created_at': datetime.datetime.now(),
        'created_by': admin.id,
    })

    for section_data in fdata['sections']:
        section = Section.create(**{
            'forum': forum.id,
            'title': section_data['title'],
            'created_at': datetime.datetime.now(),
            'created_by': admin.id,
        })

        for subsection_title in section_data['subsections']:
            Section.create(**{
                'forum': forum.id,
                'parent': section.id,
                'title': subsection_title,
                'created_at': datetime.datetime.now(),
                'created_by': admin.id,
            })

# Create threads
print('Create threads...')
current_threads_count = Thread.count()
if current_threads_count < THREADS_COUNT:
    forums = Forum.all()
    sections = Section.all()
    users = User.all()

    for i in range(THREADS_COUNT - current_threads_count):
        if i and (i % 100000 == 0):
            print(f' - Created {i} threads')

        user = random.choice(users)
        forum = random.choice(forums)
        section = random.choice(sections)

        ThreadFactory.create(
            author_id=user.id,
            forum_id=forum.id,
            section_id=section.id,
        )

# Create thread labels
print('Create thread labels...')
if not ThreadLabel.count():
    labels = set()
    while len(labels) != THREAD_LABELS_COUNT:
        labels.add(' '.join(fake.words(nb=random.randint(0, 3), ext_word_list=None)))

    for label in labels:
        ThreadLabel.create(text=label)

    labels = ThreadLabel.all()

    # TODO(a.telishev): Use cursor iterator
    threads = Thread.all()
    for i, thread in enumerate(threads):
        for label in random.choices(labels, k=random.randint(0, MAX_LABELS_FOR_ONE_THREAD)):
            ThreadsLabels.create(thread=thread.id, label=label.id)

        if i and (i % 20000 == 0):
            print(f' - Processed {i} threads')

# Create answers
print('Create answers...')
current_answers_count = Answer.count()
if current_answers_count < ANSWERS_COUNT:
    threads = Thread.all()
    users = User.all()

    for i in range(ANSWERS_COUNT - current_answers_count):
        thread = None
        user = None

        while True:
            thread = random.choice(threads)
            possible_users = list(filter(
                lambda usr: usr.registered_at and (usr.registered_at > thread.created_at),
                users
            ))

            if not possible_users:
                continue
            else:
                user = random.choice(possible_users)

                # TODO(a.telishev): Factory
                Answer.create(
                    text=fake.text(max_nb_chars=1024),
                    thread=thread.id,
                    author=user.id,
                    created_at=fake.date_between_dates(date_start=thread.created_at),
                    rating=random.randint(-100, 100),
                    is_off_topic=random.randint(0, 100) < 10,
                )
                break

        if i and (i % 20000) == 0:
            print(f' - Created {i} answers')

# Set last answer time for threads
if SET_LAST_ANSWERS_TIME:
    print('Set last answers times for threads')

    for i, thread in enumerate(Thread.all()):
        thread.set_last_answer_time()

        if i and (i % 20000 == 0):
            print(f' - Processed {i} threads')

if SET_USER_MSG_COUNT:
    print('Set user messages count')

    for i, user in enumerate(User.all()):
        user.msg_count = len(Answer.filter(author=user.id))
        user.save()

        if i and (i % 20000 == 0):
            print(f' - Processed {i} users')

print('Complete')
