import requests
from utils.assertion import assertHTTPCode

def test_get_user():
    response = requests.get("https://jsonplaceholder.typicode.com/users/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1
