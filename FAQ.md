# Frequently Asked Questions

## Can the agent copy the editing of another video?

**YES! This is one of the core features.**

The platform includes a **Style Transfer System** that can:

1. **Analyze any video** to learn its editing style
2. **Extract editing patterns** including:
   - Pacing (shot duration, cuts per minute)
   - Cropping and framing approach
   - Transition types and frequency
   - Caption positioning and styling
   - Color grading and visual effects
   - Music and audio treatment

3. **Save as reusable templates** in JSON format
4. **Apply to unlimited videos** to replicate the editing style

### Quick Example

```python
from src.analysis.style_analyzer import learn_from_video, apply_style_to_video

# Step 1: Learn from a viral video
style = learn_from_video('viral_tiktok.mp4', 'Viral Style')
style.save('styles/viral_style.json')

# Step 2: Apply to your videos
output = apply_style_to_video('my_content.mp4', style, 'reels')
```

### Real-World Use Cases

**Use Case 1: Competitor Analysis**
"I saw a competitor's video that went viral. I want my videos to have the same editing style."

```python
competitor_style = learn_from_video('competitor_viral.mp4', 'Competitor Style')
# Now apply to all your videos
```

**Use Case 2: Brand Consistency**
"I want all our videos to match our best-performing content."

```python
brand_style = learn_from_video('best_video.mp4', 'Brand Style')
brand_style.save('styles/our_brand.json')
# Use for all future videos
```

**Use Case 3: Platform-Specific Styles**
"I need TikTok-style editing for viral content."

```python
from src.models.editing_style import get_preset_style
tiktok_style = get_preset_style('viral_tiktok')
# Fast-paced, bold captions, energetic
```

### What Gets Copied?

The style transfer system analyzes and replicates:

| Category | What's Learned | Example |
|----------|---------------|---------|
| **Pacing** | Shot duration, rhythm, pace | Fast (1-2s shots) vs Slow (5-8s) |
| **Framing** | Crop style, subject focus | Face-centered vs Full scene |
| **Transitions** | Type, frequency | Hard cuts vs Smooth fades |
| **Captions** | Position, style, timing | Center/Bold vs Bottom/Minimal |
| **Visual Effects** | Color grade, filters | Vibrant vs Cinematic vs Natural |
| **Audio** | Music presence, ducking | Background music vs Prominent |

### Pre-Built Styles

Don't have a reference video? Use our preset styles:

1. **Viral TikTok Style**
   - Fast-paced (1.5s avg shots)
   - Bold center captions
   - Vibrant colors
   - Frequent cuts

2. **Professional LinkedIn Style**
   - Medium pace (4s avg shots)
   - Clean, minimal captions
   - Natural colors
   - Smooth transitions

3. **Cinematic YouTube Style**
   - Medium-slow pace (3.5s avg)
   - Elegant captions
   - Atmospheric grading
   - Artistic framing

4. **Casual Vlog Style**
   - Slow pace (5s avg)
   - No captions
   - Natural colors
   - Minimal editing

### Command Line Usage

```bash
# Learn from reference video
python examples/copy_editing_style.py learn --reference viral_video.mp4

# Apply to your video
python examples/copy_editing_style.py apply \
  --input my_video.mp4 \
  --style styles/viral_video.json \
  --format reels

# Use preset style
python examples/copy_editing_style.py apply \
  --input my_video.mp4 \
  --style viral_tiktok \
  --format reels
```

### Full Documentation

See **STYLE_TRANSFER_GUIDE.md** for:
- Complete API reference
- Advanced usage examples
- Style customization
- Combining multiple styles
- Best practices

---

## How accurate is the style copying?

**Current Phase**: Basic style analysis based on video properties (duration, aspect ratio, basic characteristics).

**Phase 3 (Coming Soon)**: AI-powered deep analysis using Claude Vision for:
- Frame-by-frame composition analysis
- Precise cut timing patterns
- Advanced color grading replication
- Audio-visual sync patterns
- Movement and motion analysis

Even in the current phase, the style transfer provides consistent results across multiple videos.

---

## Can I create my own custom styles?

**YES!** You can:

1. **Learn from any video**:
   ```python
   style = learn_from_video('reference.mp4', 'My Custom Style')
   ```

