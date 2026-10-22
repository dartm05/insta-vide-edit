"""
Instagram Format Specifications
Defines all Instagram video format requirements and constraints.
"""
from typing import Dict, Tuple, Optional
from dataclasses import dataclass


@dataclass
class VideoSpec:
    """Specification for a video format."""
    name: str
    aspect_ratio: str
    resolution: Tuple[int, int]  # (width, height)
    min_duration: int  # seconds
    max_duration: int  # seconds
    max_file_size_mb: int
    video_codec: str
    audio_codec: str
    framerate: int
    video_bitrate: str
    audio_bitrate: str
    pixel_format: str = "yuv420p"

    def get_aspect_ratio_float(self) -> float:
        """Get aspect ratio as a float (width/height)."""
        w, h = map(int, self.aspect_ratio.split(':'))
        return w / h

    def validate_duration(self, duration: float) -> bool:
        """Check if duration is within acceptable range."""
        return self.min_duration <= duration <= self.max_duration

    def validate_file_size(self, file_size_mb: float) -> bool:
        """Check if file size is within limit."""
        return file_size_mb <= self.max_file_size_mb


# Instagram Format Specifications
INSTAGRAM_SPECS: Dict[str, VideoSpec] = {
    'stories': VideoSpec(
        name='Instagram Stories',
        aspect_ratio='9:16',
        resolution=(1080, 1920),
        min_duration=0,
        max_duration=60,
        max_file_size_mb=30,
        video_codec='libx264',
        audio_codec='aac',
        framerate=30,
        video_bitrate='3500k',
        audio_bitrate='128k',
    ),
    'reels': VideoSpec(
        name='Instagram Reels',
        aspect_ratio='9:16',
        resolution=(1080, 1920),
        min_duration=0,
        max_duration=90,
        max_file_size_mb=30,
        video_codec='libx264',
        audio_codec='aac',
        framerate=30,
        video_bitrate='3500k',
        audio_bitrate='128k',
    ),
    'feed_square': VideoSpec(
        name='Instagram Feed (Square)',
        aspect_ratio='1:1',
        resolution=(1080, 1080),
        min_duration=3,
        max_duration=60,
        max_file_size_mb=30,
        video_codec='libx264',
        audio_codec='aac',
        framerate=30,
        video_bitrate='3500k',
        audio_bitrate='128k',
    ),
    'feed_portrait': VideoSpec(
        name='Instagram Feed (Portrait)',
        aspect_ratio='4:5',
        resolution=(1080, 1350),
        min_duration=3,
        max_duration=60,
        max_file_size_mb=30,
        video_codec='libx264',
        audio_codec='aac',
        framerate=30,
        video_bitrate='3500k',
        audio_bitrate='128k',
    ),
    'feed_landscape': VideoSpec(
        name='Instagram Feed (Landscape)',
        aspect_ratio='1.91:1',
        resolution=(1080, 566),
        min_duration=3,
        max_duration=60,
        max_file_size_mb=30,
        video_codec='libx264',
        audio_codec='aac',
        framerate=30,
        video_bitrate='3500k',
        audio_bitrate='128k',
    ),
}


def get_spec(format_name: str) -> VideoSpec:
    """
    Get video specification for a format.

    Args:
        format_name: Format name (e.g., 'stories', 'reels', 'feed_square')

    Returns:
        VideoSpec object

    Raises:
        ValueError: If format_name is not recognized
    """
    if format_name not in INSTAGRAM_SPECS:
        available = ', '.join(INSTAGRAM_SPECS.keys())
        raise ValueError(
            f"Unknown format '{format_name}'. Available formats: {available}"
        )
    return INSTAGRAM_SPECS[format_name]


def list_formats() -> list[str]:
    """Get list of all available format names."""
    return list(INSTAGRAM_SPECS.keys())


def get_format_by_aspect_ratio(aspect_ratio: str) -> Optional[str]:
    """
    Find a format that matches the given aspect ratio.

    Args:
        aspect_ratio: Aspect ratio string (e.g., '9:16', '1:1')

    Returns:
        Format name or None if no match found
    """
    for format_name, spec in INSTAGRAM_SPECS.items():
        if spec.aspect_ratio == aspect_ratio:
            return format_name
    return None
