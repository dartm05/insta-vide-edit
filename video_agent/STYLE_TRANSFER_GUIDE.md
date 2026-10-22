# Style Transfer Guide

## Copy Editing from Another Video

One of the most powerful features of this platform is the ability to **learn editing styles from reference videos** and apply them to your own content. This allows you to replicate the editing approach of viral videos, professional content, or any video whose style you admire.

## How It Works

The platform analyzes a reference video to extract its editing characteristics:

- **Pacing & Rhythm**: Shot duration, cuts per minute, overall pace
- **Cropping & Framing**: How subjects are framed, motion tracking patterns
- **Transitions**: Types of transitions used and their frequency
- **Captions**: Positioning, styling, frequency, word count
- **Visual Effects**: Color grading, saturation, contrast, filters
- **Audio**: Music presence, mood, ducking during speech

These patterns are saved as an **EditingStyle** that can be applied to any new video.

## Quick Start

### 1. Learn from a Reference Video

```python
from src.analysis.style_analyzer import learn_from_video

# Analyze a viral video you want to copy
style = learn_from_video(
    reference_video='viral_tiktok.mp4',
    style_name='Viral TikTok Style',
    save_to='styles/viral_tiktok.json'
)

print(f"Learned style: {style.name}")
print(f"Pace: {style.pace}")
print(f"Shot duration: {style.average_shot_duration}s")
```

### 2. Apply to Your Videos

```python
from src.analysis.style_analyzer import apply_style_to_video
from src.models.editing_style import EditingStyle

# Load the saved style
style = EditingStyle.load('styles/viral_tiktok.json')

# Apply to your content
output = apply_style_to_video(
    input_video='my_content.mp4',
    style=style,
    output_format='reels'
)

print(f"Styled video: {output}")
```

## Command Line Usage

### Learn from Reference
```bash
python examples/copy_editing_style.py learn --reference viral_video.mp4
```

### Apply Style
```bash
python examples/copy_editing_style.py apply \
    --input my_video.mp4 \
    --style styles/viral_video.json \
    --format reels
```

### Compare Two Videos
```bash
python examples/copy_editing_style.py compare \
    --reference video1.mp4 \
    --input video2.mp4
```

## Preset Styles

The platform includes built-in preset styles that you can use immediately:

### 1. Viral TikTok Style
- **Best for**: Short-form social media content
- **Characteristics**: Fast-paced, frequent cuts, bold captions, vibrant colors
- **Typical use**: Reels, TikToks, viral content

```python
from src.models.editing_style import get_preset_style

style = get_preset_style('viral_tiktok')
```

### 2. Professional LinkedIn Style
- **Best for**: Business and professional content
- **Characteristics**: Clean, subtle transitions, clear messaging
- **Typical use**: LinkedIn videos, corporate content

```python
style = get_preset_style('professional_linkedin')
```

### 3. Cinematic YouTube Style
- **Best for**: High-quality narrative content
- **Characteristics**: Smooth transitions, atmospheric grading, rule of thirds
- **Typical use**: YouTube videos, documentaries

```python
style = get_preset_style('cinematic_youtube')
```

### 4. Casual Vlog Style
- **Best for**: Personal, conversational content
- **Characteristics**: Natural feel, minimal effects, longer shots
- **Typical use**: Daily vlogs, lifestyle content

```python
style = get_preset_style('vlog_casual')
```

## Complete Workflow Example

```python
from src.analysis.style_analyzer import learn_from_video, apply_style_to_video
from pathlib import Path

# Step 1: Find a video with editing you like
reference_video = "competitor_viral_video.mp4"

# Step 2: Analyze and learn the style
print("Learning editing style...")
style = learn_from_video(
    reference_video,
    style_name="Competitor Style",
    save_to=Path("styles/competitor_style.json")
)

# Step 3: View what was learned
print(f"\nLearned characteristics:")
print(f"  Pace: {style.pace}")
print(f"  Average shot: {style.average_shot_duration}s")
print(f"  Transitions: {style.primary_transition}")
print(f"  Captions: {style.caption_position} ({style.words_per_caption} words)")
print(f"  Color: {style.color_grade}")
print(f"  Music: {style.music_presence}")

# Step 4: Apply to your videos
print("\nApplying to your content...")
your_videos = ["video1.mp4", "video2.mp4", "video3.mp4"]

for video in your_videos:
    output = apply_style_to_video(video, style, output_format='reels')
    print(f"✓ Created: {output}")

print("\n✓ All videos now have the same editing style!")
```

