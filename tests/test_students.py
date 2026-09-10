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
    
    
def test_admin_can_create_student(client, admin_token):
    response = client.post(
        "/students",
        headers={
            "Authorization": (f"Bearer {admin_token}")
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

def test_user_cant_delete_student(client, admin_token):
    student_response = client.post(
        "/students",
        headers = {
            "Authorization" : (f"Bearer {admin_token}")
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
    
    normal_user_token = user_login.json()["access_token"]
    assert user_login.status_code == 200
    
    #normal user tries to delete student..
    response = client.delete(
        f"/students/{student_id}",
        headers={
            "Authorization": (f"Bearer {normal_user_token}")
        }
    )
    
    assert response.status_code == 403
    
# to check : admin can delete students
def test_admin_can_delete_student(client, admin_token):
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

def test_get_students(client, admin_token):
    client.post(
        "/students",
        headers={
            "Authorization": f"Bearer {admin_token}"
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
                "Authorization": f"Bearer {admin_token}"
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
                              "Authorization": f"Bearer {admin_token}"
                          })
    
    assert response.status_code == 200
    
    students = response.json()
    assert len(students) == 2
    

def test_get_student(client, admin_token):
    student_response = client.post(
            "/students",
            headers={
                "Authorization": f"Bearer {admin_token}"
            },
            json={
                "name":"studentt",
                "faculty":"BCA",
                "semester": 3,
                "email":"studenttt@gmail.com"
            }
        )
    
    assert student_response.status_code == 200
    
    student_id = student_response.json()["id"]
    
    response = client.get(f"/students/{student_id}" ,
                          headers={
                              "Authorization": f"Bearer {admin_token}"
                          })
    
    assert response.status_code == 200
    
    student = response.json()
    
    assert student["name"] == "studentt"
    assert student["email"] == "studenttt@gmail.com"
    
def test_patch_student(client, admin_token):
    student_response = client.post(
            "/students",
            headers={
                "Authorization": f"Bearer {admin_token}"
            },
            json={
                "name":"oldname",
                "faculty":"BCA",
                "semester": 2,
                "email":"oldname@gmail.com"
            }
        )
    
    assert student_response.status_code == 200
    
    student_id = student_response.json()["id"]
    
    patch_response = client.patch(
        f"/students/{student_id}",
        headers={
          "Authorization": f"Bearer {admin_token}"
        },
        json={
            "name": "New Name",
            "semester": 4
     })
    
    assert patch_response.status_code == 200
    
    response = client.get(f"/students/{student_id}" ,
                          headers={
                              "Authorization": f"Bearer {admin_token}"
                          })
    
    assert response.status_code == 200
    
    student = response.json()
    
    assert student["faculty"] == "BCA"
    assert student["email"] == "oldname@gmail.com"
    
    assert student["name"] == "New Name"
    assert student["semester"] == 4
    
    
def test_delete_student(client, admin_token):
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
    
    assert student_response.status_code == 200
    
    student_id = student_response.json()["id"]
    
    delete_response = client.delete(
        f"/students/{student_id}",
        headers={
            "Authorization": (f"Bearer {admin_token}")
        }
    )
    
    assert delete_response.status_code == 200
    assert delete_response.json()["message"] == "Student deleted successfully"
        
    get_response = client.get(
        f"/students/{student_id}",
            headers={
                "Authorization": f"Bearer {admin_token}"
        })

    assert get_response.status_code == 404
        
    
    
def test_get_nonexistent_student(client, admin_token):
    response = client.get(
    "/students/999999",
    headers={
        "Authorization": f"Bearer {admin_token}"
    })
    
    assert response.status_code == 404
    assert response.json()["detail"] == "Student not found"
    
    
def test_duplicate_student_email(client, admin_token):
    student1_response = client.post(
            "/students",
            headers={
                "Authorization": f"Bearer {admin_token}"
            },
            json={
                
                    "name": "Student One",
                    "faculty": "BCA",
                    "semester": 2,
                    "email": "duplicate@gmail.com"
                
            }
        )
    
    assert student1_response.status_code == 200

    student2_response = client.post(
                "/students",
                headers={
                    "Authorization": f"Bearer {admin_token}"
                },
                json={
                    
                        "name": "Student two",
                        "faculty": "BCA",
                        "semester": 2,
                        "email": "duplicate@gmail.com"
                    
                }
            )
        
    assert student2_response.status_code == 409 
        
    
        
    
    

def test_create_student_missing_field(client, admin_token):
    student1_response = client.post(
                "/students",
                headers={
                    "Authorization": f"Bearer {admin_token}"
                },
                json={
                    
                        "name": "Student One",
                        "faculty": "BCA",
                        "semester": 2
                        
                    
                }
            )
        
    assert student1_response.status_code == 422
    
def test_create_student_invalid_email(client, admin_token):
    student1_response = client.post(
                "/students",
                headers={
                    "Authorization": f"Bearer {admin_token}"
                },
                json={
                    
                        "name": "Student One",
                        "faculty": "BCA",
                        "semester": 2,
                        "email": "this_is_not_email"
                        
                    
                }
            )
        
    assert student1_response.status_code == 422

def test_create_student_invalid_semester(client, admin_token):
    student1_response = client.post(
                "/students",
                headers={
                    "Authorization": f"Bearer {admin_token}"
                },
                json={
                    
                        "name": "Student One",
                        "faculty": "BCA",
                        "semester": 9,
                        "email": "random@gmail.com"
                        
                    
                }
            )
        
    assert student1_response.status_code == 422


def test_get_students_without_token(client):
    response = client.get("/students")

    assert response.status_code == 401
    
    
def test_get_students_invalid_token(client):
    response = client.get(
        "/students",
        headers={
            "Authorization": "Bearer this_is_a_fake_token"
        }
    )

    assert response.status_code == 401
    
def test_tampered_token(client, admin_token):
    tampered_token = admin_token[:-1] + "x"
    
    get_response = client.get(
        "/students",
        headers={
            "Authorization": f"Bearer {tampered_token}"
        })
    assert get_response.status_code == 401