#!/bin/bash

# RIS Reference Sorter Setup Script
# This script sets up the application and runs it

echo "🔬 RIS Reference Sorter Setup"
echo "=============================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.7 or higher."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Check if pip is installed
if ! command -v pip3 &> /dev/null && ! command -v pip &> /dev/null; then
    echo "❌ pip is not installed. Please install pip."
    exit 1
fi

echo "✅ pip found"

# Install dependencies
echo "📦 Installing dependencies..."
if command -v pip3 &> /dev/null; then
    pip3 install -r requirements.txt
else
    pip install -r requirements.txt
fi

if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

# Create uploads directory if it doesn't exist
if [ ! -d "uploads" ]; then
    mkdir uploads
    echo "✅ Created uploads directory"
fi

echo ""
echo "🚀 Setup complete! Starting the application..."
echo ""
echo "📝 The application will be available at: http://localhost:5000"
echo "📝 Press Ctrl+C to stop the application"
echo ""

# Run the Flask application
python3 app.py 