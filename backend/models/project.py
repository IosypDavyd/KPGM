#!/usr/bin/env python
"""Project model for KPGM"""

from datetime import datetime
from app import db

class Project(db.Model):
    """Project model for music and video generation"""
    __tablename__ = 'projects'
    
    id = db.Column(db.String(36), primary_key=True)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False, index=True)
    name = db.Column(db.String(255), nullable=False)
    
    # Music configuration
    music_prompt = db.Column(db.Text, nullable=False)
    music_style = db.Column(db.String(50), nullable=False)
    duration = db.Column(db.Integer, default=60)  # seconds
    suno_id = db.Column(db.String(255), nullable=True)  # SUNO generation ID
    music_url = db.Column(db.String(255), nullable=True)
    
    # Video configuration
    video_enabled = db.Column(db.Boolean, default=True)
    video_style = db.Column(db.String(50), nullable=True)
    video_prompt = db.Column(db.Text, nullable=True)
    runway_id = db.Column(db.String(255), nullable=True)  # Runway generation ID
    video_url = db.Column(db.String(255), nullable=True)
    
    # Status tracking
    status = db.Column(db.String(20), default='pending')  # pending, processing, completed, failed
    progress = db.Column(db.Integer, default=0)  # 0-100
    error_message = db.Column(db.Text, nullable=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    completed_at = db.Column(db.DateTime, nullable=True)
    
    def __repr__(self):
        return f'<Project {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'status': self.status,
            'progress': self.progress,
            'music_url': self.music_url,
            'video_url': self.video_url,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
