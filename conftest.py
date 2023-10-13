from rest_framework.test import APIClient
import pytest
from django.db import connections, transaction
# from unittest.mock import Mock

from main.models import User, ConfirmCode
from notes.models import Note
from todo.models import Task, Status, Priority


@pytest.fixture#(scope='session')
def api_client():
    return APIClient()

@pytest.fixture#(scope='session')
def token():
    valid_login_data = {
        "email": "admin@admin.ru",
        "password": "123"
    }
    token = APIClient().post('/api/auth/token/', data=valid_login_data).data['access']
    return token


@pytest.fixture(scope='session')
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        """Создание юзера"""
        with transaction.atomic():
            user = User(email='admin@admin.ru', username='admin')
            user.set_password('123')
            user.save()
            pass
        with transaction.atomic():
            """Создание заметки"""
            note_1 = Note(text='Hello world', user_id=1)
            note_1.save()
            note_2 = Note(text='Second', user_id=1)
            note_2.save()
            pass
        with transaction.atomic():
            """Создание задачи"""
            task_1 = Task(user_id=1, date='2023-06-27',
                        time="21:23:00",
                        title='Feed the cat',
                        status=Status.objects.create(title="First status"),
                        priority=Priority.objects.create(title="First priority"))
            task_1.save()
            task_2 = Task(user_id=1, date='2023-06-28',
                         time="21:24:00",
                         title='Feed the dog',
                         status=Status.objects.create(title="Second status"),
                         priority=Priority.objects.create(title="Second priority"))
            task_2.save()
            pass
        yield

# @pytest.fixture(scope='session')
# def django_db(transactional_db):
#     pass


