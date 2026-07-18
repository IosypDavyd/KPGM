#!/usr/bin/env python
"""Video Generation Service using Runway ML and Stability AI"""

import requests
import json
import time
from typing import Dict, Optional
from flask import current_app
import logging

logger = logging.getLogger(__name__)

class VideoService:
    """Service for video generation using Runway ML or Stability AI"""
    
    def __init__(self):
        self.runway_api_key = current_app.config.get('RUNWAY_API_KEY') if current_app else None
        self.runway_base_url = current_app.config.get('RUNWAY_API_BASE_URL', 'https://api.runwayml.com') if current_app else None
        
        self.stability_api_key = current_app.config.get('STABILITY_API_KEY') if current_app else None
        self.stability_base_url = current_app.config.get('STABILITY_API_BASE_URL', 'https://api.stability.ai') if current_app else None
        
        self.timeout = 30
    
    def generate_video_runway(self,
                             prompt: str,
                             style: str = 'cinematic',
                             duration: int = 60) -> Optional[Dict]:
        """
        Generate video using Runway ML
        
        Args:
            prompt: Video description
            style: Visual style
            duration: Video duration in seconds
        
        Returns:
            Dictionary with generation ID and status
        """
        try:
            if not self.runway_api_key:
                raise ValueError('Runway API key not configured')
            
            headers = {
                'Authorization': f'Bearer {self.runway_api_key}',
                'Content-Type': 'application/json'
            }
            
            payload = {
                'prompt': prompt,
                'style': style,
                'duration': duration,
                'num_frames': duration * 24,  # 24 fps
                'model': 'gen3'
            }
            
            response = requests.post(
                f'{self.runway_base_url}/generate',
                json=payload,
                headers=headers,
                timeout=self.timeout
            )
            
            response.raise_for_status()
            data = response.json()
            
            logger.info(f'Runway video generation started: {data.get("id")}')
            
            return {
                'generation_id': data.get('id'),
                'status': 'processing',
                'provider': 'runway',
                'prompt': prompt,
                'style': style
            }
        
        except requests.exceptions.RequestException as e:
            logger.error(f'Runway API error: {str(e)}')
            raise
        except Exception as e:
            logger.error(f'Error in generate_video_runway: {str(e)}')
            raise
    
    def generate_video_stability(self,
                                prompt: str,
                                style: str = 'cinematic',
                                duration: int = 60) -> Optional[Dict]:
        """
        Generate video using Stability AI
        
        Args:
            prompt: Video description
            style: Visual style
            duration: Video duration in seconds
        
        Returns:
            Dictionary with generation ID and status
        """
        try:
            if not self.stability_api_key:
                raise ValueError('Stability API key not configured')
            
            headers = {
                'Authorization': f'Bearer {self.stability_api_key}',
                'Content-Type': 'application/json'
            }
            
            payload = {
                'prompt': prompt,
                'style': style,
                'duration': min(duration, 25),  # Stability has max 25 seconds
                'model': 'stable-video-diffusion-img2vid'
            }
            
            response = requests.post(
                f'{self.stability_base_url}/generation/text-to-video',
                json=payload,
                headers=headers,
                timeout=self.timeout
            )
            
            response.raise_for_status()
            data = response.json()
            
            logger.info(f'Stability video generation started: {data.get("id")}')
            
            return {
                'generation_id': data.get('id'),
                'status': 'processing',
                'provider': 'stability',
                'prompt': prompt,
                'style': style
            }
        
        except requests.exceptions.RequestException as e:
            logger.error(f'Stability API error: {str(e)}')
            raise
        except Exception as e:
            logger.error(f'Error in generate_video_stability: {str(e)}')
            raise
    
    def get_generation_status(self, generation_id: str, provider: str = 'runway') -> Optional[Dict]:
        """
        Check the status of a video generation
        
        Args:
            generation_id: Generation ID
            provider: 'runway' or 'stability'
        
        Returns:
            Dictionary with status and video URL if ready
        """
        try:
            if provider == 'runway':
                return self._get_runway_status(generation_id)
            elif provider == 'stability':
                return self._get_stability_status(generation_id)
            else:
                raise ValueError(f'Unknown provider: {provider}')
        
        except Exception as e:
            logger.error(f'Error in get_generation_status: {str(e)}')
            raise
    
    def _get_runway_status(self, generation_id: str) -> Optional[Dict]:
        """Get status from Runway API"""
        headers = {
            'Authorization': f'Bearer {self.runway_api_key}',
            'Content-Type': 'application/json'
        }
        
        response = requests.get(
            f'{self.runway_base_url}/generation/{generation_id}',
            headers=headers,
            timeout=self.timeout
        )
        
        response.raise_for_status()
        data = response.json()
        
        return {
            'generation_id': generation_id,
            'status': data.get('status'),
            'video_url': data.get('video_url'),
            'provider': 'runway'
        }
    
    def _get_stability_status(self, generation_id: str) -> Optional[Dict]:
        """Get status from Stability API"""
        headers = {
            'Authorization': f'Bearer {self.stability_api_key}',
            'Content-Type': 'application/json'
        }
        
        response = requests.get(
            f'{self.stability_base_url}/generation/{generation_id}',
            headers=headers,
            timeout=self.timeout
        )
        
        response.raise_for_status()
        data = response.json()
        
        return {
            'generation_id': generation_id,
            'status': data.get('status'),
            'video_url': data.get('video_url'),
            'provider': 'stability'
        }
    
    def wait_for_generation(self, generation_id: str, provider: str = 'runway', max_wait: int = 3600) -> Optional[Dict]:
        """
        Wait for a video generation to complete
        
        Args:
            generation_id: Generation ID
            provider: 'runway' or 'stability'
            max_wait: Maximum wait time in seconds
        
        Returns:
            Dictionary with completed generation info
        """
        start_time = time.time()
        poll_interval = 10
        
        while time.time() - start_time < max_wait:
            try:
                status = self.get_generation_status(generation_id, provider)
                
                if status['status'] == 'completed':
                    logger.info(f'Video generation completed: {generation_id}')
                    return status
                
                elif status['status'] == 'failed':
                    logger.error(f'Video generation failed: {generation_id}')
                    return status
                
                poll_interval = min(poll_interval + 5, 60)
                time.sleep(poll_interval)
            
            except Exception as e:
                logger.error(f'Error polling video generation: {str(e)}')
                time.sleep(poll_interval)
        
        raise TimeoutError(f'Video generation {generation_id} did not complete within {max_wait} seconds')
    
    def list_styles(self) -> list:
        """Get available video styles"""
        return [
            'cinematic', 'abstract', 'nature', 'urban', 'psychedelic',
            'minimalist', 'surreal', 'neon', 'retro', 'futuristic'
        ]
