import pytest
import requests
from pytest_mock import mocker


# from .serializers import ModuleSerializer

from .models import User, ConfirmCode


# def send_email():
#     print('Письмо ушло')

# def test_mock(mocker):
#     mocker.patch('main.tasks.send_confirm_email', return_value=1)


# @pytest.mark.django_db(transaction=True)
@pytest.mark.django_db
# @pytest.mark.parametrize
# @pytest.mark.transactional_db
def test_register_unique(api_client, mocker):
    """Регистрация с уникальными кредами"""
    # mocker.patch('main.tasks.send_confirm_email', return_value=1, side_effect=send_email())
    mocker.patch('main.tasks.send_confirm_email', return_value=None)

    register_data = {
        "email": "tsoftin@gmail.com",
        "username": "register_test",
        "password": "123"
    }
    response = api_client.post('/api/auth/register/', data=register_data)
    assert response.status_code == 201
    assert response.data['User']['email'] == "tsoftin@gmail.com"
    assert response.data['User']['username'] == "register_test"


@pytest.mark.django_db
def test_register_not_unique(api_client):
    """Регистрация с не уникальными кредами"""
    register_data = {
        "email": "admin@admin.ru",
        "username": "admin",
        "password": "123"
    }
    response = api_client.post('/api/auth/register/', data=register_data)
    assert response.data == {
        "errors": {
            "email": ["Пользователь с таким email уже зарегестрирован"],
            "username": ["Пользователь с таким username уже зарегестрирован"]
        }
    }


@pytest.mark.django_db
def test_valid_login(api_client):
    """Авторизация с валидными данными"""
    valid_login_data = {
        "email": "admin@admin.ru",
        "password": "123"
    }
    assert api_client.post('/api/auth/token/', data=valid_login_data).status_code == 200


@pytest.mark.django_db
def test_invalid_login(api_client):
    """Авторизация с не валидным логином"""
    invalid_login_data = {
        "email": "qqq@vn.ru",
        "password": "123"
    }
    assert api_client.post('/api/auth/token/', data=invalid_login_data).status_code == 401

@pytest.mark.django_db
def test_invalid_password(api_client):
    """Авторизация с не валидным паролем"""
    invalid_login_data = {
        "email": "admin@admin.ru",
        "password": "1234"
    }
    assert api_client.post('/api/auth/token/', data=invalid_login_data).status_code == 401

@pytest.mark.django_db
def test_approve(api_client):
    """Активация юзера"""
    key = 1234
    a = ConfirmCode(user_id=1, key=key)
    a.save()
    valid_login_data = {
        "email": "admin@admin.ru",
        "password": "123"
    }
    token = api_client.post('/api/auth/token/', data=valid_login_data).data['access']
    assert api_client.post('/api/auth/approve/', data={"key": key},
                           headers={'Authorization': f'access {token}'}).data == {'success': True}
    assert api_client.post('/api/auth/approve/', data={"key": 1},
                           headers={'Authorization': f'access {token}'}).data == {"success": False,
                                                                                  "message": "Неверный пароль"}


@pytest.mark.django_db
def test_get_user_profile(api_client, token):
    """Получение профиля юзера"""
    response = {'status': 200, 'user': {'id': 1, 'is_approve': False, 'username': 'admin', 'email': 'admin@admin.ru',
                                        'first_name': '', 'last_name': '', 'is_coach': False, 'date_of_birth': None,
                                        'height': None, 'weight': None, 'avatar': None}}
    assert api_client.get('/api/profile/', headers={'Authorization': f'access {token}'}).data == response


@pytest.mark.django_db
def test_update_user_profile(api_client, token):
    """Обновление профиля юзера"""

    fields = {
        "first_name": "Владимиров!!!!!!!!",
        "last_name": "Синельникbhg",
        "date_of_birth": "1988-01-09",
        "height": "0.4",
        "weight": "0.4",
    }
    response = {'id': 1,
                'is_approve': False,
                'username': 'admin',
                'email': 'admin@admin.ru',
                'first_name': 'Владимиров!!!!!!!!',
                'last_name': 'Синельникbhg',
                'is_coach': False,
                'date_of_birth': '1988-01-09',
                'height': '0.4',
                'weight': '0.4',
                'avatar': None, 'age': 35}
    assert api_client.patch('/api/profile/update/', data=fields, headers={'Authorization': f'access {token}'}).json() == response

