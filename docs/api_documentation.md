# StegnoX API Documentation

## Overview

The StegnoX API provides endpoints for interacting with the StegnoX system. It allows you to analyze images for steganography, encode messages into images, and manage jobs.

## Base URL

```
http://localhost:5000/api/v1
```

## Authentication

Most endpoints require authentication. To authenticate, include a JWT token in the `Authorization` header:

```
Authorization: Bearer <token>
```

To obtain a token, use the `/auth/login` endpoint.

## Endpoints

### Authentication

#### Register a new user

```
POST /auth/register
```

**Request Body:**

```json
{
  "username": "user123",
  "email": "user@example.com",
  "password": "securepassword"
}
```

**Response:**

```json
{
  "success": true,
  "message": "User registered successfully",
  "data": {
    "user_id": "123e4567-e89b-12d3-a456-426614174000",
    "username": "user123",
    "email": "user@example.com"
  }
}
```

#### Login

```
POST /auth/login
```

**Request Body:**

```json
{
  "username": "user123",
  "password": "securepassword"
}
```

**Response:**

```json
{
  "success": true,
  "message": "Login successful",
  "data": {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "user": {
      "user_id": "123e4567-e89b-12d3-a456-426614174000",
      "username": "user123",
      "email": "user@example.com"
    }
  }
}
```

### Analysis

#### Analyze an image

```
POST /analysis/analyze
```

**Request Body:**

Multipart form data with the following fields:
- `file`: The image file to analyze

**Response:**

```json
{
  "success": true,
  "message": "Analysis job created",
  "data": {
    "job_id": "123e4567-e89b-12d3-a456-426614174000",
    "status": "PENDING"
  }
}
```

#### Get analysis results

```
GET /analysis/results/{job_id}
```

**Response:**

```json
{
  "success": true,
  "message": "Analysis results retrieved",
  "data": {
    "job_id": "123e4567-e89b-12d3-a456-426614174000",
    "status": "COMPLETED",
    "results": {
      "lsb_extraction": {
        "extracted_text": "Hidden message",
        "confidence": 0.95
      },
      "parity_bit_extraction": {
        "extracted_text": "",
        "confidence": 0.1
      },
      "metadata_extraction": {
        "metadata": {
          "Author": "John Doe",
          "Software": "Adobe Photoshop"
        }
      },
      "dct_analysis": {
        "confidence": 0.2,
        "assessment": "No DCT-based steganography detected",
        "statistics": {
          "mean": 0.1,
          "std_dev": 0.05
        }
      },
      "bit_plane_analysis": {
        "planes": [
          {
            "plane": 0,
            "entropy": 7.2,
            "assessment": "Normal"
          },
          {
            "plane": 1,
            "entropy": 7.1,
            "assessment": "Normal"
          }
        ]
      },
      "histogram_analysis": {
        "assessment": "No anomalies detected",
        "statistics": {
          "chi_square": 0.3,
          "p_value": 0.8
        }
      }
    }
  }
}
```

### Encoding

#### Encode a message into an image

```
POST /encoding/encode
```

**Request Body:**

Multipart form data with the following fields:
- `file`: The cover image file
- `message`: The message to encode
- `method`: The encoding method (e.g., "lsb", "parity_bit", "metadata")

**Response:**

```json
{
  "success": true,
  "message": "Encoding job created",
  "data": {
    "job_id": "123e4567-e89b-12d3-a456-426614174000",
    "status": "PENDING"
  }
}
```

#### Get encoded image

```
GET /encoding/result/{job_id}
```

**Response:**

The encoded image file.

### Jobs

#### List jobs

```
GET /jobs
```

**Query Parameters:**
- `limit` (optional): Maximum number of jobs to return (default: 10)
- `offset` (optional): Number of jobs to skip (default: 0)
- `status` (optional): Filter by job status (e.g., "PENDING", "PROCESSING", "COMPLETED", "FAILED")

**Response:**

```json
{
  "success": true,
  "message": "Jobs retrieved",
  "data": {
    "jobs": [
      {
        "id": "123e4567-e89b-12d3-a456-426614174000",
        "type": "ANALYSIS",
        "status": "COMPLETED",
        "created_at": "2023-05-10T12:34:56Z",
        "updated_at": "2023-05-10T12:35:56Z"
      },
      {
        "id": "223e4567-e89b-12d3-a456-426614174000",
        "type": "ENCODING",
        "status": "PENDING",
        "created_at": "2023-05-10T12:36:56Z",
        "updated_at": "2023-05-10T12:36:56Z"
      }
    ],
    "total": 2,
    "limit": 10,
    "offset": 0
  }
}
```

#### Get job details

```
GET /jobs/{job_id}
```

**Response:**

```json
{
  "success": true,
  "message": "Job retrieved",
  "data": {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "type": "ANALYSIS",
    "status": "COMPLETED",
    "created_at": "2023-05-10T12:34:56Z",
    "updated_at": "2023-05-10T12:35:56Z",
    "image_path": "/storage/images/image123.png",
    "result_path": "/storage/results/result123.json",
    "user_id": "123e4567-e89b-12d3-a456-426614174000",
    "priority": "NORMAL",
    "error": null
  }
}
```

#### Cancel a job

```
POST /jobs/{job_id}/cancel
```

**Response:**

```json
{
  "success": true,
  "message": "Job cancelled",
  "data": {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "status": "CANCELLED"
  }
}
```

## Error Handling

All endpoints return a standard error format:

```json
{
  "success": false,
  "message": "Error message",
  "error": {
    "code": "ERROR_CODE",
    "details": "Additional error details"
  }
}
```

### Common Error Codes

- `AUTHENTICATION_ERROR`: Authentication failed
- `AUTHORIZATION_ERROR`: User not authorized to perform the action
- `VALIDATION_ERROR`: Invalid request parameters
- `NOT_FOUND`: Resource not found
- `SERVER_ERROR`: Internal server error

## Rate Limiting

The API implements rate limiting to prevent abuse. If you exceed the rate limit, you will receive a 429 Too Many Requests response with the following body:

```json
{
  "success": false,
  "message": "Rate limit exceeded",
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "details": "Try again in X seconds"
  }
}
```

## Pagination

Endpoints that return lists of resources support pagination through the `limit` and `offset` query parameters. The response includes the total number of resources, the limit, and the offset.

## Examples

### Analyzing an Image

```bash
# Upload an image for analysis
curl -X POST \
  http://localhost:5000/api/v1/analysis/analyze \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...' \
  -F 'file=@/path/to/image.png'

# Check the job status
curl -X GET \
  http://localhost:5000/api/v1/jobs/123e4567-e89b-12d3-a456-426614174000 \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...'

# Get the analysis results
curl -X GET \
  http://localhost:5000/api/v1/analysis/results/123e4567-e89b-12d3-a456-426614174000 \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...'
```

### Encoding a Message

```bash
# Encode a message into an image
curl -X POST \
  http://localhost:5000/api/v1/encoding/encode \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...' \
  -F 'file=@/path/to/cover.png' \
  -F 'message=Secret message' \
  -F 'method=lsb'

# Download the encoded image
curl -X GET \
  http://localhost:5000/api/v1/encoding/result/123e4567-e89b-12d3-a456-426614174000 \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...' \
  -o encoded_image.png
```
