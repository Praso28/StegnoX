# StegnoX Test Plan

## Overview

This document outlines the testing strategy for the StegnoX project. It covers unit tests, integration tests, end-to-end tests, and continuous integration.

## Test Types

### Unit Tests

Unit tests verify that individual components work as expected in isolation.

#### Engine Tests (`test_engine.py`)

| Test Case | Description | Status |
|-----------|-------------|--------|
| `test_lsb_extraction` | Test LSB extraction algorithm | Implemented |
| `test_lsb_encoding` | Test LSB encoding algorithm | Implemented |
| `test_parity_bit_extraction` | Test parity bit extraction | Implemented |
| `test_parity_bit_encoding` | Test parity bit encoding | To be implemented |
| `test_metadata_extraction` | Test metadata extraction | Implemented |
| `test_metadata_encoding` | Test metadata encoding | To be implemented |
| `test_dct_analysis` | Test DCT analysis | Implemented |
| `test_bit_plane_analysis` | Test bit plane analysis | Implemented |
| `test_histogram_analysis` | Test histogram analysis | Implemented |
| `test_extract_all_methods` | Test all extraction methods | Implemented |
| `test_detect_steganography` | Test steganography detection | To be implemented |
| `test_supported_formats` | Test support for different image formats | To be implemented |

#### Storage Tests (`test_storage.py`)

| Test Case | Description | Status |
|-----------|-------------|--------|
| `test_save_image_bytes` | Test saving image from bytes | Implemented |
| `test_save_image_path` | Test saving image from path | Implemented |
| `test_save_image_auto_filename` | Test auto-generated filename | Implemented |
| `test_save_get_results` | Test saving and retrieving results | Implemented |
| `test_list_results` | Test listing results | Implemented |
| `test_delete_results` | Test deleting results | To be implemented |
| `test_temp_files` | Test temporary file management | Implemented |
| `test_storage_limits` | Test storage limits | To be implemented |
| `test_file_organization` | Test file organization | To be implemented |

#### Queue Tests (`test_queue.py`)

| Test Case | Description | Status |
|-----------|-------------|--------|
| `test_add_job` | Test adding a job | Implemented |
| `test_get_job` | Test retrieving a job | Implemented |
| `test_get_next_job` | Test getting the next job | Implemented |
| `test_mark_job_complete` | Test marking a job as complete | Implemented |
| `test_mark_job_failed` | Test marking a job as failed | Implemented |
| `test_cancel_job` | Test canceling a job | Implemented |
| `test_list_jobs` | Test listing jobs | Implemented |
| `test_get_queue_stats` | Test getting queue statistics | Implemented |
| `test_cleanup_old_jobs` | Test cleaning up old jobs | Implemented |
| `test_persistence` | Test job persistence | Implemented |
| `test_job_priorities` | Test job priorities | To be implemented |
| `test_worker_integration` | Test worker integration | To be implemented |

#### Backend Tests (`test_backend.py`)

| Test Case | Description | Status |
|-----------|-------------|--------|
| `test_analyze_image` | Test analyzing an image | Implemented |
| `test_user_registration` | Test user registration | To be implemented |
| `test_user_login` | Test user login | To be implemented |
| `test_job_submission` | Test job submission | To be implemented |
| `test_job_status` | Test job status retrieval | To be implemented |
| `test_job_results` | Test job results retrieval | To be implemented |
| `test_authentication` | Test authentication | To be implemented |
| `test_authorization` | Test authorization | To be implemented |
| `test_file_upload` | Test file upload | To be implemented |
| `test_file_download` | Test file download | To be implemented |

### Integration Tests

Integration tests verify that components work together correctly.

| Test Case | Description | Status |
|-----------|-------------|--------|
| `test_engine_storage_integration` | Test engine and storage integration | To be implemented |
| `test_queue_worker_integration` | Test queue and worker integration | To be implemented |
| `test_backend_engine_integration` | Test backend and engine integration | To be implemented |
| `test_backend_queue_integration` | Test backend and queue integration | To be implemented |
| `test_full_analysis_workflow` | Test the full analysis workflow | To be implemented |
| `test_full_encoding_workflow` | Test the full encoding workflow | To be implemented |

### End-to-End Tests

End-to-end tests verify that the entire system works correctly from a user's perspective.

| Test Case | Description | Status |
|-----------|-------------|--------|
| `test_web_image_upload` | Test image upload via web interface | To be implemented |
| `test_web_analysis` | Test analysis via web interface | To be implemented |
| `test_web_encoding` | Test encoding via web interface | To be implemented |
| `test_desktop_image_upload` | Test image upload via desktop app | To be implemented |
| `test_desktop_analysis` | Test analysis via desktop app | To be implemented |
| `test_desktop_encoding` | Test encoding via desktop app | To be implemented |

## Test Environment

### Local Development

- Python 3.8+
- pytest for running tests
- Coverage.py for measuring test coverage

### Continuous Integration

- GitHub Actions for automated testing
- Run tests on multiple platforms (Windows, Linux, macOS)
- Run tests on multiple Python versions (3.8, 3.9, 3.10)

## Test Execution

### Running Unit Tests

```bash
# Run all tests
python -m unittest discover tests

# Run specific tests
python -m unittest tests/test_engine.py
python -m unittest tests/test_storage.py
python -m unittest tests/test_queue.py
python -m unittest tests/test_backend.py
```

### Running Integration Tests

```bash
# Run all integration tests
python -m unittest discover tests/integration

# Run specific integration tests
python -m unittest tests/integration/test_engine_storage.py
```

### Running End-to-End Tests

```bash
# Run all end-to-end tests
python -m unittest discover tests/e2e

# Run specific end-to-end tests
python -m unittest tests/e2e/test_web_interface.py
```

### Measuring Test Coverage

```bash
# Install coverage.py
pip install coverage

# Run tests with coverage
coverage run -m unittest discover tests

# Generate coverage report
coverage report
coverage html  # Generates HTML report
```

## Test Data

- Sample images for testing are stored in `tests/data/`
- Test data includes clean images and images with embedded steganography
- Different image formats (PNG, JPEG, BMP, etc.)

## Continuous Integration

- GitHub Actions workflow defined in `.github/workflows/tests.yml`
- Run tests on every push and pull request
- Generate and upload test coverage reports
