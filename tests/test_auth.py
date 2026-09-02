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
    
    
def test_login_success(client):
    client.post(
        "/auth/register",
        json={
            "email":"login11@gmail.com",
            "password":"password2231"
        }
    )
    response = client.post(
        "/auth/login",
        data={
            "username": "login11@gmail.com",  #username instead of email cz OAuth2PasswordRequestForm expects username and password
            "password": "password2231"
            
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    
def test_login_wrongPassword(client):
    
    client.post(
        "/auth/register",
        json={
            "email":"testwrong@gmail.com",
            "password":"password123123"
        }
    )
    
    response = client.post(
        "/auth/login",
        data={
            "username":"testwrong@gmail.com",
            "password":"wronggg"
        }
    )
    
    assert response.status_code == 401

def test_login_unknownUser(client):
    
    response = client.post(
        "/auth/login",
        data={
            "username": "unknown@gmail.com",
            "password": "password"
        }
    )
    
    assert response.status_code == 401
    
def test_getme_authenticated(client):
    
    client.post(
        "/auth/register",
        json={
            "email":"testauthenticated@gmail.com",
            "password":"password123123"
        }
    )
    
    response = client.post(
        "/auth/login",
        data={
            "username":"testauthenticated@gmail.com",
            "password":"password123123"
        }
    )
    
    assert response.status_code == 200
    
    token = response.json()["access_token"]
    
    response = client.get(
        "/users/me",
        headers={
            "Authorization": (f"bearer {token}")
        }
    )
    
    assert response.status_code == 200
    assert response.json()["email"] == "testauthenticated@gmail.com"
    

def test_get_me_unauthenticated(client):
    response = client.get("/users/me")

    assert response.status_code == 401
