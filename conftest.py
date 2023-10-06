from rest_framework.test import APIClient
import pytest
from django.db import connections, transaction
# from unittest.mock import Mock

from main.models import User, ConfirmCode
from notes.models import Note


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
        with transaction.atomic():
            user = User(email='admin@admin.ru', username='admin')
            user.set_password('123')
            user.save()
            pass
        with transaction.atomic():
            note = Note(text='Hello world', user_id=1)
            note.save()
            note = Note(text='Second', user_id=1)
            note.save()
            pass
        yield

# @pytest.fixture(scope='session')
# def django_db(transactional_db):
#     pass


