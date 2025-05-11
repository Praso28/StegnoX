# StegnoX Engine

The StegnoX Engine is the core component of the StegnoX application, providing advanced steganography detection and encoding capabilities.

## Features

### Detection Methods

The engine includes several methods for detecting hidden data in images:

1. **LSB Extraction**: Extracts data hidden in the least significant bits of pixel values.
2. **Parity Bit Analysis**: Analyzes parity patterns in pixel values to detect hidden data.
3. **Metadata Extraction**: Extracts and analyzes image metadata for hidden information.
4. **DCT Analysis**: Analyzes Discrete Cosine Transform coefficients for signs of steganography (especially in JPEG images).
5. **Bit Plane Analysis**: Examines individual bit planes for statistical anomalies.
6. **Histogram Analysis**: Analyzes image histograms for patterns indicative of steganography.

### Encoding Methods

The engine also provides methods for hiding data in images:

1. **LSB Encoding**: Hides data in the least significant bits of pixel values.
2. **Parity Bit Encoding**: Modifies pixel values to achieve desired parity based on message bits.
3. **Metadata Encoding**: Hides data in image metadata.

## Usage

### Basic Usage

```python
from engine.stegnox_engine import StegnoxEngine

# Create an instance of the engine
engine = StegnoxEngine()

# Analyze an image with all methods
results = engine.extract_all_methods("path/to/image.png")

# Use a specific detection method
lsb_result = engine.lsb_extraction("path/to/image.png")
dct_result = engine.dct_analysis("path/to/image.png")

# Encode a message
engine.lsb_encoding("path/to/cover.png", "Secret message", "path/to/output.png")
```

### Command Line Demo

You can use the provided demo script to test the engine:

```bash
python examples/engine_demo.py --action analyze --image path/to/image.png

python examples/engine_demo.py --action encode --method lsb --image path/to/cover.png --message "Secret message" --output path/to/output.png

python examples/engine_demo.py --action decode --method lsb --image path/to/output.png
```

## Development

### Adding New Methods

To add a new detection or encoding method:

1. Add the method to the `StegnoxEngine` class
2. Add the method to the `self.methods` list in `__init__`
3. Add tests for the new method in `tests/test_engine.py`

### Testing

Run the tests to ensure all methods are working correctly:

```bash
python -m unittest tests/test_engine.py
```
