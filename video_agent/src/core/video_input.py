"""
Video Input Handler
Loads and validates input videos, extracts metadata.
"""
from pathlib import Path
from typing import Optional, Union
from loguru import logger

from config.settings import settings
from src.models.video_metadata import VideoMetadata
from src.utils.ffmpeg_wrapper import FFmpegWrapper
from src.utils.validators import validate_video_file


class VideoInput:
    """Handles video input operations."""

    def __init__(self, video_path: Path):
        """
        Initialize video input.

        Args:
            video_path: Path to video file
        """
        self.video_path = video_path
        self.metadata: Optional[VideoMetadata] = None

    @classmethod
    def load(cls, video_path: Union[str, Path]) -> 'VideoInput':
        """
        Load a video file.

        Args:
            video_path: Path to video file (string or Path)

        Returns:
            VideoInput instance

        Raises:
            FileNotFoundError: If video file doesn't exist
            ValueError: If video file is invalid
        """
        video_path = Path(video_path)

        logger.info(f"Loading video: {video_path}")

        # Validate file
        validation = validate_video_file(video_path)
        if not validation.is_valid:
            raise ValueError(f"Invalid video file: {validation}")

        if validation.warnings:
            for warning in validation.warnings:
                logger.warning(warning)

        return cls(video_path)

    def extract_metadata(self) -> VideoMetadata:
        """
        Extract video metadata using FFprobe.

        Returns:
            VideoMetadata object

        Raises:
            RuntimeError: If metadata extraction fails
        """
        if self.metadata:
            return self.metadata

        logger.info("Extracting video metadata...")

        try:
            probe_data = FFmpegWrapper.probe(self.video_path)

            # Find video stream
            video_stream = None
            audio_stream = None

            for stream in probe_data.get('streams', []):
                if stream['codec_type'] == 'video' and not video_stream:
                    video_stream = stream
                elif stream['codec_type'] == 'audio' and not audio_stream:
                    audio_stream = stream

            if not video_stream:
                raise RuntimeError("No video stream found")

            # Extract video properties
            width = int(video_stream['width'])
            height = int(video_stream['height'])
            duration = float(probe_data['format'].get('duration', 0))

            # Parse frame rate
            fps_parts = video_stream.get('r_frame_rate', '30/1').split('/')
            fps = float(fps_parts[0]) / float(fps_parts[1])

            total_frames = int(video_stream.get('nb_frames', 0))
            if total_frames == 0:
                total_frames = int(duration * fps)

            # Extract audio properties
            has_audio = audio_stream is not None
            audio_sample_rate = None
            audio_channels = None
            audio_codec = None

            if has_audio:
                audio_sample_rate = int(audio_stream.get('sample_rate', 0))
                audio_channels = int(audio_stream.get('channels', 0))
                audio_codec = audio_stream.get('codec_name')

            # File size
            file_size_mb = self.video_path.stat().st_size / (1024 * 1024)

            self.metadata = VideoMetadata(
                file_path=self.video_path,
                duration=duration,
                width=width,
                height=height,
                fps=fps,
                total_frames=total_frames,
                aspect_ratio=width / height,
                has_audio=has_audio,
                audio_sample_rate=audio_sample_rate,
                audio_channels=audio_channels,
                video_codec=video_stream.get('codec_name'),
                audio_codec=audio_codec,
                bitrate=int(probe_data['format'].get('bit_rate', 0)),
                file_size_mb=file_size_mb,
                format=probe_data['format'].get('format_name'),
            )

            logger.info(f"Metadata extracted: {width}x{height}, {duration:.1f}s, {fps:.1f}fps")
            return self.metadata

        except Exception as e:
            logger.error(f"Failed to extract metadata: {e}")
            raise RuntimeError(f"Metadata extraction failed: {e}")

    def get_info(self) -> dict:
        """
        Get video information as dictionary.

        Returns:
            Dictionary with video information
        """
        if not self.metadata:
            self.extract_metadata()

        return self.metadata.to_dict()

    def validate_for_format(self, format_name: str) -> tuple[bool, str]:
        """
        Validate video for specific Instagram format.

        Args:
            format_name: Instagram format name

        Returns:
            Tuple of (is_valid, message)
        """
        if not self.metadata:
            self.extract_metadata()

        from src.utils.validators import validate_for_instagram

        validation = validate_for_instagram(self.metadata, format_name)

        if validation.is_valid:
            message = "Video is compatible with format"
        else:
            message = "\n".join(validation.errors)

        return validation.is_valid, message

    def __str__(self) -> str:
        """String representation."""
        if not self.metadata:
            return f"VideoInput({self.video_path.name})"

        return (
            f"VideoInput({self.video_path.name}: "
            f"{self.metadata.width}x{self.metadata.height}, "
            f"{self.metadata.duration:.1f}s)"
        )

    def __repr__(self) -> str:
        """Detailed representation."""
        return self.__str__()
