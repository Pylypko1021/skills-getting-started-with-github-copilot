from src import app as app_module


def test_signup_then_unregister_same_participant(client):
    # Arrange
    activity_name = "Debate Club"
    email = "flow.student@mergington.edu"

    # Act
    signup_response = client.post(f"/activities/{activity_name}/signup", params={"email": email})
    unregister_response = client.delete(
        f"/activities/{activity_name}/participants", params={"email": email}
    )

    # Assert
    assert signup_response.status_code == 200
    assert unregister_response.status_code == 200
    assert email not in app_module.activities[activity_name]["participants"]


def test_signup_one_activity_does_not_affect_another(client):
    # Arrange
    target_activity = "Art Club"
    untouched_activity = "Science Club"
    email = "isolation.student@mergington.edu"
    before_untouched = list(app_module.activities[untouched_activity]["participants"])

    # Act
    response = client.post(f"/activities/{target_activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert email in app_module.activities[target_activity]["participants"]
    assert app_module.activities[untouched_activity]["participants"] == before_untouched
