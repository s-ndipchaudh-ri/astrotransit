# LBAT Desktop Application

A desktop application for Location Based Astro Transit calculations, built with Electron and Python.

## Features

- **Native Desktop Experience**: Runs as a Windows desktop application
- **React Frontend**: Modern, responsive user interface
- **Python Backend**: Powerful astrological calculations using Swiss Ephemeris
- **Cross-Platform**: Works on Windows, macOS, and Linux
- **Offline Capable**: All calculations run locally
- **CSV Export**: Generate detailed astrological data files

## Architecture

```
LBAT Desktop
├── Electron (Main Process)
│   ├── Manages application window
│   ├── Handles file system operations
│   └── Communicates with Python backend
├── React Frontend (Renderer Process)
│   ├── User interface components
│   ├── Location selection
│   └── Results display
└── Python Backend
    ├── FastAPI server
    ├── Astrological calculations
    └── CSV generation
```

## Prerequisites

### Windows
- **Node.js** 18.0 or higher
- **Python** 3.11 or higher
- **Git** (for cloning the repository)

### macOS
- **Node.js** 18.0 or higher
- **Python** 3.11 or higher
- **Xcode Command Line Tools**

### Linux
- **Node.js** 18.0 or higher
- **Python** 3.11 or higher
- **Build essentials** (gcc, make, etc.)

## Installation

### 1. Clone the Repository
```bash
git clone <repository-url>
cd LBAT
```

### 2. Install Dependencies

#### Node.js Dependencies
```bash
npm install
```

#### Python Backend Dependencies
```bash
cd python_backend
pip install -r requirements.txt
cd ..
```

### 3. Development Mode

#### Start the Application
```bash
# Start React development server and Electron
npm run electron-dev
```

This will:
- Start the React development server on port 3000
- Launch Electron when React is ready
- Open the desktop application

#### Alternative: Separate Development
```bash
# Terminal 1: Start React
npm start

# Terminal 2: Start Electron
npm run electron
```

### 4. Building for Distribution

#### Windows
```bash
# Use the automated build script
build_windows.bat

# Or manually
npm run dist-win
```

#### macOS
```bash
npm run dist-mac
```

#### Linux
```bash
npm run dist-linux
```

#### All Platforms
```bash
npm run dist
```

## Project Structure

```
LBAT/
├── public/
│   ├── electron.js          # Electron main process
│   ├── preload.js           # Secure API bridge
│   └── index.html           # React entry point
├── src/                     # React components
├── python_backend/
│   ├── main.py              # FastAPI backend server
│   ├── requirements.txt     # Python dependencies
│   └── outputs/             # Generated CSV files
├── package.json             # Node.js configuration
├── build_windows.bat        # Windows build script
└── dist/                    # Built application (after build)
```

## Configuration

### Environment Variables

The application uses these environment variables:

- `PORT`: Backend server port (default: 8000)
- `HOST`: Backend server host (default: 127.0.0.1)
- `NODE_ENV`: Set to 'development' for dev mode

### Backend Configuration

The Python backend runs on `http://127.0.0.1:8000` by default. You can modify this in `python_backend/main.py`.

## Usage

### 1. Launch the Application
- Double-click the built executable
- Or run `npm run electron-dev` in development

### 2. Select Location
- Choose from preset locations (including Vashind Shahapur)
- Or enter custom coordinates

### 3. Choose Date
- Single date calculation
- Date range calculation

### 4. View Results
- Ascendant details
- Nakshatra information
- KP sub-lords
- Degree buckets (optional)

### 5. Export Data
- Generate CSV files
- Save to custom location

## Development

### Adding New Features

#### Frontend (React)
- Add components in `src/components/`
- Update routing in `src/App.js`
- Modify styles in component files

#### Backend (Python)
- Add new endpoints in `python_backend/main.py`
- Update Pydantic models as needed
- Add new calculation functions

#### Electron
- Modify `public/electron.js` for main process changes
- Update `public/preload.js` for new APIs
- Add new IPC handlers as needed

### Testing

#### Frontend Tests
```bash
npm test
```

#### Backend Tests
```bash
cd python_backend
python -m pytest
```

### Debugging

#### Electron DevTools
- Press `F12` or `Ctrl+Shift+I` to open DevTools
- Available in development mode

#### Backend Logging
- Check console output for Python backend logs
- Logs are written to console in development

## Troubleshooting

### Common Issues

#### 1. Python Backend Won't Start
- Check Python version (3.11+ required)
- Verify all dependencies are installed
- Check port 8000 is available

#### 2. Build Failures
- Ensure Node.js 18+ is installed
- Clear `node_modules` and reinstall
- Check Python path in build scripts

#### 3. Runtime Errors
- Check console output for error messages
- Verify ephemeris files are present
- Check file permissions

### Getting Help

1. Check the console output for error messages
2. Verify all prerequisites are met
3. Check the project issues page
4. Review the logs in the application

## Distribution

### Windows
- Creates an NSIS installer
- Includes Python runtime
- Installs to Program Files

### macOS
- Creates a DMG file
- Includes Python runtime
- Drag and drop installation

### Linux
- Creates an AppImage
- Portable application
- No installation required

## License

[Add your license information here]

## Contributing

[Add contribution guidelines here]

## Support

[Add support information here]
