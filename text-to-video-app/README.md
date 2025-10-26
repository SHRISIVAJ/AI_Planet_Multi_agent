# Text to Video Web App

A Python web application that converts long text into engaging videos with AI-powered narration.

## Features

- **Text Input**: Paste text directly or upload text files (.txt, .md)
- **Text-to-Speech**: Automatic conversion using Google TTS
- **Video Generation**: Creates professional videos with text overlays
- **Real-time Progress**: Track processing status with live updates
- **Video Preview**: Preview generated videos before downloading
- **Responsive Design**: Works on desktop and mobile devices
- **File Management**: Automatic cleanup of temporary files

## Technology Stack

- **Backend**: Flask (Python web framework)
- **Text Processing**: Custom chunking and formatting
- **Text-to-Speech**: gTTS (Google Text-to-Speech)
- **Video Generation**: MoviePy for video creation
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **UI Framework**: Bootstrap 5
- **Icons**: Font Awesome

## Installation

1. **Clone or download the project files**

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify directory structure**:
   ```
   text-to-video-app/
   ├── app.py
   ├── requirements.txt
   ├── static/
   │   ├── css/style.css
   │   ├── js/app.js
   │   ├── uploads/
   │   └── videos/
   ├── templates/
   │   └── index.html
   ├── modules/
   │   ├── text_processor.py
   │   └── video_generator.py
   └── README.md
   ```

## Usage

1. **Start the application**:
   ```bash
   python app.py
   ```

2. **Open your browser** and navigate to `http://localhost:5000`

3. **Input your text**:
   - Type or paste text directly into the text area
   - Or upload a text file (.txt or .md format)
   - Text should be at least 10 characters (max 5,000 characters)

4. **Configure options** (optional):
   - Voice Speed: Normal, Slow, or Fast
   - Video Style: Default, Dark, or Light theme

5. **Generate video**:
   - Click "Generate Video" button
   - Monitor real-time progress
   - Preview and download the generated video

## API Endpoints

- `GET /` - Main interface
- `POST /process_text` - Start text-to-video processing
- `GET /status/<job_id>` - Check processing status
- `GET /preview/<filename>` - Preview generated video
- `GET /download/<filename>` - Download video file

## Processing Pipeline

1. **Text Analysis**: Input text is analyzed and chunked into manageable segments
2. **Speech Generation**: Each chunk is converted to speech using Google TTS
3. **Video Creation**: Text overlays are synchronized with audio
4. **Final Assembly**: All segments are combined into a single video file
5. **Output**: MP4 video file with embedded audio

## Configuration Options

### Text Processing
- Maximum chunk length: 500 characters
- Language: English (configurable)
- Line wrapping: 40 characters per line

### Video Settings
- Resolution: 1280x720 (HD)
- Frame rate: 24 fps
- Background: Customizable colors
- Text color: White (configurable)
- Font: Arial Bold, 48pt

### File Limits
- Text input: 5,000 characters
- File upload: 16MB maximum
- Supported formats: .txt, .md

## Technical Details

### Dependencies
- **Flask 2.3.3**: Web framework
- **MoviePy 1.0.3**: Video processing
- **gTTS 2.4.0**: Text-to-speech conversion
- **Pillow 10.0.1**: Image processing
- **Requests 2.31.0**: HTTP requests

### Browser Support
- Chrome 60+
- Firefox 55+
- Safari 12+
- Edge 79+

## Development Notes

### Current Implementation
- Synchronous processing (demo version)
- In-memory status tracking
- Basic error handling
- Simplified UI interactions

### Production Considerations
For production deployment, consider:

1. **Asynchronous Processing**: Use Celery or similar task queue
2. **Database**: Replace in-memory storage with Redis/PostgreSQL
3. **File Storage**: Use cloud storage (AWS S3, Google Cloud)
4. **Scaling**: Load balancing and horizontal scaling
5. **Security**: Input validation, rate limiting, authentication
6. **Monitoring**: Logging, metrics, health checks

## Troubleshooting

### Common Issues

1. **Import Errors**:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

2. **MoviePy Issues**:
   - Ensure FFmpeg is installed on your system
   - On Ubuntu: `sudo apt install ffmpeg`
   - On macOS: `brew install ffmpeg`
   - On Windows: Download from https://ffmpeg.org/

3. **Audio Generation Fails**:
   - Check internet connection (gTTS requires online access)
   - Verify Google TTS service availability

4. **Large File Processing**:
   - Increase server timeout settings
   - Consider chunking very large texts

### Error Messages

- "Text must be at least 10 characters": Provide more content
- "File too large": Use files under 16MB
- "Video generation failed": Check FFmpeg installation
- "Network error": Verify internet connection

## Customization

### Changing Video Style
Edit `modules/video_generator.py`:
```python
self.background_color = (30, 30, 50)  # RGB values
self.text_color = (255, 255, 255)     # RGB values
self.font_size = 48                   # Font size
```

### Adding Languages
Edit `modules/text_processor.py`:
```python
self.language = 'en'  # Change to desired language code
```

### Modifying UI
- CSS: `static/css/style.css`
- JavaScript: `static/js/app.js`
- HTML: `templates/index.html`

## License

This project is open source. Feel free to modify and distribute according to your needs.

## Contributing

1. Fork the repository
2. Create feature branch
3. Make changes
4. Test thoroughly
5. Submit pull request

## Support

For issues and questions:
- Check the troubleshooting section
- Review error logs in the console
- Verify all dependencies are installed correctly

---

**Note**: This is a demonstration application. For production use, implement proper security measures, error handling, and scalability features.
