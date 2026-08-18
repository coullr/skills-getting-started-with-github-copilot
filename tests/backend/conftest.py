from copy import deepcopy

import pytest
from fastapi.testclient import TestClient

from src.app import activities, app


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture(autouse=True)
def restore_activity_participants():
    original_activities = deepcopy(activities)

    yield

    for activity_name, activity in original_activities.items():
        activities[activity_name]["participants"] = activity["participants"]