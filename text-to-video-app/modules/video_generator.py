import os
import tempfile
from moviepy.editor import *
from moviepy.config import check_output_params
from PIL import Image, ImageDraw, ImageFont
import numpy as np

class VideoGenerator:
    def __init__(self):
        self.video_width = 1280
        self.video_height = 720
        self.fps = 24
        self.background_color = (30, 30, 50)  # Dark blue background
        self.text_color = (255, 255, 255)     # White text
        self.font_size = 48
        
    def create_text_clip(self, text, duration, fontsize=None, color=None):
        """Create a text clip for the video"""
        if fontsize is None:
            fontsize = self.font_size
        if color is None:
            color = 'white'
        
        try:
            # Create text clip
            txt_clip = TextClip(
                text,
                fontsize=fontsize,
                color=color,
                font='Arial-Bold',
                size=(self.video_width - 100, None),  # Leave margin
                method='caption'
            ).set_duration(duration)
            
            # Center the text
            txt_clip = txt_clip.set_position('center')
            
            return txt_clip
        except Exception as e:
            print(f"Error creating text clip: {e}")
            # Fallback: create simple text without fancy formatting
            return TextClip(
                text,
                fontsize=fontsize//2,
                color=color
            ).set_duration(duration).set_position('center')
    
    def create_background_clip(self, duration, color=None):
        """Create a solid color background clip"""
        if color is None:
            color = self.background_color
        
        # Create a colored clip
        bg_clip = ColorClip(
            size=(self.video_width, self.video_height),
            color=color,
            duration=duration
        )
        
        return bg_clip
    
    def create_video_from_text_and_audio(self, text_chunks, audio_files, output_path):
        """Create video from text chunks and corresponding audio files"""
        clips = []
        
        try:
            for i, (text, audio_file) in enumerate(zip(text_chunks, audio_files)):
                if not os.path.exists(audio_file):
                    print(f"Warning: Audio file {audio_file} not found, skipping chunk {i}")
                    continue
                
                # Load audio to get duration
                audio_clip = AudioFileClip(audio_file)
                duration = audio_clip.duration
                
                # Create background
                bg_clip = self.create_background_clip(duration)
                
                # Create text overlay
                txt_clip = self.create_text_clip(text, duration)
                
                # Composite video and audio
                video_clip = CompositeVideoClip([bg_clip, txt_clip])
                video_clip = video_clip.set_audio(audio_clip)
                
                clips.append(video_clip)
            
            if not clips:
                raise Exception("No valid clips were created")
            
            # Concatenate all clips
            final_video = concatenate_videoclips(clips, method="compose")
            
            # Write the video file
            final_video.write_videofile(
                output_path,
                fps=self.fps,
                audio_codec='aac',
                codec='libx264',
                temp_audiofile='temp-audio.m4a',
                remove_temp=True
            )
            
            # Clean up
            final_video.close()
            for clip in clips:
                clip.close()
            
            return output_path
            
        except Exception as e:
            print(f"Error creating video: {e}")
            return None
    
    def create_simple_video(self, text, audio_file, output_path):
        """Create a simple video with text and audio"""
        try:
            # Load audio
            audio_clip = AudioFileClip(audio_file)
            duration = audio_clip.duration
            
            # Create background
            bg_clip = self.create_background_clip(duration)
            
            # Create text
            txt_clip = self.create_text_clip(text, duration)
            
            # Composite
            video = CompositeVideoClip([bg_clip, txt_clip])
            video = video.set_audio(audio_clip)
            
            # Write video
            video.write_videofile(
                output_path,
                fps=self.fps,
                audio_codec='aac',
                codec='libx264',
                temp_audiofile='temp-audio.m4a',
                remove_temp=True
            )
            
            # Clean up
            video.close()
            audio_clip.close()
            
            return output_path
            
        except Exception as e:
            print(f"Error creating simple video: {e}")
            return None
    
    def get_video_info(self, video_path):
        """Get information about a video file"""
        try:
            clip = VideoFileClip(video_path)
            info = {
                'duration': clip.duration,
                'fps': clip.fps,
                'size': clip.size
            }
            clip.close()
            return info
        except Exception as e:
            print(f"Error getting video info: {e}")
            return None
