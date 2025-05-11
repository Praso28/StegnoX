# StegnoX Web Application User Guide

## Introduction

StegnoX is a powerful tool for analyzing and working with steganography in images. This guide will help you get started with the StegnoX web application.

## Getting Started

### Accessing the Application

The StegnoX web application can be accessed at:

```
http://localhost:5000
```

### Creating an Account

1. Click on the "Register" button in the top-right corner of the page
2. Enter your username, email, and password
3. Click "Register"
4. You will be redirected to the login page

### Logging In

1. Click on the "Login" button in the top-right corner of the page
2. Enter your username and password
3. Click "Login"
4. You will be redirected to the dashboard

## Dashboard

The dashboard provides an overview of your recent activities and quick access to the main features of StegnoX.

### Recent Jobs

The dashboard displays your most recent jobs, including:
- Job ID
- Job type (analysis or encoding)
- Status
- Creation date

Click on a job to view its details.

### Quick Actions

The dashboard provides quick access to the following actions:
- Analyze an image
- Encode a message
- View all jobs

## Analyzing Images

StegnoX provides powerful tools for analyzing images for steganography.

### Uploading an Image

1. Click on "Analyze" in the navigation menu
2. Click on the upload area or drag and drop an image
3. The image will be uploaded and displayed

### Running Analysis

1. After uploading an image, click on the "Analyze" button
2. StegnoX will create an analysis job and start processing the image
3. You will see a progress indicator while the analysis is running
4. Once the analysis is complete, the results will be displayed

### Understanding Analysis Results

The analysis results are organized into sections for each analysis method:

#### LSB Extraction

This section shows the results of the Least Significant Bit extraction method:
- Extracted text (if any)
- Confidence level
- Visual representation of the LSB data

#### Parity Bit Extraction

This section shows the results of the parity bit extraction method:
- Extracted text (if any)
- Confidence level
- Visual representation of the parity bit data

#### Metadata Extraction

This section shows the metadata extracted from the image:
- Author
- Software used
- Creation date
- Other metadata fields

#### DCT Analysis

This section shows the results of the Discrete Cosine Transform analysis:
- Assessment of whether DCT-based steganography is detected
- Confidence level
- Statistical information

#### Bit Plane Analysis

This section shows the results of the bit plane analysis:
- Entropy values for each bit plane
- Assessment of each bit plane
- Visual representation of each bit plane

#### Histogram Analysis

This section shows the results of the histogram analysis:
- Assessment of whether histogram anomalies are detected
- Statistical information
- Visual representation of the histogram

### Saving and Sharing Results

1. To save the analysis results, click on the "Save" button
2. To share the results, click on the "Share" button and copy the link

## Encoding Messages

StegnoX allows you to hide messages in images using various steganography techniques.

### Uploading a Cover Image

1. Click on "Encode" in the navigation menu
2. Click on the upload area or drag and drop an image
3. The image will be uploaded and displayed

### Encoding a Message

1. Enter the message you want to hide in the "Message" field
2. Select the encoding method from the dropdown menu:
   - LSB (Least Significant Bit)
   - Parity Bit
   - Metadata
3. Click on the "Encode" button
4. StegnoX will create an encoding job and start processing the image
5. You will see a progress indicator while the encoding is running
6. Once the encoding is complete, you can download the encoded image

### Downloading the Encoded Image

1. After the encoding is complete, click on the "Download" button
2. The encoded image will be downloaded to your computer

## Managing Jobs

StegnoX provides a job management system to track your analysis and encoding tasks.

### Viewing All Jobs

1. Click on "Jobs" in the navigation menu
2. You will see a list of all your jobs, including:
   - Job ID
   - Job type (analysis or encoding)
   - Status
   - Creation date
   - Last update date

### Filtering Jobs

1. Use the filter options at the top of the jobs list to filter by:
   - Job type (analysis or encoding)
   - Status (pending, processing, completed, failed, cancelled)
   - Date range

### Viewing Job Details

1. Click on a job in the list to view its details
2. For analysis jobs, you will see the analysis results
3. For encoding jobs, you will see the encoding details and a download link for the encoded image

### Cancelling Jobs

1. To cancel a pending or processing job, click on the job in the list
2. Click on the "Cancel" button in the job details page
3. Confirm the cancellation

## User Profile

### Viewing Your Profile

1. Click on your username in the top-right corner of the page
2. Select "Profile" from the dropdown menu

### Updating Your Profile

1. On your profile page, click on the "Edit" button
2. Update your information
3. Click "Save"

### Changing Your Password

1. On your profile page, click on the "Change Password" button
2. Enter your current password
3. Enter your new password
4. Confirm your new password
5. Click "Save"

## Settings

### Accessing Settings

1. Click on your username in the top-right corner of the page
2. Select "Settings" from the dropdown menu

### Application Settings

1. In the settings page, you can configure:
   - Theme (light or dark)
   - Language
   - Notification preferences

### API Access

1. In the settings page, click on the "API Access" tab
2. You can view your API key and generate a new one
3. You can also view API usage statistics

## Troubleshooting

### Common Issues

#### Image Upload Fails

- Ensure the image is in a supported format (PNG, JPEG, BMP)
- Check that the image file size is within the limits (max 10MB)
- Try a different browser or clear your browser cache

#### Analysis Takes Too Long

- Large images may take longer to analyze
- Complex steganography methods may require more processing time
- Check your internet connection

#### Encoding Fails

- Ensure the message is not too long for the selected encoding method
- Try a different encoding method
- Use a larger cover image

### Getting Help

If you encounter any issues not covered in this guide, please:
1. Check the FAQ section
2. Contact support at support@stegnox.com
3. Visit the StegnoX community forum at https://community.stegnox.com
