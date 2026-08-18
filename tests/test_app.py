from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_signup_rejects_duplicate_email():
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"

    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert response.status_code == 200

    duplicate_response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert duplicate_response.status_code == 400
    assert "already signed up" in duplicate_response.json()["detail"].lower()

    client.delete(f"/activities/{activity_name}/participants/{email}")


def test_delete_participant_removes_email_from_activity():
    activity_name = "Programming Class"
    email = "remove-me@mergington.edu"

    client.post(f"/activities/{activity_name}/signup?email={email}")

    response = client.delete(f"/activities/{activity_name}/participants/{email}")
    assert response.status_code == 200
    assert email not in client.get("/activities").json()[activity_name]["participants"]
