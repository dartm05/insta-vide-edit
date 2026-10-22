# Web Application Guide

## Overview

The Instagram Video Editor now includes a beautiful web interface where users can:
- Upload videos directly in their browser
- Copy editing styles from reference videos
- Apply preset editing styles
- Convert videos to Instagram formats
- Download processed results

## Quick Start

### 1. Install Web Dependencies

```bash
pip install -r web_requirements.txt
```

This installs:
- `fastapi` - Modern web framework
- `uvicorn` - ASGI server
- `python-multipart` - File upload support
- `aiofiles` - Async file operations
- `jinja2` - Template engine

### 2. Start the Server

```bash
python run_web.py
```

Or directly:
```bash
uvicorn web.app:app --reload --host 0.0.0.0 --port 8000
```

### 3. Open in Browser

Navigate to: **http://localhost:8000**

## Features

### 🎨 Style Transfer Tab

Upload two videos:
1. **Reference Video** - The video whose editing style you want to copy (e.g., viral TikTok/Reel)
2. **Your Video** - The video you want to edit

The system will:
- Analyze the reference video's editing patterns
- Extract the style (pacing, cropping, transitions, captions, colors)
- Apply that style to your video
- Export in your chosen Instagram format

### ✨ Preset Styles Tab

Choose from pre-built professional editing styles:
- **Viral TikTok Style** - Fast-paced, bold captions, vibrant colors
- **Professional LinkedIn Style** - Clean, subtle transitions
- **Cinematic YouTube Style** - Smooth, atmospheric grading
- **Casual Vlog Style** - Natural, minimal editing

Simply:
1. Select a preset style card
2. Upload your video
3. Choose output format
4. Process!

### ⚡ Quick Convert Tab

Fast format conversion without style editing:
1. Upload your video
2. Select Instagram format
3. Get converted video

Supported formats:
- Instagram Reels (9:16 - 90s)
- Instagram Stories (9:16 - 60s)
- Feed Square (1:1)
- Feed Portrait (4:5)
- Feed Landscape (1.91:1)

## How It Works

### Backend Architecture

```
User Browser
    ↓
FastAPI Server (web/app.py)
    ↓
Background Tasks (async processing)
    ↓
Video Processing Pipeline
    ↓
Results Storage
    ↓
Download to User
```

### File Flow

1. **Upload**: User uploads video(s) via browser
2. **Storage**: Files saved to `web/uploads/`
3. **Processing**: Background task processes video
4. **Results**: Processed video saved to `web/results/`
5. **Download**: User downloads completed video

### Progress Tracking

The web app uses polling to check job status:
- Status checked every 2 seconds
- Progress bar updates in real-time
- Shows current processing step
- Notifies on completion/error

## API Endpoints

### POST `/api/style-transfer`

Apply style transfer from reference video.

**Parameters:**
- `reference_video` (file) - Reference video
- `input_video` (file) - Video to edit
- `format` (string) - Output format
- `style_name` (string, optional) - Custom style name

**Response:**
```json
{
  "job_id": "uuid",
  "status": "processing"
}
```

### POST `/api/preset-style`

Apply preset editing style.

**Parameters:**
- `video` (file) - Video to edit
- `preset` (string) - Preset name
- `format` (string) - Output format

**Response:**
```json
{
  "job_id": "uuid",
  "status": "processing"
}
```

### POST `/api/convert`

Quick format conversion.

**Parameters:**
- `video` (file) - Video to convert
- `format` (string) - Output format

**Response:**
```json
{
  "job_id": "uuid",
  "status": "processing"
}
```

### GET `/api/status/{job_id}`

Check job status.

**Response:**
```json
{
  "id": "uuid",
  "type": "style_transfer",
  "status": "processing",
  "progress": 45,
  "created_at": "2024-01-01T12:00:00",
  "result": null,
  "error": null
}
```

### GET `/api/download/{job_id}`

Download processed video.

**Response:** Video file (video/mp4)

### GET `/api/presets`

Get list of preset styles.

**Response:**
```json
[
  {
    "id": "viral_tiktok",
    "name": "Viral TikTok Style",
    "description": "Fast-paced with bold captions",
    "pace": "fast",
    "caption_style": "bold",
    "color_grade": "vibrant"
  }
]
```

### DELETE `/api/job/{job_id}`

Delete job and clean up files.

**Response:**
```json
{
  "message": "Job deleted successfully"
}
```

## Customization

### Modify Styles

Edit preset styles in `src/models/editing_style.py`:

```python
PRESET_STYLES = {
    'my_custom_style': EditingStyle(
        name='My Custom Style',
        description='Your description',
        pace='medium',
        # ... customize parameters
    ),
}
```

### Change Theme

Edit `web/static/css/style.css`:

```css
:root {
    --primary-color: #8b5cf6;  /* Change this */
    --bg-color: #0f172a;       /* And this */
    /* ... */
}
```

### Add Custom Templates

Create new Jinja2 templates in `web/templates/`.

### Modify Processing

Edit background task functions in `web/app.py`:
- `process_style_transfer()`
- `process_preset_style()`
- `process_video_conversion()`

