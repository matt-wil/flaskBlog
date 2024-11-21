import pytest
from flaskBlog.app import *


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_index_route(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Welcome to My Flask Blog!' in response.data


def test_add_route(client):
    response = client.post('/add', data={
        'id': '1',
        'title': 'Test Post',
        'author': 'Test Author',
        'content': 'This is a Test'
    })
    assert response.status_code == 302


def test_delete_route(client):
    mock_post = {
        'id': '1',
        'title': 'Test Post',
        'author': 'Test Author',
        'content': 'This is a Test'
    }
    with open('data.json', 'w') as f:
        import json
        json.dump([mock_post], f)

    response = client.post('/delete/1')
    assert response.status_code == 302

    with open('data.json', 'r') as f:
        data = json.load(f)
        assert len(data) == 0


def test_update_route(client):
    pass


def test_like_route(client):
    pass


def test_dislike_route(client):
    pass




