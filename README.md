# Loyalty Point System for Mobile Banking

This is a FastAPI-based project that implements a Loyalty Point system for a mobile banking application. The system allows users to accumulate and redeem points, manage their vouchers, and make payments. It also includes JWT authentication for secure user login and registration, backed by MySQL using SQLAlchemy ORM.

## Features

- **User Authentication**: Secure authentication using JWT.
- **Points Accumulation**: Users earn points based on their transactions.
- **Voucher Redemption**: Users can redeem vouchers based on their points.
- **Payments**: Users can make payments using their points or vouchers.
- **Admin Interface**: Manage vouchers and view transaction reports.

## Technologies Used

- **FastAPI**: Web framework for building APIs.
- **MySQL**: Database for storing user, transaction, and voucher data.
- **SQLAlchemy**: ORM for interacting with MySQL.
- **JWT**: For handling user authentication and authorization.
- **Pydantic**: Data validation and settings management using Python type annotations.
- **Docker**: For containerizing the application (optional).

## Installation

### Requirements

- Python 3.9+
- MySQL
- Docker (Optional)

### Steps

1. **Clone the repository**:

    ```bash
    git clone https://github.com/your-repo/loyalty-point-system.git
    cd loyalty-point-system
    ```

2. **Set up a virtual environment**:

    ```bash
    python3 -m venv env
    source env/bin/activate
    ```

3. **Install dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

4. **Configure the environment**:

    Create a `.env` file with the following variables:

    ```env
    DATABASE_URL=mysql+pymysql://<username>:<password>@<host>/<database>
    JWT_SECRET_KEY=your_jwt_secret_key
    JWT_ALGORITHM=HS256
    ACCESS_TOKEN_EXPIRE_MINUTES=30
    ```

5. **Run database migrations**:

    If using Alembic for migrations:

    ```bash
    alembic upgrade head
    ```

6. **Run the FastAPI server**:

    ```bash
    uvicorn app.main:app --reload
    ```

    The application will be available at `http://127.0.0.1:8000`.

### Docker Setup (Optional)

1. **Build the Docker image**:

    ```bash
    docker build -t loyalty-point-system .
    ```

2. **Run the Docker container**:

    ```bash
    docker run -d -p 8000:8000 loyalty-point-system
    ```

## API Endpoints

### Authentication

- **POST** `/auth/register`: Register a new user.
- **POST** `/auth/login`: Authenticate and obtain a JWT token.

### User Points

- **GET** `/points/{user_id}`: Get user’s current points.
- **POST** `/points/add`: Add points to a user account.

### Voucher Redemption

- **POST** `/voucher/redeem`: Redeem a voucher using points.
- **GET** `/voucher/{user_id}`: Get available vouchers for a user.

### Payments

- **POST** `/payments`: Make a payment using points or vouchers.