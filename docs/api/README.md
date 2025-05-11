# StegnoX API Documentation

## Overview

The StegnoX API provides endpoints for steganography analysis, encoding, and job management. This document describes the available endpoints, request formats, and response structures.

## Base URL

All API endpoints are relative to the base URL:

```
http://your-server/api/v1
```

## Authentication

Most endpoints require authentication using a JWT token. To authenticate, include the token in the Authorization header:

```
Authorization: Bearer <your_token>
```

### Getting a Token

To get a token, use the login endpoint:

```
POST /auth/login
```

Request body:
```json
{
  "username": "your_username",
  "password": "your_password"
}
```

Response:
```json
{
  "success": true,
  "data": {
    "token": "your_jwt_token",
    "user": {
      "username": "your_username",
      "email": "your_email",
      "role": "user"
    }
  },
  "message": "Login successful"
}
```

## Endpoints

### Authentication

#### Register a new user

```
POST /auth/register
```

Request body:
```json
{
  "username": "new_user",
  "email": "user@example.com",
  "password": "secure_password"
}
```

#### Login

```
POST /auth/login
```

Request body:
```json
{
  "username": "your_username",
  "password": "your_password"
}
```

### Analysis

#### Analyze an image

```
POST /analysis/analyze
```

Request body (multipart/form-data):
- `file`: The image file to analyze

Response:
```json
{
  "success": true,
  "data": {
    "lsb_extraction": { ... },
    "parity_bit_extraction": { ... },
    "metadata_extraction": { ... },
    "dct_analysis": { ... },
    "bit_plane_analysis": { ... },
    "histogram_analysis": { ... }
  },
  "message": "Analysis completed successfully"
}
```

#### Encode a message in an image

```
POST /analysis/encode
```

Request body (multipart/form-data):
- `file`: The cover image file
- `message`: The message to hide
- `method`: The encoding method (e.g., "lsb_encoding", "parity_bit_encoding", "metadata_encoding")

Response:
```json
{
  "success": true,
  "data": {
    "filename": "encoded_image.png",
    "download_url": "/api/v1/analysis/download/encoded_image.png"
  },
  "message": "Message encoded successfully"
}
```

### Jobs

#### Create a job

```
POST /jobs
```

Request body (multipart/form-data):
- `file`: The image file to analyze
- `priority`: Job priority (high, normal, low)

Response:
```json
{
  "success": true,
  "data": {
    "job_id": "job_123456",
    "status": "pending"
  },
  "message": "Job created successfully"
}
```

#### Get job status

```
GET /jobs/{job_id}
```

Response:
```json
{
  "success": true,
  "data": {
    "job_id": "job_123456",
    "status": "completed",
    "results": { ... }
  },
  "message": "Job retrieved successfully"
}
```

#### List jobs

```
GET /jobs
```

Query parameters:
- `status`: Filter by status (pending, processing, completed, failed)
- `limit`: Maximum number of jobs to return (default: 10)
- `offset`: Offset for pagination (default: 0)

Response:
```json
{
  "success": true,
  "data": {
    "jobs": [
      {
        "job_id": "job_123456",
        "status": "completed",
        "created_at": "2023-01-01T12:00:00Z"
      },
      ...
    ],
    "total": 100,
    "limit": 10,
    "offset": 0
  },
  "message": "Jobs retrieved successfully"
}
```

## Error Handling

All API endpoints return a consistent error format:

```json
{
  "success": false,
  "message": "Error message",
  "errors": { ... }
}
```

Common HTTP status codes:
- 200: Success
- 201: Created
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 500: Internal Server Error
