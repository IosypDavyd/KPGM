#!/usr/bin/env python
"""API Routes for KPGM Music Video Generator"""

from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
import os
from datetime import datetime
import uuid

from services.suno_service import SunoService
from services.video_service import VideoService
from services.synthesis_service import SynthesisService
from models.project import Project
from app import db

api_bp = Blueprint('api', __name__)

# Initialize services
suno_service = SunoService()
video_service = VideoService()
synthesis_service = SynthesisService()

@api_bp.route('/generate', methods=['POST'])
@jwt_required()
def generate_music_video():
    """
    Generate music and video from text description
    
    Request JSON:
    {
        "text": "music description",
        "style": "genre",
        "duration": 60,
        "video": true,
        "video_style": "cinematic",
        "project_name": "My Project"
    }
    """
    try:
        data = request.get_json()
        
        # Validation
        if not data or 'text' not in data:
            return jsonify({'error': 'Missing required field: text'}), 400
        
        user_id = get_jwt_identity()
        project_id = str(uuid.uuid4())
        
        # Create project
        project = Project(
            id=project_id,
            user_id=user_id,
            name=data.get('project_name', f'Project-{project_id[:8]}'),
            music_prompt=data.get('text'),
            music_style=data.get('style', 'ambient'),
            duration=data.get('duration', 60),
            video_enabled=data.get('video', True),
            video_style=data.get('video_style', 'cinematic'),
            status='processing'
        )
        db.session.add(project)
        db.session.commit()
        
        current_app.logger.info(f'Created project {project_id} for user {user_id}')
        
        return jsonify({
            'project_id': project_id,
            'status': 'processing',
            'message': 'Music and video generation started',
            'progress': 0
        }), 202
    
    except Exception as e:
        current_app.logger.error(f'Error in generate_music_video: {str(e)}')
        return jsonify({'error': str(e)}), 500

@api_bp.route('/generate/<project_id>/status', methods=['GET'])
@jwt_required()
def get_generation_status(project_id):
    """Get the status of a music/video generation project"""
    try:
        user_id = get_jwt_identity()
        project = Project.query.filter_by(id=project_id, user_id=user_id).first()
        
        if not project:
            return jsonify({'error': 'Project not found'}), 404
        
        return jsonify({
            'project_id': project_id,
            'status': project.status,
            'progress': project.progress,
            'music_url': project.music_url,
            'video_url': project.video_url,
            'created_at': project.created_at.isoformat(),
            'updated_at': project.updated_at.isoformat()
        }), 200
    
    except Exception as e:
        current_app.logger.error(f'Error in get_generation_status: {str(e)}')
        return jsonify({'error': str(e)}), 500

@api_bp.route('/projects', methods=['GET'])
@jwt_required()
def list_projects():
    """List all projects for the current user"""
    try:
        user_id = get_jwt_identity()
        projects = Project.query.filter_by(user_id=user_id).all()
        
        return jsonify({
            'projects': [
                {
                    'id': p.id,
                    'name': p.name,
                    'status': p.status,
                    'music_url': p.music_url,
                    'video_url': p.video_url,
                    'created_at': p.created_at.isoformat()
                }
                for p in projects
            ]
        }), 200
    
    except Exception as e:
        current_app.logger.error(f'Error in list_projects: {str(e)}')
        return jsonify({'error': str(e)}), 500

@api_bp.route('/projects/<project_id>', methods=['GET'])
@jwt_required()
def get_project(project_id):
    """Get detailed project information"""
    try:
        user_id = get_jwt_identity()
        project = Project.query.filter_by(id=project_id, user_id=user_id).first()
        
        if not project:
            return jsonify({'error': 'Project not found'}), 404
        
        return jsonify({
            'id': project.id,
            'name': project.name,
            'status': project.status,
            'progress': project.progress,
            'music_prompt': project.music_prompt,
            'music_style': project.music_style,
            'duration': project.duration,
            'music_url': project.music_url,
            'video_url': project.video_url,
            'created_at': project.created_at.isoformat(),
            'updated_at': project.updated_at.isoformat()
        }), 200
    
    except Exception as e:
        current_app.logger.error(f'Error in get_project: {str(e)}')
        return jsonify({'error': str(e)}), 500

@api_bp.route('/projects/<project_id>/download', methods=['GET'])
@jwt_required()
def download_project(project_id):
    """Download project assets (music + video)"""
    try:
        user_id = get_jwt_identity()
        project = Project.query.filter_by(id=project_id, user_id=user_id).first()
        
        if not project:
            return jsonify({'error': 'Project not found'}), 404
        
        if project.status != 'completed':
            return jsonify({'error': 'Project is not completed yet'}), 400
        
        return jsonify({
            'project_id': project_id,
            'music_url': project.music_url,
            'video_url': project.video_url,
            'download_ready': True
        }), 200
    
    except Exception as e:
        current_app.logger.error(f'Error in download_project: {str(e)}')
        return jsonify({'error': str(e)}), 500

@api_bp.route('/projects/<project_id>', methods=['DELETE'])
@jwt_required()
def delete_project(project_id):
    """Delete a project"""
    try:
        user_id = get_jwt_identity()
        project = Project.query.filter_by(id=project_id, user_id=user_id).first()
        
        if not project:
            return jsonify({'error': 'Project not found'}), 404
        
        db.session.delete(project)
        db.session.commit()
        
        return jsonify({'message': 'Project deleted successfully'}), 200
    
    except Exception as e:
        current_app.logger.error(f'Error in delete_project: {str(e)}')
        return jsonify({'error': str(e)}), 500

@api_bp.route('/music/styles', methods=['GET'])
def get_music_styles():
    """Get available music styles"""
    styles = [
        'ambient', 'electronic', 'pop', 'rock', 'hip-hop', 'jazz',
        'classical', 'indie', 'synthwave', 'lofi', 'metal', 'acoustic'
    ]
    return jsonify({'styles': styles}), 200

@api_bp.route('/video/styles', methods=['GET'])
def get_video_styles():
    """Get available video styles"""
    styles = [
        'cinematic', 'abstract', 'nature', 'urban', 'psychedelic',
        'minimalist', 'surreal', 'neon', 'retro', 'futuristic'
    ]
    return jsonify({'styles': styles}), 200
