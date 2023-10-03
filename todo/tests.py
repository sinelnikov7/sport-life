# import pytest
#
# @pytest.mark.django_db
# def test_create_note(api_client, token):
#     """Создание заметки"""
#     data = {"text": "First"}
#     response = api_client.post('/api/note/', data=data, headers={'Authorization': f'access {token}'})
#     assert response.status_code == 201
#     assert response.data.get('text') == 'First'