from dotenv import load_dotenv
import os
from fastapi.testclient import TestClient
from netflix_api import app

client = TestClient(app)
load_dotenv()


def test_read_main():
    response = client.get("/", auth=(os.environ['API_USERNAME'], os.environ['API_PASSWORD']))
    assert response.status_code == 200
    assert response.json() == {
        "msg": "Hello! Please refer to /docs page for documentations!"}
    
def test_pagination():
    response = client.get("/search", auth=(os.environ['API_USERNAME'], os.environ['API_PASSWORD']))
    assert response.status_code == 200
    assert response.json(
    )[-1] == {"next": "http://testserver/search?page=2"}

def test_sort_desc():
    response = client.get("/search?sort_by=show_id&sort_order=desc",
                          auth=(os.environ['API_USERNAME'], os.environ['API_PASSWORD']))
    assert response.status_code == 200
    data = response.json()
    if len(data) > 1:
        assert data[2]['show_id'] > data[3]['show_id']

def test_sort_asc():
    response = client.get("/search?sort_by=show_id&sort_order=asc",
                          auth=(os.environ['API_USERNAME'], os.environ['API_PASSWORD']))
    assert response.status_code == 200
    data = response.json()
    if len(data) > 1:
        assert data[0]['show_id'] < data[1]['show_id']

# search filter: show_id
def test_search_filter1():
    response = client.get("/search?show_id=10",
                          auth=(os.environ['API_USERNAME'], os.environ['API_PASSWORD']))
    assert response.status_code == 200
    data = response.json()
    assert data[0]['show_id'] == 10


