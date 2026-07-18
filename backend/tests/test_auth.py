#!/usr/bin/env python
"""Test authentication routes"""

import pytest
from app import create_app, db
from models.user import User

@pytest.fixture
def app():
    app = create_app('testing')
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def user_data():
    return {
        'email': 'test@example.com',
        'username': 'testuser',
        'password': 'TestPassword123'
    }

class TestAuth:
    """Test authentication endpoints"""
    
    def test_register(self, client, user_data):
        """Test user registration"""
        response = client.post('/api/auth/register', json=user_data)
        assert response.status_code == 201
        data = response.get_json()
        assert data['email'] == user_data['email']
    
    def test_register_duplicate_email(self, client, user_data):
        """Test registration with duplicate email"""
        client.post('/api/auth/register', json=user_data)
        response = client.post('/api/auth/register', json=user_data)
        assert response.status_code == 409
    
    def test_login(self, client, user_data):
        """Test user login"""
        client.post('/api/auth/register', json=user_data)
        response = client.post('/api/auth/login', json={
            'email': user_data['email'],
            'password': user_data['password']
        })
        assert response.status_code == 200
        data = response.get_json()
        assert 'access_token' in data
    
    def test_login_wrong_password(self, client, user_data):
        """Test login with wrong password"""
        client.post('/api/auth/register', json=user_data)
        response = client.post('/api/auth/login', json={
            'email': user_data['email'],
            'password': 'WrongPassword123'
        })
        assert response.status_code == 401
    
    def test_login_nonexistent_user(self, client):
        """Test login with nonexistent user"""
        response = client.post('/api/auth/login', json={
            'email': 'nonexistent@example.com',
            'password': 'Password123'
        })
        assert response.status_code == 401
