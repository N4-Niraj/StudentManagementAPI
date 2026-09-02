def test_register_user(client):
    response = client.post(
            "/auth/register",
            json={
                "email": "hello2@gmail.com",
                "password": "password123"
            }
        )
    
    
    
    assert response.status_code == 200
    assert response.json()["email"] == "hello2@gmail.com"
    assert "password" not in response.json()
    assert "password_hash" not in response.json()
    


def test_register_duplicate_email(client):
    data = {
        "email": "duplicate@example.com",
        "password": "password123"
    }

    first_response = client.post(
        "/auth/register",
        json=data
    )

    second_response = client.post(
        "/auth/register",
        json=data
    )

    assert first_response.status_code == 200
    assert second_response.status_code == 409
    
    