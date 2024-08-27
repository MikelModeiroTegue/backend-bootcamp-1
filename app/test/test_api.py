from starlette.testclient import TestClient

from app import create_app

app = create_app()

client = TestClient(app)

def test_get_students():
    response = client.get("api/students")
    print(dir(response))
    assert response.status_code == 200

test_get_students()