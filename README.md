# Project Sotatek Intern Backend

## Introduction
Project Sotatek Intern Backend is a RESTful API service built using Flask, designed to handle user authentication and profile management. The project includes functionalities such as user registration, login, logout, token refresh, and profile retrieval.

## Setup and Installation

1. **Clone the repository:**

```bash
    git clone https://github.com/sotaicg/webchatbot_be.git
```

2. **Create a virtual environment and activate it:**
``` bash
    python -m venv project_backend
    source project_backend/bin/activate  # On Windows use `venv\Scripts\activate`
```
3. **Install the dependencies:**
``` bash
    pip install -r requirements.txt
```
4. **Set up the database:**
```bash
    Make sure you have a MySQL database running. Update your .env file with the correct database URI.

    DB_HOST=your_db_host
    DB_USER=your_db_user
    DB_PASSWORD=your_db_password
    DB_NAME=your_db_name
    SECRET_KEY=your_secret_key
    JWT_SECRET_KEY=your_jwt_secret_key

```

5. **Run the application:**
``` bash
    cd APIGateway
    python app.py
```

6. **Read document API:**
``` bash
    localhost:8080/swagger
```




