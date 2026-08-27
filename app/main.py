
from fastapi import FastAPI
from fastapi import HTTPException

from fastapi import status

from sqlalchemy.exc import IntegrityError


from fastapi import Depends
from sqlalchemy.orm import Session

from .database import get_db
from .models import Student as StudentModel

from .models import User as UserModel

from .security import (
    hash_password,
    require_admin,
    verify_password,
    create_access_token,
    get_current_user
)

from .schemas import (
    StudentCreate,
    StudentResponse,
    StudentUpdate,
    UserCreate,
    UserResponse,
    UserLogin,
    UserUpdate
)

from fastapi.security import OAuth2PasswordRequestForm

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Welcome to Student Management API"}


@app.get("/students", response_model=list[StudentResponse])
def get_students(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    students = db.query(StudentModel).all()
    return students


@app.post("/students", response_model=StudentResponse)
def create_student(
                    student: StudentCreate,
                    db: Session = Depends(get_db),
                    current_user: UserModel = Depends(require_admin)):
    new_student = StudentModel(
    name=student.name,
    faculty=student.faculty,
    semester=student.semester,
    email=student.email
)

    db.add(new_student)
    
    try:
        db.commit()
        db.refresh(new_student)
        
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    return new_student
    
    

    

           
    


@app.delete("/students/{student_id}")
def delete_student(student_id: int,
                   db: Session = Depends(get_db),
                   current_user: UserModel = Depends(require_admin)):
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
                   db: Session = Depends(get_db),
                   current_user: UserModel = Depends(require_admin)):
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


@app.get("/students/{student_id}", response_model=StudentResponse)
def get_student(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
            
    student = db.query(StudentModel).filter(StudentModel.id == student_id).first()
    
    if not student:
                raise HTTPException(
                    status_code=404,
                    detail="Student not found"
                )
    
    return student


    
    

    


@app.post("/auth/register", response_model= UserResponse)
def register_user( user: UserCreate, db: Session = Depends(get_db),):
    hashed_password = hash_password(user.password)

    new_user = UserModel(
        email=user.email,
        password_hash=hashed_password
    )

    db.add(new_user)
    try:
        db.commit()
        db.refresh(new_user)

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )
    return new_user


@app.post("/auth/login")
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    existing_user = db.query(UserModel).filter(
        UserModel.email == form_data.username
    ).first()

    if not existing_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not verify_password(
        form_data.password,
        existing_user.password_hash
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    access_token = create_access_token(
        {"sub": str(existing_user.id)}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
    
@app.get("/users/me", response_model=UserResponse)
def get_my_profile(
    
    current_user: UserModel = Depends(get_current_user)
):
    return current_user

@app.put("/users/me", response_model=UserResponse)
def update_my_profile(
    updated_user: UserUpdate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    current_user.email = updated_user.email
    current_user.password_hash = hash_password(updated_user.password)
        
    db.commit()
    db.refresh(current_user)

    return current_user

@app.delete("/users/me", status_code=status.HTTP_204_NO_CONTENT)
def delete_my_account(
                   db: Session = Depends(get_db),
                   current_user: UserModel = Depends(get_current_user)
                   ):
  
    db.delete(current_user)
    db.commit()
    return 
    