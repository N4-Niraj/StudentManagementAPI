
from app.security import hash_password


def test_user_cantCreate_student(client):
    
    client.post(
        "/auth/register",
        json={
            "email":"normaluser@gmail.com",
            "password":"normal123"
        }
    )
    
    login_response = client.post(
        "/auth/login",
        data={
            "username":"normaluser@gmail.com",
            "password":"normal123"
        }
    )
    
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    
    response = client.post(
        "/students",
        headers={
            "Authorization": (f"Bearer {token}")
        },
        json = {
            "name":"bruhhh",
            "faculty":"civil",
            "semester": 2,
            "email":"bruhhh@gmail.com"
        }
    )
    
    assert response.status_code == 403
    
    
def test_admin_can_create_student(client, admin_user):
    login_response = client.post(
        "/auth/login",
        data={
            "username": admin_user.email,
            "password": "admin123"
        }
    )
    
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
        
    response = client.post(
        "/students",
        headers={
            "Authorization": (f"Bearer {token}")
        },
        json = {
            "name":"bruhhh",
            "faculty":"civil",
            "semester": 2,
            "email":"bruhhh@gmail.com"
        }
    )
        
    assert response.status_code == 200
    
    
#to check so that normal user can't delete student's data

def test_user_cant_delete_student(client, admin_user):
    
    login_response = client.post(
        "/auth/login",
        data={
            "username": admin_user.email,
            "password":"admin123"
        }
    )
    
    assert login_response.status_code == 200
    
    token = login_response.json()["access_token"]
    
    student_response = client.post(
        "/students",
        headers = {
            "Authorization" : (f"Bearer {token}")
        },
        
        json = {
            "name": "delete test",
            "faculty": "BCA",
            "semester" : 2,
            "email" : "delete_test@gmail.com"
        }
    )
    
    assert student_response.status_code == 200
    
    student_id = student_response.json()["id"]
    
    #register as normal user
    
    client.post(
        "/auth/register",
        json={
            "email":"normaluser@gmail.com",
            "password":"normal123"
        }
    )
    
    user_login = client.post(
        "/auth/login",
        data={
            "username":"normaluser@gmail.com",
            "password":"normal123"
        }
    )
    
    normalUser_token = user_login.json()["access_token"]
    assert user_login.status_code == 200
    
    #normal user tries to delete student..
    response = client.delete(
        f"/students/{student_id}",
        headers={
            "Authorization": (f"Bearer {normalUser_token}")
        }
    )
    
    assert response.status_code == 403
    
# to check : admin can delete students
def test_admin_can_delete_student(client, admin_user):
    login_response = client.post(
        "/auth/login",
        data={
            "username": admin_user.email,
            "password":"admin123"
        }
    )
    
    assert login_response.status_code == 200
    
    admin_token = login_response.json()["access_token"]
    
    student_response = client.post(
        "/students",
        headers={
            "Authorization": (f"Bearer {admin_token}")
        },
        json={
            "name": "delete test2",
            "faculty": "BCA",
            "semester" : 2,
            "email" : "delete_test2@gmail.com"
        }
    )
    
    student_id = student_response.json()["id"]
    
    response = client.delete(
        f"/students/{student_id}",
        headers={
            "Authorization": (f"Bearer {admin_token}")
        }
    )
        
    assert response.status_code == 200
    assert response.json()["message"] == "Student deleted successfully"

def test_get_student(client, admin_user):
    login_response = client.post(
        "/auth/login",
        data={
            "username":admin_user.email,
            "password":"admin123"
        }
    )
    
    assert login_response.status_code == 200
    
    token = login_response.json()["access_token"]
    
    client.post(
        "/students",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "name":"Student one",
            "faculty":"BCA",
            "semester": 2,
            "email":"student1@gmail.com"
        }
    )
    client.post(
            "/students",
            headers={
                "Authorization": f"Bearer {token}"
            },
            json={
                "name":"Student two",
                "faculty":"BCA",
                "semester": 3,
                "email":"student2@gmail.com"
            }
        )
    response = client.get("/students" ,
                          headers={
                              "Authorization": f"Bearer {token}"
                          })
    
    assert response.status_code == 200
    
    students = response.json()
    assert len(students) == 2