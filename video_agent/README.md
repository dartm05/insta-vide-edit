# AI-Powered Instagram Video Editing Platform

An intelligent video editing platform that uses Claude's vision capabilities to automatically edit videos for Instagram formats (Stories/Reels 9:16, Feed 1:1, Portrait 4:5) with auto-cropping, content-aware editing, captions, and effects.

## Features

- **🎨 Style Transfer**: Learn editing styles from reference videos and apply to your content
- **✂️ Auto-Cropping**: Intelligent cropping using AI vision to detect faces, text, and action areas
- **🎬 Content-Aware Editing**: AI-driven highlight detection and scene selection
- **💬 Smart Captions**: Automatic transcription and caption generation with optimal positioning
- **✨ Effects & Filters**: AI-selected color grading and visual enhancements
- **📱 Multi-Format Export**: Simultaneously export to multiple Instagram formats
- **✅ Instagram Compliance**: Built-in validation for Instagram video specifications

## Installation

### Prerequisites

- Python 3.10+
- FFmpeg 4.4+ (with libx264, libx265, libfdk-aac)
- 8GB+ RAM recommended

### Install FFmpeg

**macOS:**
```bash
brew install ffmpeg
```

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install ffmpeg
```

**Windows:**
Download from https://ffmpeg.org/download.html

### Install Python Dependencies

```bash
cd video_agent
pip install -r requirements.txt
```

### Configuration

1. Copy the environment template:
```bash
cp .env.example .env
```

2. Edit `.env` and add your Anthropic API key:
```
ANTHROPIC_API_KEY=your_api_key_here
```

## Quick Start

### 🌐 Web Interface (Easiest!)

Start the web application:

```bash
# Install web dependencies
pip install -r ../web_requirements.txt

# Start server
python ../run_web.py
```

Then open **http://localhost:8000** in your browser!

Features:
- Upload videos directly in browser
- Copy editing styles from reference videos
- Apply preset styles with one click
- Real-time progress tracking
- Download processed results

**See [WEB_APP_GUIDE.md](../WEB_APP_GUIDE.md) for complete web app documentation.**

### Basic Usage (Python API)

```python
from src.core.pipeline import quick_convert

# Convert video to Instagram Stories format
output_path = quick_convert('my_video.mp4', format_name='stories')
print(f"Converted video: {output_path}")
```

### 🎨 Copy Editing Style from Another Video

```python
from src.analysis.style_analyzer import learn_from_video, apply_style_to_video

# Learn editing style from a viral video
style = learn_from_video('viral_video.mp4', 'Viral Style')
style.save('styles/viral_style.json')

# Apply to your content
output = apply_style_to_video('my_video.mp4', style, 'reels')
print(f"Styled video: {output}")
```

**See [STYLE_TRANSFER_GUIDE.md](STYLE_TRANSFER_GUIDE.md) for complete documentation on copying editing styles.**

### Multi-Format Export

```python
from src.core.pipeline import VideoPipeline

# Process for multiple formats
pipeline = VideoPipeline('my_video.mp4')
outputs = pipeline.process(['stories', 'reels', 'feed_square'])

for format_name, output_path in outputs.items():
    print(f"{format_name}: {output_path}")
```

### Command Line

```bash
# Basic conversion
python examples/basic_edit.py my_video.mp4 --formats stories reels feed_square

# Copy editing style
python examples/copy_editing_style.py learn --reference viral_video.mp4
python examples/copy_editing_style.py apply --input my_video.mp4 --style styles/viral_video.json
```

## Instagram Formats

| Format | Aspect Ratio | Resolution | Max Duration | Use Case |
|--------|-------------|------------|--------------|----------|
| `stories` | 9:16 | 1080x1920 | 60s | Stories |
| `reels` | 9:16 | 1080x1920 | 90s | Reels |
| `feed_square` | 1:1 | 1080x1080 | 60s | Feed posts |
| `feed_portrait` | 4:5 | 1080x1350 | 60s | Feed posts |
| `feed_landscape` | 1.91:1 | 1080x566 | 60s | Feed posts |

## Project Structure

```
video_agent/
├── config/              # Configuration files
├── src/
│   ├── core/           # Core pipeline components
│   ├── analysis/       # Video analysis modules
│   ├── ai/             # AI integration (Claude)
│   ├── processors/     # Video processing
│   ├── utils/          # Utility functions
│   └── models/         # Data models
├── examples/           # Example scripts
└── tests/             # Test suite
```

## Development Status

### ✅ Phase 1: Foundation (COMPLETE)
- [x] Project structure
- [x] Configuration system
- [x] Instagram format specifications
- [x] Video input/output handlers
- [x] FFmpeg wrapper
- [x] Validation system
- [x] Basic pipeline
- [x] Style transfer system (learn and apply editing styles)
- [x] Preset editing styles (TikTok, LinkedIn, YouTube, Vlog)

### 🚧 Phase 2: Analysis Layer (TODO)
- [ ] Frame extraction
- [ ] Scene detection
- [ ] Audio analysis
- [ ] Content scoring

### 🚧 Phase 3: AI Integration (TODO)
- [ ] Claude Vision API integration
- [ ] AI decision engine
- [ ] Prompt engineering

### 🚧 Phase 4-7: Processing Features (TODO)
- [ ] Auto-crop processor
- [ ] Content-aware editing
- [ ] Caption generation
- [ ] Effects & filters

## API Reference

### VideoPipeline

Main orchestrator for video processing.

```python
pipeline = VideoPipeline(input_path)
outputs = pipeline.process(target_formats)
```

### VideoInput

Load and validate videos.

```python
from src.core.video_input import VideoInput

video = VideoInput.load('video.mp4')
metadata = video.extract_metadata()
```

### VideoOutput

Export videos to Instagram formats.

```python
from src.core.video_output import VideoOutput

output = VideoOutput.export_for_format(
    input_path='input.mp4',
    format_name='stories',
)
```

## Cost Optimization

The platform is designed to minimize AI API costs:

- Smart frame sampling (30-60 frames per 60s video)
- Frame resizing before API calls
- Batch processing
- Result caching
- Local models where possible (Whisper, OpenCV)

**Estimated cost: ~$0.20 per 60s video**

## Troubleshooting

### FFmpeg not found

Make sure FFmpeg is installed and accessible in your PATH:
```bash
ffmpeg -version
```

### API key error

Ensure your `.env` file contains a valid Anthropic API key:
```
ANTHROPIC_API_KEY=sk-ant-...
```

### Memory issues

For large videos, adjust the memory limit in `.env`:
```
MAX_VIDEO_MEMORY_MB=4096
```

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
