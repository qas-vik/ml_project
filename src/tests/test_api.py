from fastapi.testclient import TestClient
from src.api.app import app
from src.utils.validation import validate_row_count


client = TestClient(app)

def test_root():
    r = client.get("/")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"

def test_predict():
    r = client.post("/predict", json={"name": "abc", "value": 5})
    assert r.status_code == 200
    assert r.json()["result"] == 10
