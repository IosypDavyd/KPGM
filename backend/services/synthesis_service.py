#!/usr/bin/env python
"""Audio-Video Synthesis Service"""

import os
import subprocess
import logging
from typing import Optional, Dict
from pathlib import Path

logger = logging.getLogger(__name__)

class SynthesisService:
    """Service for synchronizing and merging audio and video"""
    
    def __init__(self, ffmpeg_path: str = None):
        self.ffmpeg_path = ffmpeg_path or '/usr/bin/ffmpeg'
        self.timeout = 3600  # 1 hour
    
    def merge_audio_video(self,
                         audio_path: str,
                         video_path: str,
                         output_path: str,
                         audio_sync: float = 0.0) -> bool:
        """
        Merge audio and video files
        
        Args:
            audio_path: Path to audio file (MP3/WAV)
            video_path: Path to video file (MP4/WebM)
            output_path: Path to output file
            audio_sync: Audio sync offset in seconds
        
        Returns:
            True if successful, False otherwise
        """
        try:
            if not os.path.exists(audio_path):
                raise FileNotFoundError(f'Audio file not found: {audio_path}')
            
            if not os.path.exists(video_path):
                raise FileNotFoundError(f'Video file not found: {video_path}')
            
            # Create output directory if it doesn't exist
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # FFmpeg command
            cmd = [
                self.ffmpeg_path,
                '-i', video_path,
                '-i', audio_path,
                '-c:v', 'copy',  # Copy video codec (no re-encoding)
                '-c:a', 'aac',   # Use AAC for audio
                '-shortest',     # Match shortest duration
                '-y',            # Overwrite output
                output_path
            ]
            
            logger.info(f'Merging audio and video: {" ".join(cmd)}')
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=self.timeout
            )
            
            if result.returncode != 0:
                logger.error(f'FFmpeg error: {result.stderr}')
                return False
            
            logger.info(f'Successfully merged to: {output_path}')
            return True
        
        except subprocess.TimeoutExpired:
            logger.error(f'FFmpeg timeout while merging {audio_path} and {video_path}')
            return False
        except Exception as e:
            logger.error(f'Error in merge_audio_video: {str(e)}')
            return False
    
    def extract_audio(self, video_path: str, output_path: str) -> bool:
        """
        Extract audio from video file
        
        Args:
            video_path: Path to video file
            output_path: Path to output audio file
        
        Returns:
            True if successful, False otherwise
        """
        try:
            if not os.path.exists(video_path):
                raise FileNotFoundError(f'Video file not found: {video_path}')
            
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            cmd = [
                self.ffmpeg_path,
                '-i', video_path,
                '-q:a', '0',
                '-map', 'a',
                '-y',
                output_path
            ]
            
            logger.info(f'Extracting audio: {" ".join(cmd)}')
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=self.timeout
            )
            
            if result.returncode != 0:
                logger.error(f'FFmpeg error: {result.stderr}')
                return False
            
            logger.info(f'Audio extracted to: {output_path}')
            return True
        
        except Exception as e:
            logger.error(f'Error in extract_audio: {str(e)}')
            return False
    
    def convert_audio(self, input_path: str, output_path: str, format: str = 'mp3') -> bool:
        """
        Convert audio to different format
        
        Args:
            input_path: Input audio file
            output_path: Output audio file
            format: Target format (mp3, wav, aac, etc.)
        
        Returns:
            True if successful, False otherwise
        """
        try:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            cmd = [
                self.ffmpeg_path,
                '-i', input_path,
                '-codec:a', 'libmp3lame' if format == 'mp3' else 'aac',
                '-b:a', '192k',
                '-y',
                output_path
            ]
            
            logger.info(f'Converting audio: {" ".join(cmd)}')
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=self.timeout
            )
            
            if result.returncode != 0:
                logger.error(f'FFmpeg error: {result.stderr}')
                return False
            
            logger.info(f'Audio converted to: {output_path}')
            return True
        
        except Exception as e:
            logger.error(f'Error in convert_audio: {str(e)}')
            return False
    
    def get_duration(self, file_path: str) -> Optional[float]:
        """
        Get duration of audio/video file in seconds
        
        Args:
            file_path: Path to file
        
        Returns:
            Duration in seconds, or None if error
        """
        try:
            cmd = [
                self.ffmpeg_path,
                '-i', file_path
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            # Parse duration from ffmpeg output
            for line in result.stderr.split('\n'):
                if 'Duration' in line:
                    duration_str = line.split('Duration')[1].split(',')[0].strip()
                    parts = duration_str.split(':')
                    if len(parts) == 3:
                        hours, minutes, seconds = parts
                        total_seconds = int(hours) * 3600 + int(minutes) * 60 + float(seconds)
                        return total_seconds
            
            return None
        
        except Exception as e:
            logger.error(f'Error in get_duration: {str(e)}')
            return None
