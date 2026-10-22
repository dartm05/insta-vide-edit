"""
FFmpeg Wrapper Utilities
Provides high-level interface for FFmpeg operations.
"""
import subprocess
import json
from pathlib import Path
from typing import Optional, Dict, Any, List
from loguru import logger


class FFmpegWrapper:
    """Wrapper for FFmpeg operations."""

    @staticmethod
    def probe(video_path: Path) -> Dict[str, Any]:
        """
        Extract video metadata using ffprobe.

        Args:
            video_path: Path to video file

        Returns:
            Dictionary containing video metadata

        Raises:
            RuntimeError: If ffprobe fails
        """
        cmd = [
            'ffprobe',
            '-v', 'quiet',
            '-print_format', 'json',
            '-show_format',
            '-show_streams',
            str(video_path)
        ]

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            return json.loads(result.stdout)
        except subprocess.CalledProcessError as e:
            logger.error(f"FFprobe failed: {e.stderr}")
            raise RuntimeError(f"Failed to probe video: {e.stderr}")
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse ffprobe output: {e}")
            raise RuntimeError(f"Invalid ffprobe output: {e}")

    @staticmethod
    def extract_frame(
        video_path: Path,
        output_path: Path,
        timestamp: float,
        width: Optional[int] = None,
        height: Optional[int] = None,
    ) -> bool:
        """
        Extract a single frame from video.

        Args:
            video_path: Path to video file
            output_path: Path to save frame
            timestamp: Timestamp in seconds
            width: Optional output width
            height: Optional output height

        Returns:
            True if successful
        """
        cmd = [
            'ffmpeg',
            '-ss', str(timestamp),
            '-i', str(video_path),
            '-vframes', '1',
        ]

        # Add scaling if specified
        if width or height:
            scale_filter = []
            if width and height:
                scale_filter.append(f'scale={width}:{height}')
            elif width:
                scale_filter.append(f'scale={width}:-1')
            else:
                scale_filter.append(f'scale=-1:{height}')

            cmd.extend(['-vf', ','.join(scale_filter)])

        cmd.extend([
            '-y',  # Overwrite output
            str(output_path)
        ])

        try:
            subprocess.run(
                cmd,
                capture_output=True,
                check=True
            )
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Frame extraction failed: {e.stderr}")
            return False

    @staticmethod
    def build_filter_complex(filters: List[str]) -> str:
        """
        Build FFmpeg filter_complex string from list of filters.

        Args:
            filters: List of filter strings

        Returns:
            Filter complex string
        """
        return ','.join(filters)

    @staticmethod
    def get_duration(video_path: Path) -> float:
        """
        Get video duration in seconds.

        Args:
            video_path: Path to video file

        Returns:
            Duration in seconds
        """
        try:
            probe_data = FFmpegWrapper.probe(video_path)
            return float(probe_data['format']['duration'])
        except (KeyError, ValueError) as e:
            logger.error(f"Failed to get duration: {e}")
            return 0.0

    @staticmethod
    def extract_audio(
        video_path: Path,
        output_path: Path,
        sample_rate: int = 16000,
    ) -> bool:
        """
        Extract audio from video.

        Args:
            video_path: Path to video file
            output_path: Path to save audio
            sample_rate: Audio sample rate

        Returns:
            True if successful
        """
        cmd = [
            'ffmpeg',
            '-i', str(video_path),
            '-vn',  # No video
            '-acodec', 'pcm_s16le',
            '-ar', str(sample_rate),
            '-ac', '1',  # Mono
            '-y',
            str(output_path)
        ]

        try:
            subprocess.run(
                cmd,
                capture_output=True,
                check=True
            )
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Audio extraction failed: {e.stderr}")
            return False

    @staticmethod
    def crop_video(
        video_path: Path,
        output_path: Path,
        x: int,
        y: int,
        width: int,
        height: int,
    ) -> bool:
        """
        Crop video to specified dimensions.

        Args:
            video_path: Path to input video
            output_path: Path to output video
            x: X coordinate of crop
            y: Y coordinate of crop
            width: Width of crop
            height: Height of crop

        Returns:
            True if successful
        """
        cmd = [
            'ffmpeg',
            '-i', str(video_path),
            '-vf', f'crop={width}:{height}:{x}:{y}',
            '-c:a', 'copy',
            '-y',
            str(output_path)
        ]

        try:
            subprocess.run(
                cmd,
                capture_output=True,
                check=True
            )
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Video crop failed: {e.stderr}")
            return False

    @staticmethod
    def concat_videos(
        video_paths: List[Path],
        output_path: Path,
    ) -> bool:
        """
        Concatenate multiple videos.

        Args:
            video_paths: List of video file paths
            output_path: Path to output video

        Returns:
            True if successful
        """
        # Create concat file
        concat_file = output_path.parent / 'concat_list.txt'
        with open(concat_file, 'w') as f:
            for video_path in video_paths:
                f.write(f"file '{video_path.absolute()}'\n")

        cmd = [
            'ffmpeg',
            '-f', 'concat',
            '-safe', '0',
            '-i', str(concat_file),
            '-c', 'copy',
            '-y',
            str(output_path)
        ]

        try:
            subprocess.run(
                cmd,
                capture_output=True,
                check=True
            )
            concat_file.unlink()  # Clean up
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Video concatenation failed: {e.stderr}")
            if concat_file.exists():
                concat_file.unlink()
            return False

    @staticmethod
    def check_ffmpeg_available() -> bool:
        """Check if FFmpeg is available."""
        try:
            subprocess.run(
                ['ffmpeg', '-version'],
                capture_output=True,
                check=True
            )
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False
