from fastapi import FastAPI

from fastapi import HTTPException

from fastapi import Depends
from sqlalchemy.orm import Session

from .database import get_db
from .models import Student as StudentModel


from .schemas import StudentCreate, StudentResponse, StudentUpdate





app = FastAPI()


@app.get("/")
def root():
    return {"message": "Welcome to Student Management API"}

@app.get("/students", response_model=list[StudentResponse])
def get_students(db: Session = Depends(get_db)):
    students = db.query(StudentModel).all()
    return students

@app.post("/students", response_model=StudentResponse)
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    new_student = StudentModel(
    name=student.name,
    faculty=student.faculty,
    semester=student.semester,
    email=student.email
)

    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    return new_student
    
    
    
    

@app.get("/students/{student_id}", response_model=StudentResponse)
def get_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(StudentModel).filter(StudentModel.id == student_id).first()
    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )
    return student              
    


@app.delete("/students/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(StudentModel).filter(StudentModel.id == student_id).first()
    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )
    db.delete(student)
    db.commit()
    return {"message": "Student deleted successfully"}
    
   


@app.put("/students/{student_id}", response_model=StudentResponse)
def update_student(student_id: int,
                   updated_student: StudentUpdate,
                   db: Session = Depends(get_db)):
    student = db.query(StudentModel).filter(StudentModel.id == student_id).first()

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    
    student.name = updated_student.name
    student.faculty = updated_student.faculty
    student.semester = updated_student.semester
    student.email = updated_student.email

    db.commit()
    db.refresh(student)

    return student





