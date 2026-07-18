#!/usr/bin/env python
"""Validators for KPGM"""

import re
from typing import Tuple, List

def validate_email(email: str) -> Tuple[bool, str]:
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.match(pattern, email):
        return True, ''
    return False, 'Invalid email format'

def validate_username(username: str) -> Tuple[bool, str]:
    """Validate username"""
    if len(username) < 3:
        return False, 'Username must be at least 3 characters'
    if len(username) > 30:
        return False, 'Username must be at most 30 characters'
    if not re.match(r'^[a-zA-Z0-9_-]+$', username):
        return False, 'Username can only contain letters, numbers, underscores, and hyphens'
    return True, ''

def validate_password(password: str) -> Tuple[bool, str]:
    """Validate password strength"""
    if len(password) < 8:
        return False, 'Password must be at least 8 characters'
    if not re.search(r'[a-z]', password):
        return False, 'Password must contain lowercase letters'
    if not re.search(r'[A-Z]', password):
        return False, 'Password must contain uppercase letters'
    if not re.search(r'[0-9]', password):
        return False, 'Password must contain numbers'
    return True, ''

def validate_duration(duration: int) -> Tuple[bool, str]:
    """Validate duration"""
    if not isinstance(duration, int):
        return False, 'Duration must be an integer'
    if duration < 10:
        return False, 'Duration must be at least 10 seconds'
    if duration > 600:
        return False, 'Duration must be at most 600 seconds (10 minutes)'
    return True, ''

def validate_text(text: str, min_length: int = 10, max_length: int = 1000) -> Tuple[bool, str]:
    """Validate text input"""
    if not isinstance(text, str):
        return False, 'Text must be a string'
    if len(text) < min_length:
        return False, f'Text must be at least {min_length} characters'
    if len(text) > max_length:
        return False, f'Text must be at most {max_length} characters'
    return True, ''

def validate_file_extension(filename: str, allowed_extensions: List[str]) -> Tuple[bool, str]:
    """Validate file extension"""
    ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
    if ext not in allowed_extensions:
        return False, f'File extension must be one of: {', '.join(allowed_extensions)}'
    return True, ''
