# StegnoX Desktop Application User Guide

## Introduction

StegnoX is a powerful tool for analyzing and working with steganography in images. This guide will help you get started with the StegnoX desktop application.

## Installation

### System Requirements

- Operating System: Windows 10/11, macOS 10.14+, or Linux (Ubuntu 18.04+)
- Processor: 2 GHz dual-core or better
- Memory: 4 GB RAM minimum, 8 GB recommended
- Disk Space: 500 MB free space
- Python: 3.8 or higher (included in the installer)

### Installation Steps

1. Download the installer for your operating system from the [StegnoX website](https://stegnox.com/download)
2. Run the installer and follow the on-screen instructions
3. Launch StegnoX from your applications menu or desktop shortcut

## Getting Started

### First Launch

When you first launch StegnoX, you will see the welcome screen with options to:
- Create a new project
- Open an existing project
- Import images for analysis
- Access tutorials and documentation

### Creating a Project

1. Click on "Create New Project" on the welcome screen or select "File > New Project" from the menu
2. Enter a name for your project
3. Select a location to save the project
4. Click "Create"

### Opening a Project

1. Click on "Open Existing Project" on the welcome screen or select "File > Open Project" from the menu
2. Browse to the project file (.stx)
3. Click "Open"

## User Interface

The StegnoX desktop application has a modern, intuitive interface divided into several areas:

### Main Toolbar

The main toolbar provides quick access to common actions:
- New Project
- Open Project
- Save Project
- Import Images
- Export Results
- Settings
- Help

### Navigation Panel

The navigation panel on the left side of the window allows you to switch between different views:
- Dashboard
- Image Analysis
- Encoding
- Batch Processing
- Results
- Settings

### Workspace

The workspace is the main area where you interact with images and view results.

### Status Bar

The status bar at the bottom of the window displays information about the current operation and system status.

## Analyzing Images

### Importing Images

1. Click on "Import Images" in the toolbar or select "File > Import Images" from the menu
2. Browse to the image file(s) you want to analyze
3. Click "Open"
4. The images will be added to your project and displayed in the workspace

### Running Analysis

1. Select an image in the workspace
2. Click on "Analyze" in the Image Analysis view
3. Select the analysis methods you want to run:
   - LSB Extraction
   - Parity Bit Extraction
   - Metadata Extraction
   - DCT Analysis
   - Bit Plane Analysis
   - Histogram Analysis
4. Click "Start Analysis"
5. A progress bar will show the analysis status
6. Once the analysis is complete, the results will be displayed

### Understanding Analysis Results

The analysis results are organized into tabs for each analysis method:

#### LSB Extraction

This tab shows the results of the Least Significant Bit extraction method:
- Extracted text (if any)
- Confidence level
- Visual representation of the LSB data
- Options to save the extracted data

#### Parity Bit Extraction

This tab shows the results of the parity bit extraction method:
- Extracted text (if any)
- Confidence level
- Visual representation of the parity bit data
- Options to save the extracted data

#### Metadata Extraction

This tab shows the metadata extracted from the image:
- Author
- Software used
- Creation date
- Other metadata fields
- Options to save the metadata

#### DCT Analysis

This tab shows the results of the Discrete Cosine Transform analysis:
- Assessment of whether DCT-based steganography is detected
- Confidence level
- Statistical information
- Visual representation of the DCT coefficients

#### Bit Plane Analysis

This tab shows the results of the bit plane analysis:
- Entropy values for each bit plane
- Assessment of each bit plane
- Visual representation of each bit plane
- Options to save the bit plane images

#### Histogram Analysis

This tab shows the results of the histogram analysis:
- Assessment of whether histogram anomalies are detected
- Statistical information
- Visual representation of the histogram
- Options to save the histogram data

### Saving Results

1. To save the analysis results, click on "Save Results" in the toolbar or select "File > Save Results" from the menu
2. Choose a location and format for the results (PDF, HTML, or JSON)
3. Click "Save"

## Encoding Messages

StegnoX allows you to hide messages in images using various steganography techniques.

### Selecting a Cover Image

1. Click on "Encoding" in the navigation panel
2. Click on "Import Cover Image" or drag and drop an image into the workspace
3. The image will be displayed in the workspace

### Encoding a Message

1. Enter the message you want to hide in the "Message" field
2. Select the encoding method from the dropdown menu:
   - LSB (Least Significant Bit)
   - Parity Bit
   - Metadata
3. Configure the encoding options (if available)
4. Click on "Encode"
5. A progress bar will show the encoding status
6. Once the encoding is complete, the encoded image will be displayed

### Saving the Encoded Image

1. Click on "Save Encoded Image" or select "File > Save Encoded Image" from the menu
2. Choose a location and format for the image (PNG recommended)
3. Click "Save"

## Batch Processing

StegnoX allows you to analyze or encode multiple images at once.

### Setting Up Batch Analysis

1. Click on "Batch Processing" in the navigation panel
2. Click on "Add Images" or drag and drop multiple images into the workspace
3. Select the analysis methods you want to run
4. Configure the batch processing options:
   - Output directory
   - Result format
   - Parallel processing options
5. Click on "Start Batch Analysis"
6. A progress bar will show the overall progress and current image being processed
7. Once the batch processing is complete, a summary will be displayed

### Setting Up Batch Encoding

1. Click on "Batch Processing" in the navigation panel
2. Click on "Add Images" or drag and drop multiple images into the workspace
3. Select "Batch Encoding" from the mode dropdown
4. Enter the message you want to hide
5. Select the encoding method
6. Configure the batch processing options:
   - Output directory
   - Image format
   - Parallel processing options
7. Click on "Start Batch Encoding"
8. A progress bar will show the overall progress and current image being processed
9. Once the batch processing is complete, a summary will be displayed

## Settings

### Application Settings

1. Click on "Settings" in the navigation panel or select "Tools > Settings" from the menu
2. In the General tab, you can configure:
   - Theme (light or dark)
   - Language
   - Default project location
   - Automatic updates

### Analysis Settings

1. In the Analysis tab, you can configure:
   - Default analysis methods
   - Analysis parameters
   - Result visualization options

### Encoding Settings

1. In the Encoding tab, you can configure:
   - Default encoding method
   - Encoding parameters
   - Output format options

### Advanced Settings

1. In the Advanced tab, you can configure:
   - Parallel processing options
   - Memory usage limits
   - Temporary file handling
   - Logging options

## Troubleshooting

### Common Issues

#### Application Crashes

- Ensure your system meets the minimum requirements
- Update to the latest version of StegnoX
- Check the log files in the application data directory

#### Analysis Fails

- Ensure the image is in a supported format
- Check that the image is not corrupted
- Try analyzing with fewer methods enabled

#### Encoding Fails

- Ensure the message is not too long for the selected encoding method
- Try a different encoding method
- Use a larger cover image

### Log Files

StegnoX creates log files that can help diagnose issues:
1. Click on "Help > Show Log Files" in the menu
2. The log files directory will open
3. Look for the most recent log file

### Getting Help

If you encounter any issues not covered in this guide, please:
1. Check the FAQ section in the Help menu
2. Visit the StegnoX website at https://stegnox.com/support
3. Contact support at support@stegnox.com
