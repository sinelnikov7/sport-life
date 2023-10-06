import pytest

from .models import Note


@pytest.mark.django_db
def test_create_note(api_client, token):
    """Создание заметки"""
    data = {"text": "First"}
    response = api_client.post('/api/note/', data=data, headers={'Authorization': f'access {token}'})
    assert response.status_code == 201
    assert response.data.get('text') == 'First'

@pytest.mark.django_db
def test_get_note_list(api_client, token):
    """Получение списка заметок"""
    response = api_client.get('/api/note/', headers={'Authorization': f'access {token}'})
    assert response.status_code == 200
    assert response.json().get('results')[0].get('text') == 'Hello world'

@pytest.mark.django_db
def test_note_update(api_client, token):
    """Обновление заметки"""
    data = {"text": "First"}
    response = api_client.patch('/api/note/1/', data=data, headers={'Authorization': f'access {token}'})
    assert response.status_code == 200
    assert response.json().get('text') == 'First'

@pytest.mark.django_db
def test_note_delete(api_client, token):
    """Удаление заметки"""
    response = api_client.delete('/api/note/1/', headers={'Authorization': f'access {token}'})
    assert response.status_code == 200
    assert response.json() == {"success": True}

@pytest.mark.django_db
def test_filter_notes(api_client, token):
    """Фильтрация заметок"""
    response = api_client.get('/api/note/?text=Rld', headers={'Authorization': f'access {token}'}).json()
    assert response.get('results')[0].get('text') == 'Hello world'

@pytest.mark.django_db
def test_order_notes(api_client, token):
    """Сортировка заметок по времени создания"""
    response = api_client.get('/api/note/?ordering=-time_create', headers={'Authorization': f'access {token}'}).json()
    assert response.get('results')[0].get('text') == 'Second'
    assert response.get('results')[1].get('text') == 'Hello world'
    response = api_client.get('/api/note/?ordering=time_create', headers={'Authorization': f'access {token}'}).json()
    assert response.get('results')[0].get('text') == 'Hello world'
    assert response.get('results')[1].get('text') == 'Second'
