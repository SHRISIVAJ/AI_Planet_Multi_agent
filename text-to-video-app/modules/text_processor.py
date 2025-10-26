import os
import tempfile
from gtts import gTTS
import textwrap

class TextProcessor:
    def __init__(self):
        self.max_chunk_length = 500  # Characters per chunk
        self.language = 'en'
    
    def chunk_text(self, text, max_length=None):
        """Split long text into manageable chunks for TTS"""
        if max_length is None:
            max_length = self.max_chunk_length
        
        # Split text into sentences first
        sentences = text.replace('\n', ' ').split('. ')
        chunks = []
        current_chunk = ""
        
        for sentence in sentences:
            # Add period back if it was removed
            if not sentence.endswith('.') and sentence != sentences[-1]:
                sentence += '.'
            
            # Check if adding this sentence would exceed max length
            if len(current_chunk + sentence) > max_length and current_chunk:
                chunks.append(current_chunk.strip())
                current_chunk = sentence
            else:
                current_chunk += (" " if current_chunk else "") + sentence
        
        # Add the last chunk if it exists
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return chunks
    
    def text_to_speech(self, text, output_path=None, language=None):
        """Convert text to speech using gTTS"""
        if language is None:
            language = self.language
        
        try:
            tts = gTTS(text=text, lang=language, slow=False)
            
            if output_path is None:
                # Create temporary file
                temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
                output_path = temp_file.name
                temp_file.close()
            
            tts.save(output_path)
            return output_path
        except Exception as e:
            print(f"Error in text-to-speech conversion: {e}")
            return None
    
    def estimate_duration(self, text, words_per_minute=150):
        """Estimate audio duration based on text length"""
        words = len(text.split())
        duration_minutes = words / words_per_minute
        return duration_minutes * 60  # Return in seconds
    
    def format_text_for_display(self, text, line_length=40):
        """Format text for video display with proper line breaks"""
        return '\n'.join(textwrap.wrap(text, width=line_length))
