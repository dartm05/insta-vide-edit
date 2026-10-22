"""
AI Model Configuration
"""
from typing import Dict, Any


# Vision Analysis Configuration
VISION_CONFIG = {
    'model': 'claude-sonnet-4-5-20250929',
    'max_tokens': 4096,
    'temperature': 0.7,
    'max_frames_per_batch': 10,  # Send frames in batches to avoid token limits
}


# Analysis Prompts
ANALYSIS_PROMPTS = {
    'initial_analysis': """Analyze these video frames and provide detailed information about:

1. Scene descriptions (what's happening in each frame)
2. Main subjects (people, objects, actions)
3. Text overlays (any text visible in the video)
4. Visual composition (framing, focal points, rule of thirds)
5. Content type (talking head, action, product demo, landscape, etc.)
6. Mood and tone (energetic, calm, professional, casual, etc.)
7. Key moments (visually interesting or important frames)

Provide your analysis in a structured format that can guide video editing decisions.""",

    'crop_analysis': """Analyze these frames to determine optimal cropping for Instagram formats.

For each frame, identify:
1. Primary subject location and size (faces, people, main objects)
2. Secondary elements that should remain visible
3. Text overlays that must not be cropped out
4. Safe crop areas (regions that can be cropped without losing important content)
5. Action areas (movement, gestures, important visual information)

Consider the target aspect ratios:
- 9:16 (Stories/Reels - vertical)
- 1:1 (Feed Square)
- 4:5 (Feed Portrait)

Provide crop recommendations with coordinates and reasoning.""",

    'highlight_detection': """Analyze these video segments and identify the most engaging moments.

Rate each segment (0-100) based on:
1. Visual interest (action, colors, composition)
2. Subject clarity (is the main subject clear and well-framed?)
3. Content value (does this moment convey important information?)
4. Emotional impact (does this evoke emotion or engagement?)
5. Instagram appeal (is this share-worthy content?)

Identify the TOP highlights that should be kept for a short-form Instagram video.""",

    'caption_formatting': """Format this transcript for Instagram captions.

Requirements:
1. Break into readable chunks (5-7 words max per caption)
2. Add appropriate punctuation
3. Optional: Add relevant emojis for emphasis (use sparingly)
4. Preserve timing information
5. Make it scannable and engaging

Transcript: {transcript}

Provide formatted captions with timing.""",

    'effect_selection': """Based on the video content analysis, recommend visual effects and color grading.

Video characteristics:
{video_info}

Recommend:
1. Color grading preset (Vibrant, Cinematic, Warm, Cool, Vintage, Natural)
2. Transition styles (Cut, Fade, Dissolve, etc.)
3. Any special effects that would enhance the content
4. Music mood (if applicable)

Provide recommendations with reasoning.""",
}


# Decision Model Schemas
DECISION_SCHEMAS = {
    'editing_plan': {
        'type': 'object',
        'properties': {
            'crop_decisions': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'timestamp': {'type': 'number'},
                        'format': {'type': 'string'},
                        'crop_box': {
                            'type': 'object',
                            'properties': {
                                'x': {'type': 'integer'},
                                'y': {'type': 'integer'},
                                'width': {'type': 'integer'},
                                'height': {'type': 'integer'},
                            }
                        },
                        'tracking': {'type': 'boolean'},
                    }
                }
            },
            'cuts': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'start': {'type': 'number'},
                        'end': {'type': 'number'},
                        'score': {'type': 'number'},
                        'reason': {'type': 'string'},
                    }
                }
            },
            'captions': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'text': {'type': 'string'},
                        'start': {'type': 'number'},
                        'end': {'type': 'number'},
                        'position': {'type': 'string'},
                    }
                }
            },
            'effects': {
                'type': 'object',
                'properties': {
                    'color_grade': {'type': 'string'},
                    'transitions': {'type': 'array'},
                    'music_mood': {'type': 'string'},
                }
            }
        }
    }
}


# Cost Optimization Settings
COST_OPTIMIZATION = {
    'smart_sampling': True,
    'frame_deduplication': True,
    'batch_processing': True,
    'cache_results': True,
    'max_resolution': 1024,  # Resize frames before sending to API
    'compression_quality': 85,  # JPEG quality for frames
}
