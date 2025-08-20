@echo off
echo Building LBAT Desktop Application for Windows...
echo.

echo Step 1: Installing Node.js dependencies...
call npm install
if %errorlevel% neq 0 (
    echo Error: Failed to install Node.js dependencies
    pause
    exit /b 1
)

echo Step 2: Installing Python backend dependencies...
cd python_backend
call pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Error: Failed to install Python dependencies
    pause
    exit /b 1
)
cd ..

echo Step 3: Building React application...
call npm run build
if %errorlevel% neq 0 (
    echo Error: Failed to build React application
    pause
    exit /b 1
)

echo Step 4: Building Electron application...
call npm run dist-win
if %errorlevel% neq 0 (
    echo Error: Failed to build Electron application
    pause
    exit /b 1
)

echo.
echo Build completed successfully!
echo The Windows installer can be found in the 'dist' folder.
echo.
pause
