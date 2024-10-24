from starlette.testclient import TestClient

import sys
import os

# Add the project's root directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from app import create_app

app = create_app()

client = TestClient(app)

def test_get_students():
    response = client.get("/api/students")
    print(dir(response))
    print(response.status_code)
    print(response.text)
    assert response.status_code == 200

test_get_students()