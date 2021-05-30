from datetime import timedelta
import time
import app.main

app.main.window = timedelta(seconds=1)


def test_window():

    client = app.main.app.test_client()

    response = client.get('/metric/asdf/sum').get_json()

    assert 'value' in response
    assert response['value'] == 0

    response = client.post('/metric/asdf', json={'value': 10}).get_json()

    assert response == {}

    response = client.get('/metric/asdf/sum').get_json()

    assert 'value' in response
    assert response['value'] == 10

    time.sleep(2)

    response = client.get('/metric/asdf/sum').get_json()

    assert 'value' in response
    assert response['value'] == 0


def test_purge():
    client = app.main.app.test_client()

    client.post('/metric/asdf', json={'value': 10}).get_json()
    client.post('/metric/asdf', json={'value': 10}).get_json()
    time.sleep(0.5)
    client.post('/metric/asdf', json={'value': 10}).get_json()
    response = client.get('/metric/asdf/sum').get_json()
    assert response['value'] == 30
    time.sleep(0.6)
    
    response = client.get('/metric/asdf/sum').get_json()
    assert response['value'] == 10

    time.sleep(0.5)
    response = client.get('/metric/asdf/sum').get_json()
    assert response['value'] == 0
