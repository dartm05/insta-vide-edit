# Getting Started

Welcome to the AI-Powered Instagram Video Editing Platform! This guide will help you get up and running quickly.

## 📋 Prerequisites

Before you begin, ensure you have:

- **Python 3.9+** (check: `python --version`)
- **FFmpeg** (video processing library)
- **8GB+ RAM** (recommended)

## 🚀 Quick Setup (5 Minutes)

### Step 1: Install FFmpeg

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
Download and install from https://ffmpeg.org/download.html

Verify installation:
```bash
ffmpeg -version
```

### Step 2: Install Python Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- `anthropic` - Claude API client
- `ffmpeg-python` - FFmpeg wrapper
- `opencv-python` - Computer vision
- `pydantic` - Data validation
- `loguru` - Logging
- And more...

### Step 3: Configure API Key (Optional)

The basic features work without an API key. For AI-powered features (Phase 3):

```bash
cp .env.example .env
# Edit .env and add: ANTHROPIC_API_KEY=your_key_here
```

### Step 4: Verify Setup

```bash
python verify_setup.py
```

This checks that everything is installed correctly.

## ✅ Test Your Installation

### Test 1: Basic Conversion

Create a test script `test_conversion.py`:

```python
from src.core.pipeline import quick_convert
from pathlib import Path

# Note: Replace with your actual video file
if Path('test_video.mp4').exists():
    output = quick_convert('test_video.mp4', 'stories')
    print(f"Success! Output: {output}")
else:
    print("Please provide a test video file named 'test_video.mp4'")
```

Run it:
```bash
python test_conversion.py
```

### Test 2: Style Transfer

```python
from src.models.editing_style import get_preset_style, list_preset_styles

# Show available preset styles
print("Available styles:")
for style_name in list_preset_styles():
    style = get_preset_style(style_name)
    print(f"  - {style.name}: {style.description}")
```

## 📚 Learn the Basics

### 1. Convert Videos to Instagram Formats

```python
from src.core.pipeline import quick_convert

# Convert to Instagram Stories (9:16)
output = quick_convert('my_video.mp4', 'stories')

# Convert to Reels
output = quick_convert('my_video.mp4', 'reels')

# Convert to Feed Square (1:1)
output = quick_convert('my_video.mp4', 'feed_square')
```

### 2. Export to Multiple Formats at Once

```python
from src.core.pipeline import VideoPipeline

pipeline = VideoPipeline('my_video.mp4')
outputs = pipeline.process(['stories', 'reels', 'feed_square'])

for format_name, path in outputs.items():
    print(f"{format_name}: {path}")
```

### 3. Copy Editing Style from Another Video

```python
from src.analysis.style_analyzer import learn_from_video, apply_style_to_video

# Learn from a viral video
style = learn_from_video('viral_video.mp4', 'Viral Style')

# Apply to your content
output = apply_style_to_video('my_video.mp4', style, 'reels')
```

### 4. Use Preset Editing Styles

```python
from src.models.editing_style import get_preset_style
from src.analysis.style_analyzer import apply_style_to_video

# Use TikTok-style editing
style = get_preset_style('viral_tiktok')
output = apply_style_to_video('my_video.mp4', style, 'reels')

# Use professional LinkedIn style
style = get_preset_style('professional_linkedin')
output = apply_style_to_video('my_video.mp4', style, 'feed_square')
```

## 🎯 Common Use Cases

### Use Case 1: I want to convert my video to Instagram Stories

```python
from src.core.pipeline import quick_convert

output = quick_convert('my_video.mp4', 'stories')
print(f"Ready to upload: {output}")
```

### Use Case 2: I want to copy the editing style of a viral video

```bash
# Learn the style
python examples/copy_editing_style.py learn --reference viral_video.mp4

# Apply to your videos
python examples/copy_editing_style.py apply \
  --input my_video.mp4 \
  --style styles/viral_video.json \
  --format reels
```

### Use Case 3: I need to export to all Instagram formats

```python
from src.core.video_output import VideoOutput

formats = ['stories', 'reels', 'feed_square', 'feed_portrait']
outputs = VideoOutput.batch_export('my_video.mp4', formats)

for format_name, path in outputs.items():
    if path:
        print(f"✓ {format_name}: {path}")
```

### Use Case 4: I want consistent editing across all my videos

```python
from src.models.editing_style import EditingStyle
from src.analysis.style_analyzer import apply_style_to_video

# Create or load your brand style
style = EditingStyle.load('styles/my_brand_style.json')

# Apply to all videos
videos = ['video1.mp4', 'video2.mp4', 'video3.mp4']
for video in videos:
    output = apply_style_to_video(video, style, 'reels')
    print(f"Processed: {output}")
```

## 📖 Next Steps

Now that you're set up, explore these resources:

1. **README.md** - Overview and features
2. **STYLE_TRANSFER_GUIDE.md** - Complete guide to copying editing styles
3. **FAQ.md** - Common questions and answers
4. **examples/** - Working code examples

### Try the Examples

**Basic editing:**
```bash
python examples/basic_edit.py
```

**Style transfer:**
```bash
python examples/copy_editing_style.py
```

**With your own video:**
```bash
python examples/basic_edit.py your_video.mp4 --formats stories reels
```

## 🎓 Learning Path

### Beginner
1. Start with `quick_convert()` for simple format conversion
2. Explore the preset editing styles
3. Try exporting to different Instagram formats

### Intermediate
1. Learn style transfer from reference videos
2. Customize editing styles
3. Use validation to check video compatibility
4. Batch process multiple videos

### Advanced
1. Create custom editing styles programmatically
2. Build automated video processing pipelines
3. Integrate with your content workflow
4. Extend with custom processors (Phase 2+)

## 💡 Tips

1. **Start Simple**: Begin with basic format conversion before exploring advanced features
2. **Use Presets**: Try the preset styles before creating custom ones
3. **Validate First**: Check video compatibility before processing
4. **Save Styles**: Build a library of reusable editing styles
5. **Read Documentation**: Each module has detailed docstrings

## 🐛 Troubleshooting

### Import Errors
```bash
# Make sure you're in the project directory
cd /path/to/VideoAgent

# Install dependencies
pip install -r requirements.txt
```

### FFmpeg Not Found
```bash
# Verify FFmpeg is installed
ffmpeg -version

# If not, install it
brew install ffmpeg  # macOS
```

### Module Not Found
```python
# Add project to Python path
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
```

### Video Processing Fails
Check the logs for specific errors. Common issues:
- Corrupted video file
- Unsupported codec
- Insufficient disk space
- Memory limitations (for very large videos)

## 📞 Getting Help

If you encounter issues:

1. Check **FAQ.md** for common questions
2. Review error messages in the logs
3. Verify setup with `python verify_setup.py`
4. Check that FFmpeg is properly installed
5. Ensure all dependencies are installed

## 🎉 You're Ready!

Your setup is complete. Start converting and editing videos for Instagram!

**Quick Test:**
```bash
# Run the examples to see everything in action
python examples/basic_edit.py
python examples/copy_editing_style.py
```

**Create Your First Video:**
```python
from src.core.pipeline import quick_convert

output = quick_convert('your_video.mp4', 'reels')
print(f"Your Instagram Reel is ready: {output}")
```

Happy editing! 🎬
