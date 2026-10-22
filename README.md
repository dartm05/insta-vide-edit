# 🎬 AI-Powered Instagram Video Editor

> Transform your videos into Instagram-ready content with AI-powered style transfer

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🌟 What Is This?

A complete web application that lets you **copy the editing style of any video** and apply it to your own content. Perfect for creating viral-worthy Instagram Reels and Stories!

### Key Features

- 🎨 **Style Transfer** - Upload a viral video, copy its editing style
- ✨ **Preset Styles** - Professional templates (TikTok, LinkedIn, YouTube, Vlog)
- 📱 **Instagram Formats** - Export to Stories, Reels, Feed (Square/Portrait/Landscape)
- 🌐 **Web Interface** - Beautiful browser-based editor (no coding needed!)
- ⚡ **Fast Processing** - Real-time progress tracking
- 🔄 **Batch Processing** - Edit multiple videos at once

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r web_requirements.txt
```

> **Note**: Requires FFmpeg. Install with `brew install ffmpeg` (macOS) or `sudo apt install ffmpeg` (Linux)

### 2. Start the Web App

```bash
python run_web.py
```

### 3. Open in Browser

Go to: **http://localhost:8000**

**That's it!** 🎉

## 💡 How It Works

### Style Transfer Mode

1. **Upload a reference video** (e.g., a viral TikTok)
2. **Upload your video** (the content you want to edit)
3. **Click Process** ✨
4. **Download** your Instagram-ready video!

The AI analyzes the reference video's:
- Shot pacing and rhythm
- Cropping and framing
- Transition styles
- Caption placement
- Color grading
- Audio treatment

Then applies the same style to your video!

### Preset Styles Mode

Don't have a reference video? Use our pre-built styles:

- **Viral TikTok** - Fast-paced, bold captions, vibrant colors
- **Professional LinkedIn** - Clean, subtle, business-appropriate
- **Cinematic YouTube** - Smooth, atmospheric, film-like
- **Casual Vlog** - Natural, minimal editing, authentic feel

## 📸 Screenshots

### Web Interface
![Web Interface](https://via.placeholder.com/800x400/0f172a/8b5cf6?text=Modern+Dark+Theme+Interface)

### Style Transfer
![Style Transfer](https://via.placeholder.com/800x400/1e293b/ec4899?text=Upload+%26+Process+Videos)

### Real-time Progress
![Progress Tracking](https://via.placeholder.com/800x400/0f172a/10b981?text=Live+Progress+Updates)

## 🎯 Use Cases

| Scenario | Solution |
|----------|----------|
| "I want my Reels to look like viral TikToks" | Upload viral TikTok as reference → Process your videos |
| "I need consistent editing for my brand" | Create style template → Apply to all videos |
| "I don't know video editing" | Use preset styles → Upload → Download |
| "I want to quickly convert to Instagram formats" | Quick Convert mode → Select format → Done |

## 📚 Documentation

### Getting Started
- **[GETTING_STARTED.md](GETTING_STARTED.md)** - Setup and installation
- **[WEB_APP_GUIDE.md](WEB_APP_GUIDE.md)** - Complete web app guide
- **[FAQ.md](FAQ.md)** - Common questions

### Advanced Usage
- **[STYLE_TRANSFER_GUIDE.md](STYLE_TRANSFER_GUIDE.md)** - Deep dive into style copying
- **[Python API](video_agent/)** - Use as a Python library
- **[Examples](video_agent/examples/)** - Code examples

### Technical
- **[IMPLEMENTATION_STATUS.md](IMPLEMENTATION_STATUS.md)** - Technical details
- **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - Complete overview

## 🛠️ Installation (Detailed)

### Prerequisites

- Python 3.9 or higher
- FFmpeg 4.4+
- 8GB+ RAM (recommended)

### Step-by-Step

```bash
# 1. Clone or download the project
cd VideoAgent

# 2. Install FFmpeg
# macOS:
brew install ffmpeg

# Ubuntu/Debian:
sudo apt update && sudo apt install ffmpeg

# Windows:
# Download from https://ffmpeg.org/download.html

# 3. Install Python dependencies
pip install -r web_requirements.txt

# 4. Verify installation
python verify_setup.py

# 5. Start the web server
python run_web.py

