
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
    UserUpdate,
    StudentPatch
)

from fastapi.security import OAuth2PasswordRequestForm

app = FastAPI(
    title="Student Management API",
    description="A REST API for managing students and user accounts with JWT authentication and role-based authorization.",
    version="1.0.0"
)


@app.get(
    "/",
    tags=["General"],
    summary="API welcome endpoint",
    description="Returns a welcome message confirming that the Student Management API is running."
)
def root():
    return {"message": "Welcome to Student Management API"}


@app.get(
    "/students",
    response_model=list[StudentResponse],
    tags=["Students"],
    summary="List all students",
    description="Returns all students. Authentication is required."
)
def get_students(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    students = db.query(StudentModel).all()
    return students


@app.post(
    "/students",
    response_model=StudentResponse,
    tags=["Students"],
    summary="Create a student",
    description="Creates a new student. Admin authentication is required. Student email addresses must be unique."
)
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
            status_code=409,
            detail="Email already exists"
        )

    return new_student
    
    

    

           
    


@app.delete(
    "/students/{student_id}",
    tags=["Students"],
    summary="Delete a student",
    description="Deletes a student by ID. Admin authentication is required."
)
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
    
   


@app.put(
    "/students/{student_id}",
    response_model=StudentResponse,
    tags=["Students"],
    summary="Replace a student",
    description="Updates all student fields. Admin authentication is required."
)
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

    try:
        db.commit()
        db.refresh(student)
            
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Email already exists"
            )
    

    return student


@app.get(
    "/students/{student_id}",
    response_model=StudentResponse,
    tags=["Students"],
    summary="Get a student",
    description="Returns a single student by ID. Authentication is required."
)
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


    
    

    

@app.post(
    "/auth/register",
    response_model=UserResponse,
    tags=["Authentication"],
    summary="Register a new user",
    description="Creates a new user account. The password is securely hashed before being stored."
)

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
            status_code=409,
            detail="Email already exists"
        )
    return new_user


@app.post(
    "/auth/login",
    tags=["Authentication"],
    summary="Log in",
    description="Authenticates a user and returns a JWT access token."
)
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
    
@app.get(
    "/users/me",
    response_model=UserResponse,
    tags=["Users"],
    summary="Get my profile",
    description="Returns the profile of the currently authenticated user."
)
def get_my_profile(
    
    current_user: UserModel = Depends(get_current_user)
):
    return current_user

@app.put(
    "/users/me",
    response_model=UserResponse,
    tags=["Users"],
    summary="Update my profile",
    description="Updates the authenticated user's email address and password."
)
def update_my_profile(
    updated_user: UserUpdate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    current_user.email = updated_user.email
    current_user.password_hash = hash_password(updated_user.password)
        
    try:
        db.commit()
        db.refresh(current_user)
    
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Email already exists"
        )
        

    return current_user

@app.delete(
    "/users/me",
    tags=["Users"],
    summary="Delete my account",
    description="Permanently deletes the currently authenticated user's account."
)
def delete_my_account(
                   db: Session = Depends(get_db),
                   current_user: UserModel = Depends(get_current_user)
                   ):
  
    db.delete(current_user)
    db.commit()
    return 
    
    
    



@app.patch(
    "/students/{student_id}",
    response_model=StudentResponse,
    tags=["Students"],
    summary="Partially update a student",
    description="Updates only the fields provided in the request. Admin authentication is required."
)
def update_student_partial(
    student_id: int,
    updated_student: StudentPatch,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(require_admin)
):
    student = db.query(StudentModel).filter(
        StudentModel.id == student_id
    ).first()

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    update_data = updated_student.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(student, field, value)

    try:
        db.commit()
        db.refresh(student)

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Email already exists"
        )

    return student
    
