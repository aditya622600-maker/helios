from fastapi.testclient import TestClient

from apps.api.main import app

client = TestClient(app)


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_analysis_round_trip(sample_request: dict) -> None:
    created = client.post("/analysis-runs", json=sample_request)
    assert created.status_code == 201
    body = created.json()
    assert body["candidates"][0]["candidate_id"] == "roof-a"
    assert body["candidates"][0]["rank"] == 1

    fetched = client.get(f"/analysis-runs/{body['run_id']}")
    assert fetched.status_code == 200
    assert fetched.json()["run_id"] == body["run_id"]

    geojson = client.get(f"/analysis-runs/{body['run_id']}/candidates.geojson")
    assert geojson.status_code == 200
    assert geojson.json()["type"] == "FeatureCollection"
