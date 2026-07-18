#!/bin/bash
# Development startup script

set -e

echo "🚀 Starting KPGM Music Video Generator..."

# Create necessary directories
mkdir -p uploads
mkdir -p logs
mkdir -p /tmp/kpgm

# Check if Python dependencies are installed
if [ ! -d "venv" ]; then
    echo "📦 Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install/update Python dependencies
echo "📦 Installing Python dependencies..."
cd backend
pip install -q -r requirements.txt
cd ..

# Check FFmpeg
if ! command -v ffmpeg &> /dev/null; then
    echo "⚠️  FFmpeg not found. Please install FFmpeg:"
    echo "   Ubuntu/Debian: sudo apt-get install ffmpeg"
    echo "   macOS: brew install ffmpeg"
    exit 1
fi

echo "✅ All checks passed!"
echo ""
echo "🎯 To start the development servers, run in separate terminals:"
echo ""
echo "Terminal 1 (Backend):"
echo "  cd backend && python app.py"
echo ""
echo "Terminal 2 (Frontend):"
echo "  cd frontend && npm install && npm start"
echo ""
echo "Backend: http://localhost:5000"
echo "Frontend: http://localhost:3000"