## Production Deployment

### Using Gunicorn

```bash
pip install gunicorn
gunicorn web.app:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Using Docker

Create `Dockerfile`:

```dockerfile
FROM python:3.9-slim

# Install FFmpeg
RUN apt-get update && apt-get install -y ffmpeg

# Copy application
WORKDIR /app
COPY . .

# Install dependencies
RUN pip install -r web_requirements.txt

# Expose port
EXPOSE 8000

# Run application
CMD ["uvicorn", "web.app:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:
```bash
docker build -t instagram-video-editor .
docker run -p 8000:8000 instagram-video-editor
```

### With Redis (for Production)

For production, use Redis for job storage instead of in-memory dict.

Install:
```bash
pip install redis
```

Modify `web/app.py`:
```python
import redis

# Connect to Redis
redis_client = redis.Redis(host='localhost', port=6379, db=0)

# Store jobs in Redis
def create_job(job_type: str, **kwargs) -> str:
    job_id = str(uuid.uuid4())
    job_data = {
        "id": job_id,
        "type": job_type,
        "status": JobStatus.PENDING,
        # ...
    }
    redis_client.setex(
        f"job:{job_id}",
        3600,  # Expire after 1 hour
        json.dumps(job_data)
    )
    return job_id
```

### With Celery (for Heavy Workloads)

For distributed task processing:

```bash
pip install celery redis
```

Create `web/celery_app.py`:
```python
from celery import Celery

celery_app = Celery(
    'video_processor',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0'
)

@celery_app.task
def process_video_task(job_id, input_path, format_name):
    # Processing logic here
    pass
```

Run Celery worker:
```bash
celery -A web.celery_app worker --loglevel=info
```

## Security Considerations

### File Size Limits

Add in `web/app.py`:

```python
from fastapi import File, UploadFile

# Limit file size
MAX_FILE_SIZE = 500 * 1024 * 1024  # 500MB

@app.post("/api/upload")
async def upload(file: UploadFile = File(...)):
    # Check file size
    contents = await file.read()
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(413, "File too large")
```

### File Type Validation

```python
ALLOWED_EXTENSIONS = {'.mp4', '.mov', '.avi', '.mkv'}

def validate_file(filename: str):
    ext = Path(filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(400, f"Invalid file type: {ext}")
```

### Authentication

Add authentication with OAuth or JWT:

```python
from fastapi.security import HTTPBearer

security = HTTPBearer()

@app.post("/api/convert")
async def convert(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    # Verify token
    # Process request
    pass
```

## Troubleshooting

### Port Already in Use

Change port in `run_web.py`:
```python
uvicorn.run(app, host="0.0.0.0", port=8080)  # Use 8080
```

### Upload Fails

Check:
- File size limits
- Available disk space
- File permissions on `web/uploads/` directory

### Processing Hangs

Check:
- FFmpeg is installed: `ffmpeg -version`
- Sufficient RAM available
- Logs for specific errors

### CORS Issues

If accessing from different domain:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Performance Optimization

### Concurrent Processing

Limit concurrent jobs:

```python
import asyncio

MAX_CONCURRENT_JOBS = 3
semaphore = asyncio.Semaphore(MAX_CONCURRENT_JOBS)

async def process_with_limit():
    async with semaphore:
        # Process video
        pass
```

### Cleanup Old Files

Add scheduled cleanup:

```python
import asyncio
from datetime import datetime, timedelta

async def cleanup_old_files():
    while True:
        # Clean files older than 24 hours
        cutoff = datetime.now() - timedelta(hours=24)
        for file in UPLOAD_DIR.glob("*"):
            if datetime.fromtimestamp(file.stat().st_mtime) < cutoff:
                file.unlink()

        await asyncio.sleep(3600)  # Run every hour
```

### Compression

Compress videos before processing:

```python
from src.utils.ffmpeg_wrapper import FFmpegWrapper

def compress_video(input_path, output_path):
    # Reduce file size
    FFmpegWrapper.compress(input_path, output_path, crf=28)
```

## Monitoring

### Add Logging

```python
from loguru import logger

logger.add(
    "logs/web_app.log",
    rotation="500 MB",
    retention="10 days",
    level="INFO"
)

@app.post("/api/convert")
async def convert_video(...):
    logger.info(f"New conversion request: {video.filename}")
    # ...
```

### Metrics

Track metrics:

```python
from collections import Counter

metrics = {
    'total_jobs': 0,
    'completed_jobs': 0,
    'failed_jobs': 0,
    'formats': Counter(),
}

@app.get("/api/metrics")
async def get_metrics():
    return metrics
```

## Next Steps

1. **Test the Interface**
   ```bash
   python run_web.py
   # Open http://localhost:8000
   ```

2. **Upload Test Videos**
   - Try style transfer with a reference video
   - Test preset styles
   - Try quick conversion

3. **Deploy to Production**
   - Use Gunicorn or Docker
   - Set up Redis for job storage
   - Add authentication
   - Configure domain and SSL

4. **Monitor Usage**
   - Check logs regularly
   - Monitor disk space
   - Track processing times

Enjoy your web-based video editing platform! 🎬
