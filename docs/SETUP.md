# KPGM Setup Guide

## Prerequisites

- Python 3.9 or higher
- Node.js 16 or higher
- FFmpeg
- Git

## Installation

### 1. Clone Repository

```bash
git clone https://github.com/IosypDavyd/KPGM.git
cd KPGM
git checkout music-video-generator
```

### 2. Backend Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
cd backend
pip install -r requirements.txt

# Create .env file
cp ../.env.example ../.env
```

### 3. Frontend Setup

```bash
# Install Node dependencies
cd frontend
npm install
```

### 4. Configuration

Edit `.env` file and add your API keys:

```env
# SUNO API
SUNO_API_KEY=your_suno_api_key

# Runway ML API
RUNWAY_API_KEY=your_runway_api_key

# Stability AI API
STABILITY_API_KEY=your_stability_api_key

# JWT Secret
JWT_SECRET=your_jwt_secret_key
SECRET_KEY=your_secret_key
```

### 5. Database Setup

```bash
cd backend
python
>>> from app import create_app, db
>>> app = create_app()
>>> with app.app_context():
>>>     db.create_all()
>>> exit()
```

### 6. FFmpeg Installation

**Ubuntu/Debian:**
```bash
sudo apt-get install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

**Windows:**
Download from https://ffmpeg.org/download.html

## Running the Application

### Terminal 1: Backend

```bash
cd backend
python app.py
# Server running on http://localhost:5000
```

### Terminal 2: Frontend

```bash
cd frontend
npm start
# App running on http://localhost:3000
```

## Getting API Keys

### SUNO AI

1. Visit https://www.suno.ai
2. Sign up and go to API settings
3. Generate API key
4. Add to `.env`

### Runway ML

1. Visit https://www.runwayml.com
2. Create account
3. Go to API section
4. Generate API key
5. Add to `.env`

### Stability AI

1. Visit https://platform.stability.ai
2. Sign up
3. Go to API keys
4. Create new key
5. Add to `.env`

## Troubleshooting

### FFmpeg not found

Add FFmpeg to your system PATH or update `FFMPEG_PATH` in `.env`

### API Key errors

Ensure all API keys are correctly added to `.env` file

### Port already in use

Change port in `.env`:
```env
API_PORT=5001
```

### Database errors

Delete `kpgm.db` and recreate:
```bash
rm kpgm.db
python
>>> from app import create_app, db
>>> app = create_app()
>>> with app.app_context():
>>>     db.create_all()
>>> exit()
```
