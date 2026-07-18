#!/usr/bin/env python
"""CLI for KPGM Music Video Generator"""

import click
import os
from pathlib import Path
from backend.services.suno_service import SunoService
from backend.services.video_service import VideoService
from backend.services.synthesis_service import SynthesisService

@click.group()
def cli():
    """KPGM Music Video Generator CLI"""
    pass

@cli.command()
@click.option('--text', required=True, help='Music description')
@click.option('--style', default='ambient', help='Music style/genre')
@click.option('--duration', default=60, type=int, help='Duration in seconds')
@click.option('--output', default='output.mp3', help='Output file path')
def music(text, style, duration, output):
    """Generate music from text description"""
    click.echo(f'🎵 Generating music: "{text}"')
    click.echo(f'   Style: {style}, Duration: {duration}s')
    
    try:
        service = SunoService()
        result = service.generate_music(text, style, duration)
        click.echo(f'✓ Generation started: {result["generation_id"]}')
        click.echo('⏳ Waiting for completion...')
        
        completed = service.wait_for_generation(result['generation_id'])
        
        if completed['status'] == 'completed':
            click.echo(f'✓ Music generated successfully!')
            click.echo(f'   URL: {completed["music_url"]}')
        else:
            click.echo(f'✗ Generation failed: {completed["status"]}')
    
    except Exception as e:
        click.echo(f'✗ Error: {str(e)}', err=True)

@cli.command()
@click.option('--prompt', required=True, help='Video description')
@click.option('--style', default='cinematic', help='Video style')
@click.option('--duration', default=60, type=int, help='Duration in seconds')
@click.option('--provider', default='runway', type=click.Choice(['runway', 'stability']), help='Video generation provider')
@click.option('--output', default='output.mp4', help='Output file path')
def video(prompt, style, duration, provider, output):
    """Generate video from text description"""
    click.echo(f'🎬 Generating video: "{prompt}"')
    click.echo(f'   Style: {style}, Duration: {duration}s, Provider: {provider}')
    
    try:
        service = VideoService()
        
        if provider == 'runway':
            result = service.generate_video_runway(prompt, style, duration)
        else:
            result = service.generate_video_stability(prompt, style, duration)
        
        click.echo(f'✓ Generation started: {result["generation_id"]}')
        click.echo('⏳ Waiting for completion...')
        
        completed = service.wait_for_generation(result['generation_id'], provider)
        
        if completed['status'] == 'completed':
            click.echo(f'✓ Video generated successfully!')
            click.echo(f'   URL: {completed["video_url"]}')
        else:
            click.echo(f'✗ Generation failed: {completed["status"]}')
    
    except Exception as e:
        click.echo(f'✗ Error: {str(e)}', err=True)

@cli.command()
@click.option('--audio', required=True, help='Audio file path')
@click.option('--video', required=True, help='Video file path')
@click.option('--output', default='merged.mp4', help='Output file path')
def merge(audio, video, output):
    """Merge audio and video files"""
    click.echo(f'🔄 Merging audio and video...')
    click.echo(f'   Audio: {audio}')
    click.echo(f'   Video: {video}')
    click.echo(f'   Output: {output}')
    
    try:
        service = SynthesisService()
        success = service.merge_audio_video(audio, video, output)
        
        if success:
            click.echo(f'✓ Files merged successfully!')
            click.echo(f'   Saved to: {output}')
        else:
            click.echo(f'✗ Merge failed', err=True)
    
    except Exception as e:
        click.echo(f'✗ Error: {str(e)}', err=True)

if __name__ == '__main__':
    cli()
