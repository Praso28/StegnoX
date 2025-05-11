# StegnoX Architecture

## Overview

StegnoX is a comprehensive steganography analysis tool designed with a modular architecture. It consists of several key components that work together to provide a seamless experience for analyzing and working with steganography in images.

## Components

### 1. Web Frontend (React)

The web frontend provides a user-friendly interface for interacting with the StegnoX system. It is built using React and includes the following features:

- User authentication and account management
- Image upload and management
- Steganography analysis and encoding
- Job management and monitoring
- Results visualization

The frontend communicates with the backend API using RESTful endpoints.

### 2. Backend API (Flask)

The backend API serves as the central hub for the StegnoX system. It is built using Flask and provides the following functionality:

- RESTful API endpoints for all system operations
- Authentication and authorization
- Job management
- File handling and validation
- Integration with the steganography engine, job queue, and storage service

### 3. Steganography Engine

The steganography engine is the core component of StegnoX. It provides the following functionality:

- LSB (Least Significant Bit) extraction and encoding
- Parity bit analysis and encoding
- Metadata extraction and encoding
- DCT (Discrete Cosine Transform) analysis
- Bit plane analysis
- Histogram analysis
- Support for multiple image formats

The engine is designed to be extensible, allowing for the addition of new steganography methods.

### 4. Job Queue System

The job queue system manages the processing of steganography analysis and encoding jobs. It provides the following features:

- Priority-based job scheduling
- Job status tracking
- Persistent job storage
- Multi-threaded worker support

### 5. Storage Service

The storage service manages the storage of images and analysis results. It provides the following functionality:

- Secure file storage
- Result storage and retrieval
- Temporary file management
- Cleanup routines

## Data Flow

### Analysis Workflow

1. User uploads an image through the web frontend or desktop application
2. Frontend sends the image to the backend API
3. Backend validates the image and creates a job in the queue
4. Worker picks up the job from the queue
5. Worker uses the steganography engine to analyze the image
6. Results are stored in the storage service
7. User is notified that the analysis is complete
8. User views the results through the frontend

### Encoding Workflow

1. User uploads a cover image and enters a message through the frontend
2. Frontend sends the image and message to the backend API
3. Backend validates the inputs and creates a job in the queue
4. Worker picks up the job from the queue
5. Worker uses the steganography engine to encode the message into the image
6. Encoded image is stored in the storage service
7. User is notified that the encoding is complete
8. User downloads the encoded image through the frontend

## System Architecture Diagram

```
+----------------+     +----------------+     +----------------+
|                |     |                |     |                |
|  Web Frontend  |<--->|  Backend API   |<--->|  Job Queue     |
|  (React)       |     |  (Flask)       |     |                |
|                |     |                |     |                |
+----------------+     +----------------+     +----------------+
                              ^                      ^
                              |                      |
                              v                      v
                       +----------------+     +----------------+
                       |                |     |                |
                       |  Storage       |<--->|  Workers       |
                       |  Service       |     |                |
                       |                |     |                |
                       +----------------+     +----------------+
                              ^                      ^
                              |                      |
                              v                      v
                       +----------------+
                       |                |
                       |  Steganography |
                       |  Engine        |
                       |                |
                       +----------------+
```

## Technology Stack

- **Frontend**: React, JavaScript, HTML, CSS
- **Backend**: Python, Flask
- **Database**: SQLite (development), PostgreSQL (production)
- **Job Queue**: Custom implementation with JSON file storage
- **Storage**: File system-based storage
- **Deployment**: Docker, Docker Compose
