# Student Management API

A REST API for managing students and user accounts, built with FastAPI, PostgreSQL, SQLAlchemy, and JWT-based authentication.

## Overview

The Student Management API provides endpoints for managing student records and user accounts.

The project includes:

* User registration and authentication
* JWT-based authentication
* Role-based authorization
* Student CRUD operations
* Input validation with Pydantic
* PostgreSQL database integration
* Database migrations with Alembic
* Automated API tests with pytest
* Interactive API documentation with Swagger UI

## Features

### Authentication

* User registration
* Secure password hashing
* User login
* JWT access tokens
* Authenticated user profile management

### Authorization

The API uses role-based authorization:

* **User** — can access authenticated user functionality and read student data
* **Admin** — can create, update, and delete student records

### Student Management

Administrators can:

* Create students
* View students
* View individual student records
* Update student records
* Partially update student records
* Delete student records

The API also validates student data and prevents duplicate student email addresses.

## Tech Stack

* **Python**
* **FastAPI**
* **PostgreSQL**
* **SQLAlchemy**
* **Alembic**
* **Pydantic**
* **JWT**
* **pwdlib**
* **pytest**
* **Uvicorn**
* **Swagger UI / OpenAPI**


## Project Structure

```text
StudentManagementAPI/
├── app/
│   ├── main.py          # FastAPI application and API routes
│   ├── database.py      # Database connection and session setup
│   ├── models.py        # SQLAlchemy database models
│   ├── schemas.py       # Pydantic request/response schemas
│   └── security.py      # Password hashing, JWT authentication and authorization
│
├── alembic/             # Database migration files
├── tests/               # Automated API tests
│   ├── conftest.py
│   ├── test_auth.py
│   ├── test_root.py
│   └── test_students.py
│
├── frontend/             # Frontend application
├── alembic.ini           # Alembic configuration
├── requirements.txt      # Python dependencies
├── Design.md             # Project design notes
└── README.md             # Project documentation
```

## Authentication & Authorization

The API uses JWT-based authentication.

### Authentication Flow

1. A user registers using `/auth/register`.
2. The password is securely hashed before being stored in the database.
3. The user logs in using `/auth/login`.
4. The API verifies the credentials and returns a JWT access token.
5. The client sends the token using the `Authorization` header:

```text
Authorization: Bearer <access_token>
```

6. Protected endpoints verify the token and identify the current user.

### Roles

The API currently supports two roles:

| Role  | Access                                                                 |
| ----- | ---------------------------------------------------------------------- |
| User  | Authenticated user operations and student read operations              |
| Admin | All user permissions plus student creation, modification, and deletion |

Admin-only operations are protected using role-based authorization.

## API Documentation

Once the application is running, interactive API documentation is available through Swagger UI:

```text
http://127.0.0.1:8000/docs
```

The OpenAPI specification is available at:

```text
http://127.0.0.1:8000/openapi.json
```

Swagger UI can be used to explore endpoints, inspect request/response schemas, and test the API.

## Environment Variables

Create a `.env` file in the project root.

Example:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/student_management
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Do **not** commit the `.env` file to Git.

The project already ignores `.env` through `.gitignore`.

## Setup & Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd StudentManagementAPI
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Linux/macOS:

```bash
source .venv/bin/activate
```

On Windows:

```bash
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create the `.env` file described above and configure your PostgreSQL database.

Make sure PostgreSQL is installed and running, and that the database specified by DATABASE_URL already exists.  

### 5. Run database migrations

```bash
alembic upgrade head
```


### 6. Start the application

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

## Running Tests

The project uses pytest for automated testing.

Run the complete test suite with:

```bash
pytest
```

The current test suite covers:

* User registration
* User login
* JWT authentication
* Invalid and tampered tokens
* Role-based authorization
* Student CRUD operations
* Validation errors
* Duplicate student emails
* Missing resources
* Protected endpoints

The test suite currently contains **24 tests**.

## API Endpoints

### General

| Method | Endpoint | Description          |
| ------ | -------- | -------------------- |
| GET    | `/`      | API welcome endpoint |

### Students

| Method | Endpoint                 | Access              |
| ------ | ------------------------ | ------------------- |
| GET    | `/students`              | Authenticated users |
| POST   | `/students`              | Admin               |
| GET    | `/students/{student_id}` | Authenticated users |
| PUT    | `/students/{student_id}` | Admin               |
| PATCH  | `/students/{student_id}` | Admin               |
| DELETE | `/students/{student_id}` | Admin               |

### Authentication

| Method | Endpoint         | Description                    |
| ------ | ---------------- | ------------------------------ |
| POST   | `/auth/register` | Register a new user            |
| POST   | `/auth/login`    | Authenticate and receive a JWT |

### Users

| Method | Endpoint    | Description                   |
| ------ | ----------- | ----------------------------- |
| GET    | `/users/me` | Get current user's profile    |
| PUT    | `/users/me` | Update current user's profile |
| DELETE | `/users/me` | Delete current user's account |

## Future Improvements

Possible future improvements include:

* Improved pagination for student listings
* More granular permissions
* Better API response/status-code conventions
* Additional integration tests
* Frontend integration and deployment
* Production deployment configuration
* CI/CD with automated testing

## License

This project is currently intended as a learning and portfolio project.
