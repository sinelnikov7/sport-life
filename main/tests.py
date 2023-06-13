import pytest
# from .serializers import ModuleSerializer

from .models import User

# @pytest.mark.django_db(transaction=True)
@pytest.mark.django_db
# @pytest.mark.transactional_db
def test_register(api_client):

    register_data= {
        "email": "register_test@test.ru",
        "username": "register_test",
        "password": "123"
    }
    response = api_client.post('/register/', data=register_data)
    assert response.status_code == 201
    assert response.data['User']['email'] == "register_test@test.ru"
    assert response.data['User']['username'] == "register_test"


@pytest.mark.django_db
def test_login(api_client):

    valid_login_data = {
        "email": "admin@admin.ru",
        "password": "123"
    }
    assert api_client.post('/token/', data=valid_login_data).status_code == 200
    invalid_login_data = {
        "email": "qqq@vn.ru",
        "password": "123"
    }
    assert api_client.post('/token/', data=invalid_login_data).status_code == 401
    assert User.objects.count() == 1


# @pytest.mark.django_db
# def test_serializer_negative_length_title():
#     data = {"title": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa", "description": "First Module"}
#     serializer = ModuleSerializer(data=data)
#     assert not serializer.is_valid()
#     assert "Ensure this field has no more than 50 characters." in serializer.errors["title"]


