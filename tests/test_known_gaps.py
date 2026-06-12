import pytest


@pytest.mark.xfail(
    strict=False,
    reason="Capacity is defined in the model but currently not enforced by the signup endpoint.",
)
def test_signup_should_fail_when_activity_is_at_capacity(client):
    # Arrange
    activity_name = "Chess Club"
    response_before = client.get("/activities")
    activity = response_before.json()[activity_name]
    remaining_slots = activity["max_participants"] - len(activity["participants"])

    for index in range(remaining_slots):
        client.post(
            f"/activities/{activity_name}/signup",
            params={"email": f"fill{index}@mergington.edu"},
        )

    overflow_email = "overflow@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup", params={"email": overflow_email}
    )

    # Assert
    assert response.status_code == 400


@pytest.mark.xfail(
    strict=False,
    reason="Email format is currently not validated by the signup endpoint.",
)
def test_signup_should_reject_invalid_email_format(client):
    # Arrange
    activity_name = "Art Club"
    invalid_email = "invalid-email-format"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup", params={"email": invalid_email}
    )

    # Assert
    assert response.status_code == 422
