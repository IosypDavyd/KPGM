#!/usr/bin/env python
"""Database migration script"""

import os
from pathlib import Path

def create_directories():
    """Create necessary directories"""
    dirs = [
        'uploads',
        'logs',
        'backend/tests',
        'frontend/src/components',
        'frontend/src/pages'
    ]
    for d in dirs:
        Path(d).mkdir(parents=True, exist_ok=True)
        print(f'✓ Created directory: {d}')

def init_database():
    """Initialize database"""
    try:
        from backend.app import create_app, db
        app = create_app()
        with app.app_context():
            db.create_all()
            print('✓ Database initialized')
    except Exception as e:
        print(f'✗ Error initializing database: {e}')

if __name__ == '__main__':
    print('🔧 Initializing KPGM...')
    create_directories()
    print('\n✅ Initialization complete!')
