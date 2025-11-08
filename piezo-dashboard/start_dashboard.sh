#!/bin/bash

echo "Starting Piezoelectric Energy Dashboard..."
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed or not in PATH."
    echo "Please install Python 3.7+ using your package manager"
    exit 1
fi

# Navigate to the dashboard directory
cd "$(dirname "$0")"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Start the server
echo
echo "========================================"
echo "  Piezoelectric Dashboard Starting!"
echo "========================================"
echo
echo "Dashboard will be available at:"
echo "  http://localhost:8000"
echo
echo "Press Ctrl+C to stop the server"
echo

cd backend
python main.py
