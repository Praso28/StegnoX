# StegnoX Backend

The StegnoX Backend is a Flask-based API that provides steganography analysis and job management functionality.

## Features

- **RESTful API**: Well-structured API with versioning
- **Authentication**: JWT-based authentication and authorization
- **Job Management**: Queue-based job processing system
- **Steganography Analysis**: Advanced steganography detection and encoding
- **File Management**: Secure file upload and download

## Directory Structure

```
backend/
├── api/              # API endpoints
│   └── v1/           # API version 1
│       ├── auth.py   # Authentication endpoints
│       ├── jobs.py   # Job management endpoints
│       └── analysis.py # Steganography analysis endpoints
├── auth/             # Authentication utilities
│   └── auth.py       # JWT token handling
├── config/           # Configuration
│   └── config.py     # Application configuration
├── models/           # Data models
│   ├── user.py       # User model
│   └── user_db.py    # User database
├── utils/            # Utility functions
│   ├── file_utils.py # File handling utilities
│   └── response.py   # Response formatting
├── app.py            # Main application
└── run.py            # Run script
```

## API Endpoints

### Authentication

- `POST /api/v1/auth/register`: Register a new user
- `POST /api/v1/auth/login`: Login a user
- `GET /api/v1/auth/users`: List all users (admin only)

### Job Management

- `POST /api/v1/jobs`: Create a new job
- `GET /api/v1/jobs`: List jobs
- `GET /api/v1/jobs/<job_id>`: Get job details
- `DELETE /api/v1/jobs/<job_id>`: Cancel a job

### Steganography Analysis

- `POST /api/v1/analysis/analyze`: Analyze an image for steganography
- `POST /api/v1/analysis/encode`: Encode a message in an image
- `GET /api/v1/analysis/images/<filename>`: Get an image from storage

## Authentication

The API uses JWT (JSON Web Tokens) for authentication. To access protected endpoints, you need to include the token in the Authorization header:

```
Authorization: Bearer <token>
```

You can obtain a token by registering a new user or logging in.

## Usage Examples

### Register a new user

```bash
curl -X POST http://localhost:5000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "email": "test@example.com", "password": "password123"}'
```

### Login

```bash
curl -X POST http://localhost:5000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "password123"}'
```

### Create a job

```bash
curl -X POST http://localhost:5000/api/v1/jobs \
  -H "Authorization: Bearer <token>" \
  -F "file=@/path/to/image.png" \
  -F "priority=high"
```

### Analyze an image

```bash
curl -X POST http://localhost:5000/api/v1/analysis/analyze \
  -H "Authorization: Bearer <token>" \
  -F "file=@/path/to/image.png" \
  -F "methods=lsb_extraction,parity_bit_extraction"
```

## Running the Backend

```bash
cd backend
python run.py
```

The API will be available at http://localhost:5000.
