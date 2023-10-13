import pytest

from .models import Task


@pytest.mark.django_db
def test_create_task(api_client, token):
    """Создание задачи"""
    data = {"date": "2023-06-28",
            "time": "21:23:00",
            "title": "Погладить кота",
            "status_id": 1,
            "priority_id": 2
            }
    response = api_client.post('/api/task/', data=data, headers={'Authorization': f'access {token}'})
    assert response.status_code == 201
    assert response.data.get('title') == 'Погладить кота'

@pytest.mark.django_db
def test_get_task_list(api_client, token):
    """Получение списка задач"""
    response = api_client.get('/api/task/', headers={'Authorization': f'access {token}'})
    assert response.status_code == 200
    assert response.json().get('results')[0].get('title') == 'Feed the cat'
    assert response.json().get('results')[1].get('title') == 'Feed the dog'

@pytest.mark.django_db
def test_task_update(api_client, token):
    """Обновление задачи"""
    data = {"title": "OK"}
    response = api_client.patch('/api/task/1/', data=data, headers={'Authorization': f'access {token}'})
    assert response.status_code == 200
    assert response.json().get('title') == 'OK'
#
@pytest.mark.django_db
def test_task_delete(api_client, token):
    """Удаление задачи"""
    response = api_client.delete('/api/task/1/', headers={'Authorization': f'access {token}'})
    assert response.status_code == 200
    assert response.json() == {"success": True}

@pytest.mark.django_db
def test_filter_task(api_client, token):
    """Фильтрация задач"""
    response = api_client.get('/api/task/?title=Dog', headers={'Authorization': f'access {token}'}).json()
    assert response.get('results')[0].get('title') == 'Feed the dog'
#
@pytest.mark.django_db
def test_order_task_date(api_client, token):
    """Сортировка задач по дате"""
    response = api_client.get('/api/task/?ordering=date', headers={'Authorization': f'access {token}'}).json()
    assert response.get('results')[0].get('title') == 'Feed the cat'
    assert response.get('results')[1].get('title') == 'Feed the dog'
    response = api_client.get('/api/task/?ordering=-date', headers={'Authorization': f'access {token}'}).json()
    assert response.get('results')[0].get('title') == 'Feed the dog'
    assert response.get('results')[1].get('title') == 'Feed the cat'

@pytest.mark.django_db
def test_order_task_time(api_client, token):
    """Сортировка задач по времени"""
    response = api_client.get('/api/task/?ordering=time', headers={'Authorization': f'access {token}'}).json()
    assert response.get('results')[0].get('title') == 'Feed the cat'
    assert response.get('results')[1].get('title') == 'Feed the dog'
    response = api_client.get('/api/task/?ordering=-time', headers={'Authorization': f'access {token}'}).json()
    assert response.get('results')[0].get('title') == 'Feed the dog'
    assert response.get('results')[1].get('title') == 'Feed the cat'