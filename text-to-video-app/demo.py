#!/usr/bin/env python3
"""
Text to Video Web App - Demo Script

This script demonstrates the core functionality of the text-to-video application
without running a web server. It creates a sample video from text input.
"""

import os
import sys
import tempfile
from modules.text_processor import TextProcessor
from modules.video_generator import VideoGenerator

def create_sample_video():
    """Create a sample video to demonstrate functionality"""
    
    # Sample text
    sample_text = """
    Welcome to the Text to Video Generator! This is a demonstration of how 
    long text can be converted into engaging videos with AI-powered narration. 
    
    The application processes your text by breaking it into manageable chunks, 
    converts each chunk to speech using Google's Text-to-Speech service, 
    and then creates a video with synchronized text overlays and audio.
    
    This technology can be used for creating educational content, audiobooks, 
    presentations, or any scenario where you need to convert written content 
    into video format.
    """
    
    print("🎬 Text to Video Generator - Demo")
    print("=" * 50)
    print(f"Sample text length: {len(sample_text)} characters")
    print(f"Sample text preview: {sample_text[:100]}...")
    print()
    
    # Initialize processors
    text_processor = TextProcessor()
    video_generator = VideoGenerator()
    
    try:
        # Step 1: Process text
        print("📝 Step 1: Processing text...")
        chunks = text_processor.chunk_text(sample_text)
        print(f"   Text split into {len(chunks)} chunks")
        
        # Step 2: Generate audio
        print("🎵 Step 2: Converting text to speech...")
        temp_dir = tempfile.mkdtemp()
        audio_files = []
        
        for i, chunk in enumerate(chunks[:2]):  # Limit to 2 chunks for demo
            print(f"   Processing chunk {i+1}/{min(len(chunks), 2)}")
            audio_file = os.path.join(temp_dir, f'audio_{i}.mp3')
            result = text_processor.text_to_speech(chunk, audio_file)
            if result:
                audio_files.append(result)
                print(f"   ✓ Audio file created: {os.path.basename(audio_file)}")
            else:
                print(f"   ❌ Failed to create audio for chunk {i+1}")
        
        if not audio_files:
            print("❌ No audio files were generated. Check your internet connection.")
            return False
        
        # Step 3: Create video
        print("🎬 Step 3: Creating video...")
        output_path = os.path.join(os.getcwd(), 'sample_video.mp4')
        
        if len(audio_files) == 1:
            result = video_generator.create_simple_video(
                chunks[0],
                audio_files[0],
                output_path
            )
        else:
            result = video_generator.create_video_from_text_and_audio(
                chunks[:len(audio_files)],
                audio_files,
                output_path
            )
        
        if result:
            print(f"✅ Video created successfully: {output_path}")
            
            # Get video info
            info = video_generator.get_video_info(output_path)
            if info:
                print(f"   Duration: {info['duration']:.1f} seconds")
                print(f"   Resolution: {info['size'][0]}x{info['size'][1]}")
                print(f"   Frame rate: {info['fps']} fps")
            
            file_size = os.path.getsize(output_path) / (1024 * 1024)  # MB
            print(f"   File size: {file_size:.1f} MB")
            
            return True
        else:
            print("❌ Video creation failed")
            return False
            
    except Exception as e:
        print(f"❌ Error during processing: {e}")
        return False
    
    finally:
        # Clean up temporary files
        print("🧹 Cleaning up temporary files...")
        for audio_file in audio_files:
            try:
                os.remove(audio_file)
            except:
                pass
        try:
            os.rmdir(temp_dir)
        except:
            pass

def check_dependencies():
    """Check if all required dependencies are available"""
    print("🔍 Checking dependencies...")
    
    required_modules = [
        ('flask', 'Flask'),
        ('moviepy.editor', 'MoviePy'),
        ('gtts', 'gTTS'),
        ('PIL', 'Pillow')
    ]
    
    missing = []
    for module, name in required_modules:
        try:
            __import__(module)
            print(f"   ✓ {name}")
        except ImportError:
            print(f"   ❌ {name} (missing)")
            missing.append(name)
    
    if missing:
        print(f"\n❌ Missing dependencies: {', '.join(missing)}")
        print("Run: pip install -r requirements.txt")
        return False
    
    print("✅ All dependencies available")
    return True

def show_project_structure():
    """Display the project structure"""
    print("\n📁 Project Structure:")
    print("text-to-video-app/")
    
    structure = {
        'app.py': 'Main Flask application',
        'requirements.txt': 'Python dependencies',
        'README.md': 'Documentation and usage guide',
        'static/css/style.css': 'Custom CSS styles',
        'static/js/app.js': 'Frontend JavaScript',
        'templates/index.html': 'Main HTML template',
        'modules/text_processor.py': 'Text processing and TTS',
        'modules/video_generator.py': 'Video generation logic'
    }
    
    for file_path, description in structure.items():
        indicator = "✓" if os.path.exists(file_path) else "❌"
        print(f"   {indicator} {file_path:<30} - {description}")

def main():
    """Main function"""
    print("🎬 Text to Video Web App")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    print()
    
    # Show project structure
    show_project_structure()
    
    print()
    
    # Ask user what to do
    print("Available actions:")
    print("1. Create sample video (demo)")
    print("2. Show usage instructions")
    print("3. Exit")
    
    try:
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == '1':
            print("\n" + "="*50)
            success = create_sample_video()
            print("\n" + "="*50)
            if success:
                print("🎉 Demo completed successfully!")
                print("Check the 'sample_video.mp4' file in the current directory.")
            else:
                print("❌ Demo failed. Check error messages above.")
                
        elif choice == '2':
            print("\n📖 Usage Instructions:")
            print("-" * 30)
            print("1. Install dependencies: pip install -r requirements.txt")
            print("2. Run the web app: python app.py")
            print("3. Open browser: http://localhost:5000")
            print("4. Enter text or upload file")
            print("5. Generate and download video")
            print("\nFor detailed instructions, see README.md")
            
        elif choice == '3':
            print("👋 Goodbye!")
            
        else:
            print("❌ Invalid choice. Please run the script again.")
            
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()
