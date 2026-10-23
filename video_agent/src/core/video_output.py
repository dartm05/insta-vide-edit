"""
Video Output Handler
Exports and encodes videos to Instagram-compliant formats.
"""
import subprocess
from pathlib import Path
from typing import Optional, List
from loguru import logger

from config.settings import settings
from config.instagram_specs import VideoSpec, get_spec


class VideoOutput:
    """Handles video output and encoding operations."""

    @staticmethod
    def export(
        input_path: Path,
        output_path: Path,
        spec: VideoSpec,
        filters: Optional[List[str]] = None,
    ) -> Path:
        """
        Export video with Instagram-compliant encoding.

        Args:
            input_path: Path to input video
            output_path: Path to output video
            spec: Instagram format specification
            filters: Optional list of FFmpeg filters to apply

        Returns:
            Path to exported video

        Raises:
            RuntimeError: If export fails
        """
        logger.info(f"Exporting video for {spec.name}...")

        # Ensure output directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Build FFmpeg command
        cmd = [
            'ffmpeg',
            '-i', str(input_path),
        ]

        # Add filters if specified
        if filters:
            filter_complex = ','.join(filters)
            cmd.extend(['-vf', filter_complex])

        # Video encoding settings
        cmd.extend([
            '-c:v', spec.video_codec,
            '-preset', 'medium',
            '-crf', '23',  # Quality (lower = better, 18-28 is good range)
            '-b:v', spec.video_bitrate,
            '-maxrate', spec.video_bitrate,
            '-bufsize', f'{int(spec.video_bitrate[:-1]) * 2}k',
            '-pix_fmt', spec.pixel_format,
            '-r', str(spec.framerate),
            '-s', f'{spec.resolution[0]}x{spec.resolution[1]}',
        ])

        # Check if input has audio stream
        try:
            probe_cmd = ['ffprobe', '-v', 'error', '-select_streams', 'a:0',
                        '-show_entries', 'stream=codec_type', '-of', 'default=nw=1',
                        str(input_path)]
            probe_result = subprocess.run(probe_cmd, capture_output=True, text=True, timeout=5)
            has_audio = 'audio' in probe_result.stdout.lower()
        except:
            has_audio = False

        # Audio encoding settings (only if input has audio)
        if has_audio:
            cmd.extend([
                '-c:a', spec.audio_codec,
                '-b:a', spec.audio_bitrate,
                '-ar', '44100',  # Sample rate
                '-ac', '2',  # Stereo
            ])
        else:
            # No audio in input, skip audio encoding
            cmd.extend(['-an'])  # Disable audio
            logger.info("Input video has no audio stream, encoding video only")

        # Additional flags for compatibility
        cmd.extend([
            '-movflags', '+faststart',  # Enable streaming
            '-profile:v', 'main',  # H.264 profile
            '-level', '4.0',  # H.264 level
        ])

        # Overwrite output
        cmd.extend(['-y', str(output_path)])

        try:
            logger.debug(f"FFmpeg command: {' '.join(cmd)}")
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            logger.info(f"Video exported successfully: {output_path}")
            return output_path

        except subprocess.CalledProcessError as e:
            logger.error(f"Export failed: {e.stderr}")
            raise RuntimeError(f"Video export failed: {e.stderr}")

    @staticmethod
    def export_for_format(
        input_path: Path,
        format_name: str,
        output_dir: Optional[Path] = None,
        output_name: Optional[str] = None,
        filters: Optional[List[str]] = None,
    ) -> Path:
        """
        Export video for specific Instagram format.

        Args:
            input_path: Path to input video
            format_name: Instagram format name
            output_dir: Optional output directory (defaults to settings.OUTPUT_DIR)
            output_name: Optional output filename (defaults to input_name_format.mp4)
            filters: Optional FFmpeg filters

        Returns:
            Path to exported video
        """
        spec = get_spec(format_name)

        if output_dir is None:
            output_dir = settings.OUTPUT_DIR

        if output_name is None:
            stem = input_path.stem
            output_name = f"{stem}_{format_name}.mp4"

        output_path = output_dir / output_name

        return VideoOutput.export(input_path, output_path, spec, filters)

    @staticmethod
    def create_thumbnail(
        video_path: Path,
        output_path: Path,
        timestamp: float = 0.0,
        width: int = 640,
    ) -> Path:
        """
        Create a thumbnail image from video.

        Args:
            video_path: Path to video file
            output_path: Path to save thumbnail
            timestamp: Timestamp in seconds
            width: Thumbnail width (height auto-calculated)

        Returns:
            Path to thumbnail
        """
        logger.info(f"Creating thumbnail at {timestamp}s...")

        cmd = [
            'ffmpeg',
            '-ss', str(timestamp),
            '-i', str(video_path),
            '-vframes', '1',
            '-vf', f'scale={width}:-1',
            '-q:v', '2',  # High quality JPEG
            '-y',
            str(output_path)
        ]

        try:
            subprocess.run(cmd, capture_output=True, check=True)
            logger.info(f"Thumbnail created: {output_path}")
            return output_path

        except subprocess.CalledProcessError as e:
            logger.error(f"Thumbnail creation failed: {e.stderr}")
            raise RuntimeError(f"Failed to create thumbnail: {e.stderr}")

    @staticmethod
    def validate_output(output_path: Path, spec: VideoSpec) -> bool:
        """
        Validate that output video meets Instagram specifications.

        Args:
            output_path: Path to output video
            spec: Instagram format specification

        Returns:
            True if valid
        """
        from src.core.video_input import VideoInput
        from src.utils.validators import validate_for_instagram

        try:
            video = VideoInput.load(output_path)
            metadata = video.extract_metadata()
            validation = validate_for_instagram(metadata, spec.name)

            if not validation.is_valid:
                logger.error(f"Output validation failed: {validation}")
                return False

            if validation.warnings:
                for warning in validation.warnings:
                    logger.warning(warning)

            logger.info("Output validation passed")
            return True

        except Exception as e:
            logger.error(f"Output validation error: {e}")
            return False

    @staticmethod
    def batch_export(
        input_path: Path,
        formats: List[str],
        output_dir: Optional[Path] = None,
    ) -> dict[str, Path]:
        """
        Export video to multiple Instagram formats.

        Args:
            input_path: Path to input video
            formats: List of format names
            output_dir: Optional output directory

        Returns:
            Dictionary mapping format names to output paths
        """
        logger.info(f"Batch exporting to {len(formats)} formats...")

        results = {}
        for format_name in formats:
            try:
                output_path = VideoOutput.export_for_format(
                    input_path,
                    format_name,
                    output_dir
                )
                results[format_name] = output_path

            except Exception as e:
                logger.error(f"Failed to export {format_name}: {e}")
                results[format_name] = None

        return results
