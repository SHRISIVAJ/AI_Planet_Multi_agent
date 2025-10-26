from flask import Flask, render_template, request, send_file, jsonify, redirect, url_for
import os
import uuid
import tempfile
import time
from werkzeug.utils import secure_filename
from modules.text_processor import TextProcessor
from modules.video_generator import VideoGenerator

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['VIDEO_FOLDER'] = 'static/videos'

# Ensure directories exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['VIDEO_FOLDER'], exist_ok=True)

# Global storage for processing status (in production, use Redis or database)
processing_status = {}

text_processor = TextProcessor()
video_generator = VideoGenerator()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_text', methods=['POST'])
def process_text():
    try:
        # Get text from form or uploaded file
        text_input = request.form.get('text_input', '').strip()
        
        # Handle file upload
        if 'text_file' in request.files:
            file = request.files['text_file']
            if file and file.filename:
                filename = secure_filename(file.filename)
                if filename.endswith(('.txt', '.md')):
                    text_content = file.read().decode('utf-8')
                    text_input = text_content if text_content else text_input

        if not text_input or len(text_input.strip()) < 10:
            return jsonify({'error': 'Please provide text with at least 10 characters'}), 400

        # Generate unique job ID
        job_id = str(uuid.uuid4())
        
        # Initialize processing status
        processing_status[job_id] = {
            'status': 'processing',
            'progress': 0,
            'message': 'Starting text processing...',
            'video_path': None
        }
        
        # Start processing in background (simplified for demo)
        try:
            result = process_text_to_video(text_input, job_id)
            return jsonify({'job_id': job_id, 'status': 'started'})
        except Exception as e:
            processing_status[job_id] = {
                'status': 'error',
                'progress': 0,
                'message': f'Error: {str(e)}',
                'video_path': None
            }
            return jsonify({'error': str(e)}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def process_text_to_video(text, job_id):
    """Process text to video (simplified synchronous version)"""
    try:
        # Update status
        processing_status[job_id]['message'] = 'Chunking text...'
        processing_status[job_id]['progress'] = 20
        
        # Chunk text
        chunks = text_processor.chunk_text(text)
        
        # Update status
        processing_status[job_id]['message'] = 'Converting text to speech...'
        processing_status[job_id]['progress'] = 40
        
        # Convert to audio (for demo, we'll create one audio file)
        audio_files = []
        temp_dir = tempfile.mkdtemp()
        
        for i, chunk in enumerate(chunks[:3]):  # Limit to 3 chunks for demo
            audio_file = os.path.join(temp_dir, f'audio_{i}.mp3')
            result = text_processor.text_to_speech(chunk, audio_file)
            if result:
                audio_files.append(result)
        
        if not audio_files:
            raise Exception("Failed to generate audio files")
        
        # Update status
        processing_status[job_id]['message'] = 'Creating video...'
        processing_status[job_id]['progress'] = 70
        
        # Create video
        video_filename = f'video_{job_id}.mp4'
        video_path = os.path.join(app.config['VIDEO_FOLDER'], video_filename)
        
        if len(chunks) == 1 or len(audio_files) == 1:
            # Simple video
            result = video_generator.create_simple_video(
                chunks[0] if chunks else text[:500],
                audio_files[0],
                video_path
            )
        else:
            # Multi-chunk video
            result = video_generator.create_video_from_text_and_audio(
                chunks[:len(audio_files)],
                audio_files,
                video_path
            )
        
        if result:
            processing_status[job_id] = {
                'status': 'completed',
                'progress': 100,
                'message': 'Video created successfully!',
                'video_path': video_filename
            }
        else:
            raise Exception("Video generation failed")
            
        # Clean up temp files
        for audio_file in audio_files:
            try:
                os.remove(audio_file)
            except:
                pass
                
    except Exception as e:
        processing_status[job_id] = {
            'status': 'error',
            'progress': 0,
            'message': f'Error: {str(e)}',
            'video_path': None
        }

@app.route('/status/<job_id>')
def get_status(job_id):
    """Get processing status"""
    if job_id in processing_status:
        return jsonify(processing_status[job_id])
    else:
        return jsonify({'error': 'Job not found'}), 404

@app.route('/download/<filename>')
def download_video(filename):
    """Download generated video"""
    try:
        video_path = os.path.join(app.config['VIDEO_FOLDER'], filename)
        if os.path.exists(video_path):
            return send_file(
                video_path,
                as_attachment=True,
                download_name=filename,
                mimetype='video/mp4'
            )
        else:
            return jsonify({'error': 'Video file not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/preview/<filename>')
def preview_video(filename):
    """Serve video for preview"""
    try:
        video_path = os.path.join(app.config['VIDEO_FOLDER'], filename)
        if os.path.exists(video_path):
            return send_file(video_path, mimetype='video/mp4')
        else:
            return jsonify({'error': 'Video file not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.errorhandler(413)
def too_large(e):
    return jsonify({'error': 'File too large. Maximum size is 16MB.'}), 413

if __name__ == '__main__':
    print("Text to Video Web App")
    print("Available endpoints:")
    print("- / : Main interface")
    print("- /process_text : Process text to video")
    print("- /status/<job_id> : Check processing status")
    print("- /download/<filename> : Download video")
    print("- /preview/<filename> : Preview video")
    print("\nTo run the app: python app.py")
    print("Note: This is a demo version. For production, use proper task queues like Celery.")
    
    # Don't actually run the server as per instructions
    # app.run(debug=True, host='0.0.0.0', port=5000)
