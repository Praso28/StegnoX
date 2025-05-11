# StegnoX Developer Guide

## Introduction

This guide is intended for developers who want to contribute to the StegnoX project. It provides information about the codebase structure, development environment setup, coding standards, and contribution guidelines.

## Codebase Structure

The StegnoX codebase is organized into several components:

```
StegnoX/
├── backend/           # Flask API backend
│   ├── api/           # API endpoints
│   ├── auth/          # Authentication utilities
│   ├── config/        # Configuration
│   ├── models/        # Data models
│   └── utils/         # Utility functions
├── desktop/           # Desktop GUI application
│   ├── ui/            # UI components
│   ├── controllers/   # Application controllers
│   └── utils/         # Utility functions
├── engine/            # Steganography engine
│   └── stegnox_engine.py  # Core steganography algorithms
├── frontend/          # React web frontend
│   ├── src/           # Frontend source code
│   │   ├── assets/    # Static assets
│   │   ├── components/# Reusable UI components
│   │   ├── context/   # React context providers
│   │   ├── pages/     # Page components
│   │   ├── services/  # API service functions
│   │   ├── styles/    # CSS styles
│   │   └── utils/     # Utility functions
│   └── public/        # Public assets
├── queue/             # Job queue system
│   └── job_queue.py   # Job queue implementation
├── storage/           # Storage service
│   └── storage_service.py  # Storage implementation
├── docs/              # Documentation
│   └── architecture.md  # System architecture
├── tests/             # Test files
│   ├── unit/          # Unit tests
│   ├── integration/   # Integration tests
│   └── e2e/           # End-to-end tests
├── examples/          # Example scripts
├── main.py            # Main entry point
└── requirements.txt   # Python dependencies
```

## Development Environment Setup

### Prerequisites

- Python 3.8 or higher
- Node.js 14 or higher
- Git

### Setting Up the Development Environment

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/stegnox.git
   cd stegnox
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # Development dependencies
   ```

4. Install frontend dependencies:
   ```bash
   cd frontend
   npm install
   cd ..
   ```

5. Set up pre-commit hooks:
   ```bash
   pre-commit install
   ```

### Running the Application

#### Backend

```bash
# Run the backend in development mode
python main.py --mode web --debug
```

#### Frontend

```bash
# Run the frontend development server
cd frontend
npm start
```

#### Desktop Application

```bash
# Run the desktop application
python main.py --mode desktop --debug
```

## Coding Standards

### Python

- Follow PEP 8 style guide
- Use type hints
- Write docstrings for all functions, classes, and modules
- Use meaningful variable and function names
- Keep functions small and focused on a single task
- Write unit tests for all new code

### JavaScript/React

- Follow the Airbnb JavaScript Style Guide
- Use ES6+ features
- Use functional components and hooks
- Use PropTypes for component props
- Keep components small and focused on a single responsibility
- Write unit tests for all new components

## Testing

### Running Tests

```bash
# Run all tests
python -m unittest discover tests

# Run unit tests
python -m unittest discover tests/unit

# Run integration tests
python -m unittest discover tests/integration

# Run end-to-end tests
python -m unittest discover tests/e2e

# Run with coverage
coverage run -m unittest discover tests
coverage report
coverage html  # Generates HTML report
```

### Writing Tests

- Write unit tests for all new code
- Use meaningful test names that describe what is being tested
- Follow the Arrange-Act-Assert pattern
- Mock external dependencies
- Keep tests independent of each other
- Test both success and failure cases

## Contributing

### Contribution Workflow

1. Fork the repository
2. Create a new branch for your feature or bug fix
3. Make your changes
4. Run tests to ensure your changes don't break existing functionality
5. Submit a pull request

### Pull Request Guidelines

- Keep pull requests focused on a single feature or bug fix
- Include tests for all new code
- Update documentation as needed
- Follow the coding standards
- Write a clear and concise description of your changes

### Code Review Process

- All pull requests must be reviewed by at least one maintainer
- Address all review comments
- Ensure all tests pass
- Ensure code coverage does not decrease

## Architecture

### Component Interactions

The StegnoX system consists of several components that interact with each other:

1. **Web Frontend**: Communicates with the Backend API using RESTful endpoints
2. **Backend API**: Integrates with the Steganography Engine, Job Queue, and Storage Service
3. **Desktop Application**: Uses the Steganography Engine directly
4. **Steganography Engine**: Provides algorithms for steganography analysis and encoding
5. **Job Queue**: Manages the processing of steganography jobs
6. **Storage Service**: Manages the storage of images and results

### Data Flow

1. User uploads an image through the Web Frontend or Desktop Application
2. The image is sent to the Backend API (Web) or processed directly (Desktop)
3. The Backend API creates a job in the Job Queue
4. Workers process the job using the Steganography Engine
5. Results are stored using the Storage Service
6. The user is notified that the job is complete
7. The user views the results

## Adding New Features

### Adding a New Steganography Method

1. Add the method to the `StegnoxEngine` class in `engine/stegnox_engine.py`
2. Add the method to the `self.methods` list in `__init__`
3. Add tests for the new method in `tests/unit/test_engine.py`
4. Update the frontend to support the new method
5. Update the documentation

### Adding a New API Endpoint

1. Create a new endpoint in the appropriate file in `backend/api/v1/`
2. Add tests for the new endpoint in `tests/unit/test_backend.py`
3. Update the API documentation
4. Update the frontend to use the new endpoint

### Adding a New Frontend Feature

1. Create new components in `frontend/src/components/`
2. Add the components to the appropriate pages
3. Add tests for the new components
4. Update the user documentation

## Deployment

### Backend Deployment

The backend can be deployed using Docker:

```bash
# Build the Docker image
docker build -t stegnox-backend .

# Run the container
docker run -p 5000:5000 stegnox-backend
```

### Frontend Deployment

The frontend can be built and deployed to a static hosting service:

```bash
# Build the frontend
cd frontend
npm run build

# Deploy to a static hosting service
# (specific commands depend on the service)
```

### Desktop Application Distribution

The desktop application can be packaged for distribution:

```bash
# Package the application
python setup.py py2app  # macOS
python setup.py py2exe  # Windows
python setup.py bdist_rpm  # Linux
```

## Resources

- [Python Documentation](https://docs.python.org/3/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [React Documentation](https://reactjs.org/docs/getting-started.html)
- [Steganography Resources](https://en.wikipedia.org/wiki/Steganography)

## Getting Help

If you need help with development, please:
1. Check the existing documentation
2. Look for similar issues in the issue tracker
3. Ask questions in the developer chat
4. Contact the maintainers at dev@stegnox.com
