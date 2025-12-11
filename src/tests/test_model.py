import joblib
from pathlib import Path
from src.models.model_loader import load_model

def test_load_model(tmp_path):
    model_path = tmp_path / "dummy.pkl"
    joblib.dump({"a": 1}, model_path)

    model = load_model(model_path)
    assert model["a"] == 1
