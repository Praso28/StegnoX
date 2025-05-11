# StegnoX - Advanced Steganography Analysis Tool

StegnoX is a powerful tool for analyzing and working with steganography in images. It provides both a web interface and a desktop application for hiding and revealing messages in images.

## Features

- **Advanced Steganography Engine**:
  - LSB (Least Significant Bit) extraction and encoding
  - Parity bit analysis and encoding
  - Metadata extraction and encoding
  - DCT (Discrete Cosine Transform) analysis
  - Bit plane analysis
  - Histogram analysis
  - Support for multiple image formats

- **Job Queue System**:
  - Priority-based job scheduling
  - Job status tracking
  - Persistent job storage
  - Multi-threaded worker support

- **Storage Service**:
  - Secure file storage
  - Results management
  - Metadata tracking
  - Temporary file handling

- **Multiple Interfaces**:
  - Web API for remote access
  - Desktop GUI for local use
  - Command-line tools for automation

## Project Structure

```
StegnoX/
├── backend/           # Flask API backend
├── deployment/        # Deployment configuration files
│   ├── deploy.sh
│   ├── docker-compose.yml
│   ├── docker-compose.dev.yml
│   └── docker-compose.prod.yml
├── desktop/           # Desktop GUI application
│   ├── build_desktop.py  # Desktop build script
│   └── ...
├── docs/              # Documentation
│   └── architecture.md  # System architecture
├── engine/            # Steganography engine
│   ├── stegnox_engine.py  # Core steganography algorithms
│   └── README.md      # Engine documentation
├── examples/          # Example scripts
│   ├── engine_demo.py  # Engine usage examples
│   ├── worker.py      # Worker implementation
│   ├── submit_job.py  # Job submission example
│   └── check_job.py   # Job status checking
├── frontend/          # React web frontend
│   └── src/           # Frontend source code
├── queue/             # Job queue system
│   ├── job_queue.py   # Job queue implementation
│   └── README.md      # Queue documentation
├── storage/           # Storage service
│   ├── storage_service.py  # Storage implementation
│   └── README.md      # Storage documentation
├── tests/             # Test files
│   ├── unit/          # Unit tests
│   ├── integration/   # Integration tests
│   └── e2e/           # End-to-end tests
├── main.py            # Main entry point
├── README.md          # Project documentation
└── requirements.txt   # Python dependencies
```

## Installation

### Local Development

1. Clone the repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

### Web Mode

```
python main.py --mode web
```

This will start the Flask API server on http://localhost:5000.

### Desktop Mode

```
python main.py --mode desktop
```

This will launch the desktop GUI application.

### Example Scripts

The `examples/` directory contains scripts demonstrating how to use the StegnoX components:

```
# Run the engine demo
python examples/engine_demo.py --action analyze --image path/to/image.png

# Start a worker process
python examples/worker.py

# Submit a job to the queue
python examples/submit_job.py --image path/to/image.png

# Check job status
python examples/check_job.py --job-id <job_id>
```

See the [examples README](examples/README.md) for more details.

## Testing

Run the tests to ensure all components are working correctly:

```
# Run all tests
python -m unittest discover tests

# Run specific tests
python -m unittest tests/test_engine.py
python -m unittest tests/test_storage.py
python -m unittest tests/test_queue.py
```

## Development

See the [architecture document](docs/architecture.md) for details on the system design.

Each component has its own README with detailed documentation:
- [Engine Documentation](engine/README.md)
- [Storage Service Documentation](storage/README.md)
- [Job Queue Documentation](queue/README.md)

## Deployment

StegnoX can be deployed in several ways:

1. **Docker Deployment**: Deploy using Docker and Docker Compose
2. **Manual Deployment**: Deploy the components manually
3. **Desktop Application**: Build and distribute the desktop application

For detailed deployment instructions, see the [deployment guide](docs/deployment.md).

### Docker Deployment

Deploy using Docker and Docker Compose:

```bash
# Navigate to the deployment directory
cd deployment

# For development
docker-compose -f docker-compose.dev.yml up

# For production
docker-compose -f docker-compose.prod.yml up -d
```

### Desktop Application Distribution

To build the desktop application installers:

```bash
# Navigate to the desktop directory
cd desktop

# Build for all platforms
python build_desktop.py --version 2023.5.1
```

## License

MIT