#!/usr/bin/env python
"""Test utility functions"""

import pytest
from utils.validators import (
    validate_email,
    validate_username,
    validate_password,
    validate_duration,
    validate_text
)

class TestValidators:
    """Test validator functions"""
    
    def test_validate_email_valid(self):
        """Test valid email validation"""
        valid, msg = validate_email('test@example.com')
        assert valid is True
        assert msg == ''
    
    def test_validate_email_invalid(self):
        """Test invalid email validation"""
        valid, msg = validate_email('invalid-email')
        assert valid is False
    
    def test_validate_username_valid(self):
        """Test valid username"""
        valid, msg = validate_username('testuser')
        assert valid is True
    
    def test_validate_username_too_short(self):
        """Test username too short"""
        valid, msg = validate_username('ab')
        assert valid is False
    
    def test_validate_password_valid(self):
        """Test valid password"""
        valid, msg = validate_password('TestPassword123')
        assert valid is True
    
    def test_validate_password_too_weak(self):
        """Test weak password"""
        valid, msg = validate_password('weak')
        assert valid is False
    
    def test_validate_duration_valid(self):
        """Test valid duration"""
        valid, msg = validate_duration(60)
        assert valid is True
    
    def test_validate_duration_too_short(self):
        """Test duration too short"""
        valid, msg = validate_duration(5)
        assert valid is False
    
    def test_validate_text_valid(self):
        """Test valid text"""
        valid, msg = validate_text('This is a valid description for music')
        assert valid is True
    
    def test_validate_text_too_short(self):
        """Test text too short"""
        valid, msg = validate_text('short')
        assert valid is False
