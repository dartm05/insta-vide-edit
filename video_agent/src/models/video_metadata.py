"""
Video Metadata Models
"""
from dataclasses import dataclass
from typing import Optional, Dict, Any
from pathlib import Path


@dataclass
class VideoMetadata:
    """Metadata extracted from a video file."""
    file_path: Path
    duration: float  # seconds
    width: int
    height: int
    fps: float
    total_frames: int
    aspect_ratio: float
    has_audio: bool
    audio_sample_rate: Optional[int] = None
    audio_channels: Optional[int] = None
    video_codec: Optional[str] = None
    audio_codec: Optional[str] = None
    bitrate: Optional[int] = None
    file_size_mb: float = 0.0
    format: Optional[str] = None

    def get_aspect_ratio_string(self) -> str:
        """Get aspect ratio as a string (e.g., '16:9')."""
        # Common aspect ratios
        common_ratios = {
            16/9: '16:9',
            9/16: '9:16',
            4/3: '4:3',
            3/4: '3:4',
            1/1: '1:1',
            4/5: '4:5',
            5/4: '5:4',
            21/9: '21:9',
        }

        # Find closest match
        closest_ratio = min(common_ratios.keys(), key=lambda x: abs(x - self.aspect_ratio))
        if abs(closest_ratio - self.aspect_ratio) < 0.01:
            return common_ratios[closest_ratio]

        # Return calculated ratio
        gcd = self._gcd(self.width, self.height)
        return f"{self.width // gcd}:{self.height // gcd}"

    @staticmethod
    def _gcd(a: int, b: int) -> int:
        """Calculate greatest common divisor."""
        while b:
            a, b = b, a % b
        return a

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'file_path': str(self.file_path),
            'duration': self.duration,
            'width': self.width,
            'height': self.height,
            'fps': self.fps,
            'total_frames': self.total_frames,
            'aspect_ratio': self.aspect_ratio,
            'aspect_ratio_string': self.get_aspect_ratio_string(),
            'has_audio': self.has_audio,
            'audio_sample_rate': self.audio_sample_rate,
            'audio_channels': self.audio_channels,
            'video_codec': self.video_codec,
            'audio_codec': self.audio_codec,
            'bitrate': self.bitrate,
            'file_size_mb': self.file_size_mb,
            'format': self.format,
        }


@dataclass
class FrameData:
    """Data for a single video frame."""
    frame_number: int
    timestamp: float  # seconds
    image_path: Optional[Path] = None
    image_data: Optional[bytes] = None
    scene_number: Optional[int] = None
    is_keyframe: bool = False

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'frame_number': self.frame_number,
            'timestamp': self.timestamp,
            'image_path': str(self.image_path) if self.image_path else None,
            'scene_number': self.scene_number,
            'is_keyframe': self.is_keyframe,
        }


@dataclass
class SceneData:
    """Data for a video scene."""
    scene_number: int
    start_frame: int
    end_frame: int
    start_time: float
    end_time: float
    duration: float
    keyframe: Optional[FrameData] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'scene_number': self.scene_number,
            'start_frame': self.start_frame,
            'end_frame': self.end_frame,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'duration': self.duration,
            'keyframe': self.keyframe.to_dict() if self.keyframe else None,
        }


@dataclass
class AudioData:
    """Audio analysis data."""
    has_speech: bool
    transcript: Optional[str] = None
    word_timestamps: Optional[list] = None  # List of (word, start, end) tuples
    silence_segments: Optional[list] = None  # List of (start, end) tuples
    volume_peaks: Optional[list] = None  # List of timestamps
    average_volume: Optional[float] = None
    sample_rate: Optional[int] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'has_speech': self.has_speech,
            'transcript': self.transcript,
            'word_timestamps': self.word_timestamps,
            'silence_segments': self.silence_segments,
            'volume_peaks': self.volume_peaks,
            'average_volume': self.average_volume,
            'sample_rate': self.sample_rate,
        }
