#!/usr/bin/env python
"""SUNO API Service for music generation"""

import requests
import json
import time
from typing import Dict, Optional
from flask import current_app
import logging

logger = logging.getLogger(__name__)

class SunoService:
    """Service for interacting with SUNO API"""
    
    def __init__(self):
        self.api_key = current_app.config.get('SUNO_API_KEY') if current_app else None
        self.base_url = current_app.config.get('SUNO_API_BASE_URL', 'https://api.suno.ai') if current_app else None
        self.timeout = 30
    
    def generate_music(self, 
                      prompt: str, 
                      style: str = 'ambient',
                      duration: int = 60) -> Optional[Dict]:
        """
        Generate music using SUNO API
        
        Args:
            prompt: Music description
            style: Music genre/style
            duration: Duration in seconds
        
        Returns:
            Dictionary with generation ID and status
        """
        try:
            if not self.api_key:
                raise ValueError('SUNO API key not configured')
            
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            payload = {
                'prompt': prompt,
                'style': style,
                'duration': duration,
                'model': 'chirp-v3'
            }
            
            response = requests.post(
                f'{self.base_url}/generate',
                json=payload,
                headers=headers,
                timeout=self.timeout
            )
            
            response.raise_for_status()
            data = response.json()
            
            logger.info(f'SUNO generation started: {data.get("id")}')
            
            return {
                'generation_id': data.get('id'),
                'status': 'processing',
                'prompt': prompt,
                'style': style
            }
        
        except requests.exceptions.RequestException as e:
            logger.error(f'SUNO API error: {str(e)}')
            raise
        except Exception as e:
            logger.error(f'Error in generate_music: {str(e)}')
            raise
    
    def get_generation_status(self, generation_id: str) -> Optional[Dict]:
        """
        Check the status of a music generation
        
        Args:
            generation_id: SUNO generation ID
        
        Returns:
            Dictionary with status and music URL if ready
        """
        try:
            if not self.api_key:
                raise ValueError('SUNO API key not configured')
            
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            response = requests.get(
                f'{self.base_url}/generation/{generation_id}',
                headers=headers,
                timeout=self.timeout
            )
            
            response.raise_for_status()
            data = response.json()
            
            return {
                'generation_id': generation_id,
                'status': data.get('status'),  # processing, completed, failed
                'music_url': data.get('audio_url'),
                'title': data.get('title'),
                'duration': data.get('duration')
            }
        
        except requests.exceptions.RequestException as e:
            logger.error(f'SUNO API error: {str(e)}')
            raise
        except Exception as e:
            logger.error(f'Error in get_generation_status: {str(e)}')
            raise
    
    def wait_for_generation(self, generation_id: str, max_wait: int = 3600) -> Optional[Dict]:
        """
        Wait for a music generation to complete
        
        Args:
            generation_id: SUNO generation ID
            max_wait: Maximum wait time in seconds
        
        Returns:
            Dictionary with completed generation info
        """
        start_time = time.time()
        poll_interval = 5  # Start with 5 seconds
        
        while time.time() - start_time < max_wait:
            try:
                status = self.get_generation_status(generation_id)
                
                if status['status'] == 'completed':
                    logger.info(f'Generation completed: {generation_id}')
                    return status
                
                elif status['status'] == 'failed':
                    logger.error(f'Generation failed: {generation_id}')
                    return status
                
                # Increase poll interval over time
                poll_interval = min(poll_interval + 2, 30)
                time.sleep(poll_interval)
            
            except Exception as e:
                logger.error(f'Error polling generation: {str(e)}')
                time.sleep(poll_interval)
        
        raise TimeoutError(f'Generation {generation_id} did not complete within {max_wait} seconds')
    
    def list_styles(self) -> list:
        """Get available music styles"""
        return [
            'ambient', 'electronic', 'pop', 'rock', 'hip-hop', 'jazz',
            'classical', 'indie', 'synthwave', 'lofi', 'metal', 'acoustic'
        ]
