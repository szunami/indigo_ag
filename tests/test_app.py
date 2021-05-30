from datetime import timedelta
import time
from app.app import app, store_metric, sum

app.window = timedelta(seconds=1)


def test_window():

    client = app.test_client()

    response = client.get('/metric/asdf/sum').get_json()

    assert 'value' in response
    assert response['value'] == 0

    response = client.post('/metric/asdf', json={'value': 10}).get_json()

    assert response == {}

    response = client.get('/metric/asdf/sum').get_json()

    assert 'value' in response
    assert response['value'] == 10

    time.sleep(6)

    response = client.get('/metric/asdf/sum').get_json()

    assert 'value' in response
    assert response['value'] == 0
