# StegnoX Developer Guide

## Architecture

StegnoX follows a modular architecture with the following components:

1. **Engine**: Core steganography algorithms
2. **Storage**: File and result storage
3. **Queue**: Job scheduling and management
4. **Backend**: API endpoints and authentication
5. **Frontend**: Web interface
6. **Desktop**: Desktop application

### Component Interactions

```
+-------------+      +-------------+      +-------------+
|   Frontend  |----->|   Backend   |----->|   Engine    |
+-------------+      +-------------+      +-------------+
                           |                    |
                           v                    v
                     +-------------+      +-------------+
                     |    Queue    |----->|   Storage   |
                     +-------------+      +-------------+
```

## Development Environment Setup

### Prerequisites

- Python 3.8 or higher
- Node.js 14 or higher (for frontend development)
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

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up the frontend:
   ```bash
   cd frontend
   npm install
   ```

5. Run the application in development mode:
   ```bash
   python main.py --mode web --debug
   ```

## Code Structure

```
stegnox/
├── engine/                # Core steganography algorithms
│   ├── stegnox_engine.py  # Main engine class
│   └── algorithms/        # Individual algorithms
├── storage/               # Storage service
│   └── storage_service.py # Storage implementation
├── queue/                 # Job queue
│   └── job_queue.py       # Queue implementation
├── backend/               # API backend
│   ├── api/               # API endpoints
│   ├── auth/              # Authentication
│   ├── config/            # Configuration
│   └── utils/             # Utilities
├── frontend/              # Web frontend
│   ├── src/               # Source code
│   └── public/            # Static assets
├── desktop/               # Desktop application
│   ├── app.py             # Main application
│   └── ui/                # UI components
├── tests/                 # Tests
│   ├── test_engine.py     # Engine tests
│   ├── test_storage.py    # Storage tests
│   ├── test_queue.py      # Queue tests
│   ├── integration/       # Integration tests
│   ├── e2e/               # End-to-end tests
│   └── desktop/           # Desktop tests
├── docs/                  # Documentation
├── deployment/            # Deployment scripts
└── main.py                # Application entry point
```

## Adding New Features

### Adding a New Steganography Algorithm

1. Create a new file in `engine/algorithms/` for your algorithm.
2. Implement the algorithm with extract and encode methods.
3. Add the algorithm to the `StegnoxEngine` class in `engine/stegnox_engine.py`.
4. Add tests for the algorithm in `tests/test_engine.py`.

Example:

```python
# engine/algorithms/new_algorithm.py
def extract(image_path):
    """Extract hidden data using the new algorithm"""
    # Implementation
    return {"message": "Extracted message"}

def encode(image_path, message):
    """Encode a message using the new algorithm"""
    # Implementation
    return {"encoded_image_path": "path/to/encoded/image.png"}

# In engine/stegnox_engine.py
from .algorithms import new_algorithm

class StegnoxEngine:
    # ...
    
    def extract_new_algorithm(self, image_path):
        """Extract data using the new algorithm"""
        return new_algorithm.extract(image_path)
    
    def encode_new_algorithm(self, image_path, message):
        """Encode a message using the new algorithm"""
        return new_algorithm.encode(image_path, message)
```

### Adding a New API Endpoint

1. Create a new route in the appropriate blueprint in `backend/api/v1/`.
2. Implement the endpoint logic.
3. Add tests for the endpoint in `tests/test_backend.py`.

Example:

```python
# In backend/api/v1/analysis.py
from flask import Blueprint, request, jsonify
from ...utils.response import success_response, error_response
from ...utils.error_handler import handle_error

@analysis_bp.route('/new-endpoint', methods=['POST'])
@handle_error
def new_endpoint():
    """New API endpoint"""
    # Implementation
    return success_response(data={"result": "Success"}, message="Operation successful")
```

## Testing

### Running Tests

```bash
# Run all tests
python run_tests.py

# Run specific test types
python run_tests.py --unit
python run_tests.py --integration
python run_tests.py --e2e
python run_tests.py --desktop

# Run with coverage
python run_tests.py --coverage --html
```

### Writing Tests

1. Unit tests should be placed in the `tests/` directory.
2. Integration tests should be placed in the `tests/integration/` directory.
3. End-to-end tests should be placed in the `tests/e2e/` directory.
4. Desktop tests should be placed in the `tests/desktop/` directory.

Example:

```python
import unittest
from engine.stegnox_engine import StegnoxEngine

class TestNewAlgorithm(unittest.TestCase):
    def setUp(self):
        self.engine = StegnoxEngine()
        self.test_image = "tests/data/test_image.png"
    
    def test_extract_new_algorithm(self):
        result = self.engine.extract_new_algorithm(self.test_image)
        self.assertIn("message", result)
    
    def test_encode_new_algorithm(self):
        message = "Test message"
        result = self.engine.encode_new_algorithm(self.test_image, message)
        self.assertIn("encoded_image_path", result)
```

## Deployment

See the [Deployment Guide](../deployment/README.md) for detailed deployment instructions.
