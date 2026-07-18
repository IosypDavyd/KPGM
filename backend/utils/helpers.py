#!/usr/bin/env python
"""Utility functions for KPGM"""

import os
import json
import hashlib
import uuid
from datetime import datetime
from functools import wraps
import logging

logger = logging.getLogger(__name__)

def generate_id():
    """Generate unique ID"""
    return str(uuid.uuid4())

def get_file_hash(file_path):
    """Calculate SHA256 hash of file"""
    sha256_hash = hashlib.sha256()
    with open(file_path, 'rb') as f:
        for byte_block in iter(lambda: f.read(4096), b''):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def format_size(bytes):
    """Format bytes to human-readable size"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes < 1024.0:
            return f"{bytes:.2f} {unit}"
        bytes /= 1024.0
    return f"{bytes:.2f} TB"

def ensure_dir(path):
    """Ensure directory exists"""
    os.makedirs(path, exist_ok=True)
    return path

def remove_file(path):
    """Safely remove file"""
    try:
        if os.path.exists(path):
            os.remove(path)
            return True
    except Exception as e:
        logger.error(f'Error removing file {path}: {str(e)}')
    return False

def load_json(file_path):
    """Load JSON file"""
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f'Error loading JSON {file_path}: {str(e)}')
        return None

def save_json(data, file_path):
    """Save JSON file"""
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except Exception as e:
        logger.error(f'Error saving JSON {file_path}: {str(e)}')
        return False

def retry(max_attempts=3, delay=1):
    """Decorator for retry logic"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise
                    logger.warning(f'Attempt {attempt + 1} failed: {str(e)}. Retrying...')
                    import time
                    time.sleep(delay)
            return None
        return wrapper
    return decorator

def timestamp():
    """Get current timestamp"""
    return datetime.utcnow().isoformat()
