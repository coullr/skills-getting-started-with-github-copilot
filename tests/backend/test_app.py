from urllib.parse import quote


def test_root_redirects_to_static_index(client):
    # Arrange
    expected_location = "/static/index.html"

    # Act
    response = client.get("/", follow_redirects=False)

    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == expected_location


def test_get_activities_returns_activity_details(client):
    # Arrange
    expected_activity = "Chess Club"

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    assert expected_activity in response.json()
    assert "participants" in response.json()[expected_activity]


def test_signup_adds_new_participant(client):
    # Arrange
    activity_name = "Basketball Team"
    email = "newstudent@mergington.edu"
    endpoint = f"/activities/{quote(activity_name)}/signup"

    # Act
    response = client.post(endpoint, params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json() == {
        "message": f"Signed up {email} for {activity_name}"
    }
    assert email in client.get("/activities").json()[activity_name]["participants"]


def test_signup_rejects_unknown_activity(client):
    # Arrange
    activity_name = "Unknown Club"
    endpoint = f"/activities/{quote(activity_name)}/signup"

    # Act
    response = client.post(endpoint, params={"email": "student@mergington.edu"})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_rejects_duplicate_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"
    endpoint = f"/activities/{quote(activity_name)}/signup"
    client.post(endpoint, params={"email": email})

    # Act
    response = client.post(endpoint, params={"email": email})

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_unregister_removes_participant(client):
    # Arrange
    activity_name = "Programming Class"
    email = "remove-me@mergington.edu"
    signup_endpoint = f"/activities/{quote(activity_name)}/signup"
    unregister_endpoint = (
        f"/activities/{quote(activity_name)}/participants/{quote(email)}"
    )
    client.post(signup_endpoint, params={"email": email})

    # Act
    response = client.delete(unregister_endpoint)

    # Assert
    assert response.status_code == 200
    assert response.json() == {
        "message": f"Removed {email} from {activity_name}"
    }
    assert email not in client.get("/activities").json()[activity_name]["participants"]


def test_unregister_rejects_unknown_activity(client):
    # Arrange
    activity_name = "Unknown Club"
    email = "student@mergington.edu"
    endpoint = (
        f"/activities/{quote(activity_name)}/participants/{quote(email)}"
    )

    # Act
    response = client.delete(endpoint)

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_rejects_missing_participant(client):
    # Arrange
    activity_name = "Art Club"
    email = "missing@mergington.edu"
    endpoint = f"/activities/{quote(activity_name)}/participants/{quote(email)}"

    # Act
    response = client.delete(endpoint)

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found in this activity"