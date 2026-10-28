import pytest
from fastapi.testclient import TestClient
from app.api.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["deterministic_mode"] == True

def test_dashboard():
    response = client.get("/dashboard")
    assert response.status_code == 200
    data = response.json()
    assert "total_runs" in data
    assert "metrics_computed" in data
    assert "note" in data

def test_create_and_get_run():
    response = client.post("/runs", json={
        "dataset_version": "v1",
        "configs": [{"name": "baseline", "model_name": "llama2", "use_rag": False}]
    })
    assert response.status_code == 200
    data = response.json()
    assert "run_id" in data
    run_id = data["run_id"]
    
    response2 = client.get(f"/runs/{run_id}")
    assert response2.status_code == 200
    data2 = response2.json()
    assert "run" in data2
    assert "results" in data2
    assert len(data2["results"]) == 3
