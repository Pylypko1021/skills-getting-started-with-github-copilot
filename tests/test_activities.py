def test_get_activities_returns_all_activities(client):
    # Arrange
    expected_minimum_activities = 1

    # Act
    response = client.get("/activities")
    payload = response.json()

    # Assert
    assert response.status_code == 200
    assert isinstance(payload, dict)
    assert len(payload) >= expected_minimum_activities


def test_get_activities_has_required_fields(client):
    # Arrange
    required_fields = {"description", "schedule", "max_participants", "participants"}

    # Act
    response = client.get("/activities")
    payload = response.json()

    # Assert
    assert response.status_code == 200
    for details in payload.values():
        assert required_fields.issubset(details.keys())


def test_get_activities_participant_lists_are_consistent(client):
    # Arrange
    response = client.get("/activities")

    # Act
    payload = response.json()

    # Assert
    for details in payload.values():
        participants = details["participants"]
        assert isinstance(participants, list)
        assert all(isinstance(email, str) for email in participants)
