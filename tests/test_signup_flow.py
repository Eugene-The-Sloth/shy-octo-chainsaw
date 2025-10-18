import pytest
import requests

BASE = "http://localhost:8001"

@pytest.mark.skipif(True, reason="Run when local server is available")
def test_signup_and_unregister_flow():
    """Outline test: sign up a student then unregister; verify counts update"""
    # This test will require a running server and teacher credentials
    teacher = 'mrodriguez'
    email = 'teststudent@mergington.edu'
    activity = 'Manga Club'

    # Sign up
    resp = requests.post(f"{BASE}/activities/{activity}/signup?email={email}&teacher_username={teacher}")
    assert resp.status_code == 200

    # Unregister
    resp = requests.post(f"{BASE}/activities/{activity}/unregister?email={email}&teacher_username={teacher}")
    assert resp.status_code == 200