# 6. Open http://localhost:8000 in your browser
```

## 🎨 Instagram Formats

| Format | Aspect Ratio | Resolution | Max Duration | Best For |
|--------|-------------|------------|--------------|----------|
| **Stories** | 9:16 | 1080x1920 | 60s | Temporary content |
| **Reels** | 9:16 | 1080x1920 | 90s | Viral short-form |
| **Feed Square** | 1:1 | 1080x1080 | 60s | Grid aesthetic |
| **Feed Portrait** | 4:5 | 1080x1350 | 60s | Maximum visibility |
| **Feed Landscape** | 1.91:1 | 1080x566 | 60s | Cinematic content |

## 💻 Python API

Don't want to use the web interface? Use it as a Python library:

```python
from src.analysis.style_analyzer import learn_from_video, apply_style_to_video

# Learn from a viral video
style = learn_from_video('viral_tiktok.mp4', 'Viral Style')

# Apply to your content
output = apply_style_to_video('my_video.mp4', style, 'reels')

print(f"Done! Video saved to: {output}")
```

Or use presets:

```python
from src.models.editing_style import get_preset_style
from src.analysis.style_analyzer import apply_style_to_video

# Use TikTok-style editing
style = get_preset_style('viral_tiktok')
output = apply_style_to_video('my_video.mp4', style, 'reels')
```

## 🏗️ Project Structure

```
VideoAgent/
├── web/                    # Web application
│   ├── app.py             # FastAPI server
│   ├── static/            # CSS, JavaScript
│   └── templates/         # HTML
│
├── video_agent/           # Core Python package
│   ├── config/            # Settings & formats
│   ├── src/               # Video processing
│   └── examples/          # Code examples
│
├── run_web.py            # Start server
├── WEB_APP_GUIDE.md      # Web documentation
└── README.md             # This file
```

## 🔧 Configuration

Create a `.env` file for custom settings:

```bash
cp video_agent/.env.example video_agent/.env
```

Edit `video_agent/.env`:

```env
# Output directory
OUTPUT_DIR=./output

# Processing settings
MAX_FRAMES_PER_VIDEO=60
ENABLE_CACHING=true

# For AI features (Phase 3)
ANTHROPIC_API_KEY=your_key_here
```

## 🚢 Deployment

### Docker

```bash
docker build -t video-editor .
docker run -p 8000:8000 video-editor
```

### Production (with Gunicorn)

```bash
pip install gunicorn
gunicorn web.app:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

See [WEB_APP_GUIDE.md](WEB_APP_GUIDE.md#production-deployment) for more options.

## 📊 Performance

- **Processing Speed**: ~30s for 60s video (varies by complexity)
- **File Size Limits**: Up to 500MB per video
- **Concurrent Jobs**: 3 simultaneous (configurable)
- **Output Quality**: Instagram-optimized encoding

## 🔒 Privacy

- All processing is done **locally** on your machine
- No videos are uploaded to external servers
- No data is collected or stored
- Full control over your content

## 🤝 Contributing

Contributions welcome! Some ideas:

- Add more preset styles
- Implement Phase 2 (advanced analysis)
- Improve UI/UX
- Add more Instagram formats
- Optimize processing speed

## 📝 License

MIT License - see [LICENSE](LICENSE) for details.

## 🙏 Acknowledgments

Built with:
- [FastAPI](https://fastapi.tiangolo.com) - Web framework
- [FFmpeg](https://ffmpeg.org) - Video processing
- [OpenCV](https://opencv.org) - Computer vision
- [Anthropic Claude](https://anthropic.com) - AI (Phase 3)

## 📞 Support

- **Issues**: Check [FAQ.md](FAQ.md)
- **Setup Help**: See [GETTING_STARTED.md](GETTING_STARTED.md)
- **Web App**: Read [WEB_APP_GUIDE.md](WEB_APP_GUIDE.md)

## 🎉 Quick Demo

```bash
# Start the server
python run_web.py

# In your browser (http://localhost:8000):
# 1. Click "Style Transfer" tab
# 2. Upload a viral video as reference
# 3. Upload your video
# 4. Select "Instagram Reels"
# 5. Click "Process Video"
# 6. Download your edited video!
```

---

<div align="center">

**Made with ❤️ for content creators**

[Get Started](#-quick-start) • [Documentation](GETTING_STARTED.md) • [Web Guide](WEB_APP_GUIDE.md)

</div>
