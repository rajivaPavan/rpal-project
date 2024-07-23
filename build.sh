#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Navigate to the directory containing your script
cd "$(dirname "$0")"
cd src

# Install PyInstaller if it's not already installed
if ! command -v pyinstaller &> /dev/null; then
    pip show pyinstaller &> /dev/null || pip install pyinstaller
fi

# Build the executable
pyinstaller --onefile --name myrpal myrpal.py

# Create the build directory if it doesn't exist
build_dir="../build"
[ -d "$build_dir" ] || mkdir -p "$build_dir"

# Remove the existing executable from the build directory
if [ -f "$build_dir/myrpal" ]; then
    rm "$build_dir/myrpal"
fi

# Move the executable to the build directory
mv dist/myrpal "$build_dir/"

# Clean up build files
rm -rf build dist myrpal.spec __pycache__

# Navigate back to the original directory
cd ..
