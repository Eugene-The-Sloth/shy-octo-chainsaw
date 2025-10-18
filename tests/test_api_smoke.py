import requests
import pytest

BASE = "http://localhost:8001"

@pytest.mark.skipif(True, reason="Run when local server is available")
def test_get_activities_smoke():
    """Smoke test: GET /activities returns 200 and JSON mapping"""
    resp = requests.get(f"{BASE}/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    # Expect Manga Club to be present
    assert "Manga Club" in data
