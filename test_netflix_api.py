from fastapi.testclient import TestClient

from netflix_api import app

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "msg": "Hello! Please refer to /docs page for documentations!"}
    
def test_pagination():
    response = client.get("/search")
    assert response.status_code == 200
    assert response.json(
    )[-1] == {"next": "http://testserver/search?page=2"}

def test_sort_desc():
    response = client.get("/search?sort_by=show_id&sort_order=desc")
    assert response.status_code == 200
    data = response.json()
    if len(data) > 1:
        assert data[0]['show_id'] > data[1]['show_id']

def test_sort_asc():
    response = client.get("/search?sort_by=show_id&sort_order=asc")
    assert response.status_code == 200
    data = response.json()
    if len(data) > 1:
        assert data[0]['show_id'] < data[1]['show_id']

def test_limit():
    pass

# search filter: show_id
def test_search_filter1():
    pass

def test_create():
    pass

def test_update():
    pass

def test_delete():
    pass


