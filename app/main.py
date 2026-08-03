from fastapi import FastAPI
from .models import Student

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Welcome to Student Management API"}

@app.get("/students")
def get_students():
    return students_db

@app.post("/students")
def create_student(student: Student):
    students_db.append(student)
    return {
            "message": "student created successfully",
            "student": student}



students_db = [
    Student(
            id=1,
            name="Niraj",
            faculty="Engineering",
            semester=3,
            email="niraj@example.com"
            )
    ,Student(
        id=2,
        name="Ram",
        faculty="BCA",
        semester=2,
        email="alice@example.com"
        )
    ,Student(
        id=3, 
        name="worm",
        faculty="Engineering",
        semester=3,
        email="worm@example.com"
        )
    ,Student(
        id=4, 
        name="luke",
        faculty="BSC-Csit",
        semester=5,
        email="luke@example.com"
        )
    ,Student(
        id=5, 
        name="jay",
        faculty="BBS",
        semester=6,
        email="jay@example.com"
        )
    ,Student(
        id=6, 
        name="Hari",
        faculty="BCA",
        semester=3,
        email="hari@example.com"
        )
    ]