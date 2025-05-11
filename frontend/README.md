# StegnoX Frontend

The StegnoX Frontend is a React-based web application that provides a user interface for the StegnoX steganography analysis tool.

## Features

- **User Authentication**: Register, login, and manage user profiles
- **Image Analysis**: Upload and analyze images for hidden data
- **Message Encoding**: Hide messages in images using various steganography techniques
- **Job Management**: Create, monitor, and manage analysis jobs
- **Results Visualization**: View and interpret analysis results

## Directory Structure

```
frontend/
├── src/                # Source code
│   ├── assets/         # Static assets (images, icons, etc.)
│   ├── components/     # Reusable UI components
│   ├── context/        # React context providers
│   ├── pages/          # Page components
│   ├── services/       # API service functions
│   ├── styles/         # CSS styles
│   ├── utils/          # Utility functions
│   ├── App.js          # Main application component
│   └── index.js        # Application entry point
├── public/             # Public assets
└── package.json        # Project dependencies
```

## Components

### Pages

- **HomePage**: Landing page with information about the application
- **LoginPage**: User login form
- **RegisterPage**: User registration form
- **DashboardPage**: User dashboard with quick actions and recent jobs
- **AnalyzePage**: Upload and analyze images for steganography
- **EncodePage**: Hide messages in images
- **JobsPage**: List and manage analysis jobs
- **JobDetailPage**: View detailed information about a specific job
- **ProfilePage**: User profile management

### Reusable Components

- **Navbar**: Navigation bar with authentication state
- **Footer**: Application footer with links
- **FileUpload**: Drag-and-drop file upload component
- **AnalysisResults**: Display and visualize analysis results
- **JobList**: Display and manage job listings

## Services

- **api.js**: Base API configuration with authentication
- **authService.js**: Authentication API functions
- **jobService.js**: Job management API functions
- **analysisService.js**: Image analysis and encoding API functions

## Context

- **AuthContext**: Authentication state management

## Installation

1. Install dependencies:
   ```
   npm install
   ```

2. Start the development server:
   ```
   npm start
   ```

## Building for Production

```
npm run build
```

## Development

### Adding a New Page

1. Create a new component in the `pages` directory
2. Add the route to `App.js`
3. Update the navigation if needed

### Adding a New Component

1. Create a new component in the `components` directory
2. Import and use it in your pages

### Adding a New API Service

1. Create a new service file in the `services` directory
2. Import and use it in your components

## API Integration

The frontend communicates with the StegnoX backend API. All API calls are made through the service functions, which handle authentication and error handling.

## Authentication

Authentication is managed through the AuthContext provider. It handles:

- User login and registration
- Token storage and management
- Protected route access
- User state across the application