## Style Properties Reference

### EditingStyle Object

```python
style = EditingStyle(
    name="My Style",
    description="Description of the style",

    # Pacing
    average_shot_duration=3.0,      # seconds
    min_shot_duration=1.0,
    max_shot_duration=5.0,
    pace='medium',                  # slow, medium, fast, dynamic

    # Transitions
    primary_transition='cut',       # cut, fade, dissolve, wipe, slide
    transition_frequency=15.0,      # per minute

    # Cropping
    crop_style='centered',          # centered, dynamic, rule_of_thirds
    subject_focus='face',           # face, full_body, object, scene
    headroom_percentage=0.15,
    motion_tracking=True,

    # Captions
    has_captions=True,
    caption_position='center',      # top, center, bottom
    caption_style='modern',         # minimal, modern, bold, elegant
    caption_frequency='always',     # always, keywords_only, occasional, never
    words_per_caption=5,

    # Visual Effects
    color_grade='natural',          # natural, vibrant, cinematic, warm, cool, vintage
    saturation_level=1.0,           # 0.0-2.0
    contrast_level=1.0,
    brightness_level=1.0,
    uses_filters=False,
    filter_intensity=0.5,

    # Audio
    music_presence='background',    # none, background, prominent
    music_mood='energetic',
    sound_effects=False,
    audio_ducking=True,
)
```

## Advanced: AI-Powered Style Analysis (Phase 3)

In the full implementation (Phase 3), the style analyzer will use Claude Vision to deeply understand editing patterns:

- **Shot composition analysis**: How subjects are positioned in each frame
- **Cut timing patterns**: AI detects rhythm and pacing patterns
- **Visual coherence**: Identifies color palettes and grading consistency
- **Caption timing**: Analyzes sync with speech and visual elements
- **Effect usage patterns**: Detects when and how effects are applied

This deep analysis will allow for much more accurate style replication.

## Tips for Best Results

1. **Choose good references**: Pick videos that are well-edited and consistent in style
2. **Match content types**: Sports videos have different editing than talking heads
3. **Test and iterate**: Try the style on multiple videos and refine as needed
4. **Combine styles**: Load multiple styles and blend their characteristics
5. **Save your styles**: Build a library of styles for different content types

## Use Cases

### 1. Content Creator
"I found a competitor's video that went viral. I want my videos to have the same editing style."

```python
style = learn_from_video('competitor_viral.mp4', 'Viral Style')
for video in my_videos:
    apply_style_to_video(video, style, 'reels')
```

### 2. Agency
"A client wants all their videos to match their brand style. Create a template from their best-performing video."

```python
brand_style = learn_from_video('client_best_video.mp4', 'Client Brand Style')
brand_style.save('styles/client_brand.json')
# Use for all future client videos
```

### 3. Educator
"I want my educational videos to have a professional but engaging style like Khan Academy."

```python
style = get_preset_style('professional_linkedin')
style.caption_frequency = 'keywords_only'
style.pace = 'slow'
# Customize and save
```

### 4. Social Media Manager
"I need to repurpose long-form content into TikTok-style short clips."

```python
tiktok_style = get_preset_style('viral_tiktok')
for long_video in content_library:
    apply_style_to_video(long_video, tiktok_style, 'reels')
```

## Limitations (Current Phase)

The style transfer feature is currently in Phase 1. Full AI-powered style analysis will be available in Phase 3. Current limitations:

- Style analysis is based on basic video properties (duration, aspect ratio, etc.)
- Deep pattern recognition (shot timing, composition analysis) requires AI integration
- Style application uses basic processing without AI-guided decisions

Even with these limitations, the preset styles and basic analysis provide a solid foundation for consistent editing across multiple videos.

## Coming in Phase 3

- **AI-powered deep style analysis** using Claude Vision
- **Frame-by-frame composition analysis**
- **Intelligent cut timing replication**
- **Advanced caption timing patterns**
- **Audio-visual sync pattern detection**
- **Style blending** (combine multiple styles)
- **Style fine-tuning** based on performance metrics

## Questions?

See `examples/copy_editing_style.py` for complete working examples.
