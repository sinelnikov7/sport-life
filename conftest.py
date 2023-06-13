
from rest_framework.test import APIClient
import pytest
from django.db import connections, transaction

from main.models import User, ConfirmCode


@pytest.fixture(scope='session')
def api_client():
    return APIClient()


@pytest.fixture(scope='session')
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        with transaction.atomic():
            # Выполните все миграции и/или загрузку начальных данных, если это необходимо
            user = User(email='admin@admin.ru', username='admin')
            user.set_password('123')
            user.save()
            pass

        yield

# @pytest.fixture(scope='session')
# def django_db(transactional_db):
#     pass


