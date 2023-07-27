import pytest
from pytest_mock import mocker

# from .serializers import ModuleSerializer

from .models import User, ConfirmCode

def qqq():
    print('qqq')
def test_mock(mocker):
    mocker.patch('main.tasks.send_confirm_email', return_value=1)


# @pytest.mark.django_db(transaction=True)
@pytest.mark.django_db
# @pytest.mark.parametrize
# @pytest.mark.transactional_db
def test_register(api_client, mocker):
    mocker.patch('main.tasks.send_confirm_email', return_value=1, side_effect=qqq())

    register_data= {
        "email": "tsoftin@gmail.com",
        "username": "register_test",
        "password": "123"
    }
    response = api_client.post('/api/auth/register/', data=register_data)
    assert response.status_code == 201
    assert response.data['User']['email'] == "tsoftin@gmail.com"
    assert response.data['User']['username'] == "register_test"

@pytest.mark.django_db
def test_login(api_client):

    valid_login_data = {
        "email": "admin@admin.ru",
        "password": "123"
    }
    assert api_client.post('/api/auth/token/', data=valid_login_data).status_code == 200
    invalid_login_data = {
        "email": "qqq@vn.ru",
        "password": "123"
    }
    assert api_client.post('/api/auth/token/', data=invalid_login_data).status_code == 401
    assert User.objects.count() == 1
@pytest.mark.django_db
def test_approve(api_client):
    key = 1234
    a = ConfirmCode(user_id=1, key=key)
    a.save()
    valid_login_data = {
        "email": "admin@admin.ru",
        "password": "123"
    }
    token = api_client.post('/api/auth/token/', data=valid_login_data).data['access']
    assert api_client.post('/api/auth/approve/', data={"key": key}, headers={'Authorization': f'access {token}'}).data == {'success': True}
    assert api_client.post('/api/auth/approve/', data={"key": 1}, headers={'Authorization': f'access {token}'}).data == {"success": False, "message": "Неверный пароль"}



# @pytest.mark.django_db
# def test_serializer_negative_length_title():
#     data = {"title": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa", "description": "First Module"}
#     serializer = ModuleSerializer(data=data)
#     assert not serializer.is_valid()
#     assert "Ensure this field has no more than 50 characters." in serializer.errors["title"]


