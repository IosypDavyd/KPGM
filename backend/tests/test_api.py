#!/usr/bin/env python
"""Test API routes"""

import pytest
from app import create_app, db
from models.user import User
from models.project import Project
from werkzeug.security import generate_password_hash

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
def auth_token(client):
    """Create test user and get auth token"""
    user_data = {
        'email': 'test@example.com',
        'username': 'testuser',
        'password': 'TestPassword123'
    }
    client.post('/api/auth/register', json=user_data)
    response = client.post('/api/auth/login', json={
        'email': user_data['email'],
        'password': user_data['password']
    })
    return response.get_json()['access_token']

class TestAPI:
    """Test API endpoints"""
    
    def test_health_check(self, client):
        """Test health check endpoint"""
        response = client.get('/api/health')
        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'healthy'
    
    def test_info(self, client):
        """Test info endpoint"""
        response = client.get('/api/info')
        assert response.status_code == 200
        data = response.get_json()
        assert 'name' in data
        assert 'features' in data
    
    def test_get_music_styles(self, client):
        """Test getting music styles"""
        response = client.get('/api/music/styles')
        assert response.status_code == 200
        data = response.get_json()
        assert 'styles' in data
        assert isinstance(data['styles'], list)
    
    def test_get_video_styles(self, client):
        """Test getting video styles"""
        response = client.get('/api/video/styles')
        assert response.status_code == 200
        data = response.get_json()
        assert 'styles' in data
        assert isinstance(data['styles'], list)
    
    def test_generate_without_auth(self, client):
        """Test generate endpoint without authentication"""
        response = client.post('/api/generate', json={
            'text': 'test music'
        })
        assert response.status_code == 401
    
    def test_list_projects(self, client, auth_token):
        """Test list projects endpoint"""
        headers = {'Authorization': f'Bearer {auth_token}'}
        response = client.get('/api/projects', headers=headers)
        assert response.status_code == 200
        data = response.get_json()
        assert 'projects' in data
