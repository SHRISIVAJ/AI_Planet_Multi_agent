# Text to Video Web App - Deployment Guide

## Quick Start

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the demo**:
   ```bash
   python demo.py
   ```

3. **Start the web app**:
   ```bash
   python app.py
   # Then open http://localhost:5000 in your browser
   ```

## Production Deployment Options

### Option 1: Traditional Server (Gunicorn + Nginx)

1. **Install Gunicorn**:
   ```bash
   pip install gunicorn
   ```

2. **Run with Gunicorn**:
   ```bash
   gunicorn -w 4 -b 0.0.0.0:8000 app:app
   ```

3. **Nginx configuration** (`/etc/nginx/sites-available/texttovideo`):
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;
       
       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
           client_max_body_size 50M;
       }
       
       location /static {
           alias /path/to/your/app/static;
           expires 1y;
           add_header Cache-Control "public, immutable";
       }
   }
   ```

### Option 2: Docker Container

1. **Create Dockerfile**:
   ```dockerfile
   FROM python:3.9-slim
   
   RUN apt-update && apt-get install -y ffmpeg
   
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   
   COPY . .
   
   EXPOSE 5000
   CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
   ```

2. **Build and run**:
   ```bash
   docker build -t text-to-video-app .
   docker run -p 5000:5000 text-to-video-app
   ```

### Option 3: Cloud Platforms

#### Heroku
1. Create `Procfile`:
   ```
   web: gunicorn app:app
   ```

2. Add buildpacks:
   ```bash
   heroku buildpacks:add heroku/python
   heroku buildpacks:add https://github.com/jonathanong/heroku-buildpack-ffmpeg-latest.git
   ```

#### Railway/Render
- Both support Python apps directly
- Add environment variable: `PYTHON_VERSION=3.9`
- Ensure FFmpeg is available in build environment

#### AWS/GCP/Azure
- Use container services (ECS, Cloud Run, Container Instances)
- Or traditional compute with the Docker approach above

## Environment Variables

Set these for production:

```bash
export FLASK_ENV=production
export FLASK_DEBUG=False
export SECRET_KEY=your-secret-key-here
export MAX_CONTENT_LENGTH=16777216  # 16MB
```

## Performance Optimization

### For Production

1. **Use Celery for background tasks**:
   ```bash
   pip install celery redis
   ```

2. **Add Redis for session storage**:
   ```python
   import redis
   from flask_session import Session
   
   app.config['SESSION_TYPE'] = 'redis'
   app.config['SESSION_REDIS'] = redis.from_url('redis://localhost:6379')
   ```

3. **Use CDN for static files**

4. **Implement file cleanup cron job**

### Scaling Considerations

- Use load balancer for multiple app instances
- Shared file storage (S3, Google Cloud Storage)
- Database for job tracking (PostgreSQL, MongoDB)
- Caching layer (Redis, Memcached)

## Security Checklist

- [ ] Enable HTTPS
- [ ] Set up CSRF protection
- [ ] Implement rate limiting
- [ ] Add input validation
- [ ] Sanitize file uploads
- [ ] Use environment variables for secrets
- [ ] Enable security headers
- [ ] Regular dependency updates

## Monitoring

### Logging
```python
import logging
logging.basicConfig(level=logging.INFO)
```

### Health Check Endpoint
Add to `app.py`:
```python
@app.route('/health')
def health():
    return {'status': 'healthy', 'timestamp': time.time()}
```

### Metrics
- Track processing times
- Monitor error rates
- Video generation success rates
- Storage usage

## Troubleshooting

### Common Issues

1. **FFmpeg not found**:
   - Ubuntu: `apt install ffmpeg`
   - CentOS: `yum install ffmpeg`
   - Docker: Add to Dockerfile

2. **Memory issues with large files**:
   - Implement streaming processing
   - Add swap space
   - Limit concurrent processes

3. **Disk space**:
   - Implement automatic cleanup
   - Use cloud storage
   - Monitor disk usage

4. **Network timeouts**:
   - Increase timeout settings
   - Implement retry logic
   - Use local TTS if possible
