# PowerShell script to build LBAT Desktop Application for Windows
# Run this script in PowerShell with execution policy: Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

Write-Host "Building LBAT Desktop Application for Windows..." -ForegroundColor Green
Write-Host ""

# Step 1: Install Node.js dependencies
Write-Host "Step 1: Installing Node.js dependencies..." -ForegroundColor Yellow
npm install
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: Failed to install Node.js dependencies" -ForegroundColor Red
    Read-Host "Press Enter to continue..."
    exit 1
}

# Step 2: Install Python backend dependencies
Write-Host "Step 2: Installing Python backend dependencies..." -ForegroundColor Yellow
Set-Location python_backend
pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: Failed to install Python dependencies" -ForegroundColor Red
    Read-Host "Press Enter to continue..."
    exit 1
}
Set-Location ..

# Step 3: Build React application
Write-Host "Step 3: Building React application..." -ForegroundColor Yellow
npm run build
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: Failed to build React application" -ForegroundColor Red
    Read-Host "Press Enter to continue..."
    exit 1
}

# Step 4: Build Electron application
Write-Host "Step 4: Building Electron application..." -ForegroundColor Yellow
npm run dist-win
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: Failed to build Electron application" -ForegroundColor Red
    Read-Host "Press Enter to continue..."
    exit 1
}

Write-Host ""
Write-Host "Build completed successfully!" -ForegroundColor Green
Write-Host "The Windows installer can be found in the 'dist' folder." -ForegroundColor Green
Write-Host ""
Read-Host "Press Enter to continue..."