2. **Manually create a style**:
   ```python
   from src.models.editing_style import EditingStyle

   custom_style = EditingStyle(
       name="My Style",
       pace='fast',
       average_shot_duration=2.0,
       primary_transition='cut',
       caption_position='center',
       color_grade='vibrant',
       # ... customize all parameters
   )
   custom_style.save('styles/my_style.json')
   ```

3. **Modify existing styles**:
   ```python
   style = EditingStyle.load('styles/viral_tiktok.json')
   style.caption_position = 'bottom'
   style.color_grade = 'cinematic'
   style.save('styles/modified_style.json')
   ```

---

## What file formats are supported?

**Input**: MP4, MOV, AVI, MKV, M4V, WebM

**Output**: MP4 (H.264) optimized for Instagram with:
- Proper codec (libx264)
- Correct resolution and aspect ratio
- Instagram-compliant bitrate
- AAC audio

---

## Do I need an API key for style transfer?

**No!** Style transfer works without any API calls:
- Style analysis uses local video processing
- Basic pattern extraction is algorithmic
- No cost for learning or applying styles

**API key needed for** (Phase 3):
- AI-powered style analysis (deep pattern recognition)
- Intelligent content-aware editing
- Caption generation
- Advanced crop decisions

---

## Can I use this for batch processing?

**YES!**

```python
from src.models.editing_style import EditingStyle

# Load your style once
style = EditingStyle.load('styles/brand_style.json')

# Apply to many videos
videos = ['video1.mp4', 'video2.mp4', 'video3.mp4']
for video in videos:
    output = apply_style_to_video(video, style, 'reels')
    print(f"Processed: {output}")
```

Or use the pipeline:

```python
from src.core.video_output import VideoOutput

# Export many videos to multiple formats
for video in videos:
    VideoOutput.batch_export(video, ['stories', 'reels', 'feed_square'])
```

---

## How much does it cost?

**Current Phase** (Basic processing):
- **FREE** - No API calls needed
- Only uses local processing (FFmpeg, OpenCV)

**Phase 3** (AI-powered features):
- Estimated ~$0.20 per 60-second video
- Cost-optimized with smart frame sampling
- Optional - you can still use basic features for free

---

## Where are my videos saved?

Default: `./output/` directory

Customize in `.env`:
```
OUTPUT_DIR=./my_videos
```

Or programmatically:
```python
from config.settings import settings
settings.OUTPUT_DIR = Path('/custom/path')
```

---

## Can I preview before processing?

**Yes!** Use validation:

```python
from src.core.video_input import VideoInput

video = VideoInput.load('my_video.mp4')
metadata = video.extract_metadata()

# Check what will happen
print(f"Duration: {metadata.duration}s")
print(f"Resolution: {metadata.width}x{metadata.height}")
print(f"Aspect: {metadata.get_aspect_ratio_string()}")

# Check format compatibility
is_valid, message = video.validate_for_format('stories')
print(f"Stories compatible: {is_valid}")
```

---

## What's the difference between formats?

| Format | Size | Aspect | Best For |
|--------|------|--------|----------|
| Stories | 1080x1920 | 9:16 | Temporary content, behind-the-scenes |
| Reels | 1080x1920 | 9:16 | Viral short-form, entertainment |
| Feed Square | 1080x1080 | 1:1 | Grid aesthetic, universal compatibility |
| Feed Portrait | 1080x1350 | 4:5 | Maximum feed real estate |
| Feed Landscape | 1080x566 | 1.91:1 | Cinematic content, wide scenes |

---

## Need More Help?

- **Style Transfer**: See `STYLE_TRANSFER_GUIDE.md`
- **Basic Usage**: See `README.md`
- **Examples**: Check `examples/` directory
- **Code Documentation**: All functions have detailed docstrings

## Common Issues

### "FFmpeg not found"
Install FFmpeg:
```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt install ffmpeg

# Windows
# Download from ffmpeg.org
```

### "Module not found"
Install dependencies:
```bash
pip install -r requirements.txt
```

### "Video validation failed"
Check the validation message for specific issues. The platform will suggest fixes:
```python
from src.utils.validators import validate_for_instagram, suggest_fixes

validation = validate_for_instagram(metadata, 'stories')
if not validation.is_valid:
    fixes = suggest_fixes(metadata, spec)
    print(f"Suggested fixes: {fixes}")
```
