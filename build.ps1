# Exit immediately if a command exits with a non-zero status
$ErrorActionPreference = "Stop"

# Navigate to the directory containing your script
Set-Location -Path (Split-Path -Path $MyInvocation.MyCommand.Definition -Parent)
Set-Location -Path "src"

# Install PyInstaller if it's not already installed
if (-not (Get-Command pyinstaller -ErrorAction SilentlyContinue)) {
    pip show pyinstaller -ErrorAction SilentlyContinue | Out-Null
    if ($LASTEXITCODE -ne 0) {
        pip install pyinstaller
    }
}

# Build the executable
pyinstaller --onefile --name myrpal myrpal.py

# Create the build directory if it doesn't exist
$buildDir = "../build"
if (-not (Test-Path -Path $buildDir)) {
    New-Item -Path $buildDir -ItemType Directory | Out-Null
}

# Remove the existing executable from the build directory
if (Test-Path -Path "$buildDir/myrpal.exe") {
    Remove-Item -Path "$buildDir/myrpal.exe"
}

# Move the executable to the build directory
Move-Item -Path "dist/myrpal.exe" -Destination $buildDir

# Clean up build files
Remove-Item -Recurse -Force "build", "dist", "myrpal.spec", "__pycache__"

# Navigate back to the original directory
Set-Location -Path ".."
