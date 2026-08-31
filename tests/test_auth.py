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
    
    