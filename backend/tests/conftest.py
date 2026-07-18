#!/usr/bin/env python
"""Test configuration"""

import pytest
import os

# Set test environment
os.environ['FLASK_ENV'] = 'testing'

@pytest.fixture(scope='session')
def test_config():
    """Provide test configuration"""
    return {
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'JWT_SECRET_KEY': 'test-secret-key',
        'SECRET_KEY': 'test-secret-key'
    }
