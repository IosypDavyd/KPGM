#!/usr/bin/env python
"""Authentication routes for KPGM"""

from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import uuid

from models.user import User
from app import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user"""
    try:
        data = request.get_json()
        
        if not data or not data.get('email') or not data.get('password'):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Check if user exists
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email already registered'}), 409
        
        # Create new user
        user = User(
            id=str(uuid.uuid4()),
            email=data['email'],
            username=data.get('username', data['email'].split('@')[0]),
            password_hash=generate_password_hash(data['password'])
        )
        
        db.session.add(user)
        db.session.commit()
        
        current_app.logger.info(f'New user registered: {user.email}')
        
        return jsonify({
            'message': 'User registered successfully',
            'user_id': user.id,
            'email': user.email
        }), 201
    
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Error in register: {str(e)}')
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    """Login user and return JWT token"""
    try:
        data = request.get_json()
        
        if not data or not data.get('email') or not data.get('password'):
            return jsonify({'error': 'Missing required fields'}), 400
        
        user = User.query.filter_by(email=data['email']).first()
        
        if not user or not check_password_hash(user.password_hash, data['password']):
            return jsonify({'error': 'Invalid email or password'}), 401
        
        # Create JWT token
        access_token = create_access_token(
            identity=user.id,
            expires_delta=current_app.config['JWT_ACCESS_TOKEN_EXPIRES']
        )
        
        current_app.logger.info(f'User logged in: {user.email}')
        
        return jsonify({
            'message': 'Login successful',
            'access_token': access_token,
            'user_id': user.id,
            'email': user.email
        }), 200
    
    except Exception as e:
        current_app.logger.error(f'Error in login: {str(e)}')
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/refresh', methods=['POST'])
def refresh():
    """Refresh JWT token"""
    try:
        data = request.get_json()
        
        if not data or not data.get('refresh_token'):
            return jsonify({'error': 'Missing refresh token'}), 400
        
        # In production, implement proper refresh token logic
        access_token = create_access_token(
            identity=data.get('user_id'),
            expires_delta=current_app.config['JWT_ACCESS_TOKEN_EXPIRES']
        )
        
        return jsonify({
            'access_token': access_token
        }), 200
    
    except Exception as e:
        current_app.logger.error(f'Error in refresh: {str(e)}')
        return jsonify({'error': str(e)}), 500
