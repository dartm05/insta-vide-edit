"""
Instagram Compliance Validators
"""
from pathlib import Path
from typing import Tuple, Optional
from loguru import logger

from config.instagram_specs import VideoSpec, get_spec
from src.models.video_metadata import VideoMetadata


class ValidationResult:
    """Result of validation check."""

    def __init__(self):
        self.is_valid = True
        self.errors = []
        self.warnings = []

    def add_error(self, message: str):
        """Add an error."""
        self.is_valid = False
        self.errors.append(message)
        logger.error(f"Validation error: {message}")

    def add_warning(self, message: str):
        """Add a warning."""
        self.warnings.append(message)
        logger.warning(f"Validation warning: {message}")

    def __str__(self) -> str:
        """String representation."""
        lines = []
        if self.is_valid:
            lines.append("✓ Validation passed")
        else:
            lines.append("✗ Validation failed")

        if self.errors:
            lines.append("\nErrors:")
            for error in self.errors:
                lines.append(f"  - {error}")

        if self.warnings:
            lines.append("\nWarnings:")
            for warning in self.warnings:
                lines.append(f"  - {warning}")

        return "\n".join(lines)


def validate_for_instagram(
    metadata: VideoMetadata,
    format_name: str,
) -> ValidationResult:
    """
    Validate video metadata against Instagram specifications.

    Args:
        metadata: Video metadata
        format_name: Target Instagram format

    Returns:
        ValidationResult object
    """
    result = ValidationResult()

    try:
        spec = get_spec(format_name)
    except ValueError as e:
        result.add_error(str(e))
        return result

    # Check duration
    if not spec.validate_duration(metadata.duration):
        if metadata.duration < spec.min_duration:
            result.add_error(
                f"Video too short: {metadata.duration:.1f}s "
                f"(minimum: {spec.min_duration}s)"
            )
        else:
            result.add_error(
                f"Video too long: {metadata.duration:.1f}s "
                f"(maximum: {spec.max_duration}s)"
            )

    # Check file size
    if not spec.validate_file_size(metadata.file_size_mb):
        result.add_error(
            f"File too large: {metadata.file_size_mb:.1f}MB "
            f"(maximum: {spec.max_file_size_mb}MB)"
        )

    # Check aspect ratio
    target_aspect = spec.get_aspect_ratio_float()
    aspect_diff = abs(metadata.aspect_ratio - target_aspect)
    if aspect_diff > 0.01:
        result.add_warning(
            f"Aspect ratio mismatch: {metadata.get_aspect_ratio_string()} "
            f"(target: {spec.aspect_ratio}). Will apply cropping."
        )

    # Check resolution
    if (metadata.width, metadata.height) != spec.resolution:
        result.add_warning(
            f"Resolution mismatch: {metadata.width}x{metadata.height} "
            f"(target: {spec.resolution[0]}x{spec.resolution[1]}). Will resize."
        )

    # Check audio
    if not metadata.has_audio:
        result.add_warning("Video has no audio track")

    # Check frame rate
    if metadata.fps and abs(metadata.fps - spec.framerate) > 5:
        result.add_warning(
            f"Frame rate mismatch: {metadata.fps:.1f}fps "
            f"(target: {spec.framerate}fps). Will adjust."
        )

    return result


def validate_video_file(video_path: Path) -> ValidationResult:
    """
    Validate that a video file exists and is readable.

    Args:
        video_path: Path to video file

    Returns:
        ValidationResult object
    """
    result = ValidationResult()

    if not video_path.exists():
        result.add_error(f"Video file not found: {video_path}")
        return result

    if not video_path.is_file():
        result.add_error(f"Path is not a file: {video_path}")
        return result

    # Check file extension
    valid_extensions = {'.mp4', '.mov', '.avi', '.mkv', '.m4v', '.webm'}
    if video_path.suffix.lower() not in valid_extensions:
        result.add_warning(
            f"Unusual video format: {video_path.suffix}. "
            f"Recommended: {', '.join(valid_extensions)}"
        )

    # Check file size
    file_size_mb = video_path.stat().st_size / (1024 * 1024)
    if file_size_mb > 100:
        result.add_warning(
            f"Large file size: {file_size_mb:.1f}MB. Processing may take longer."
        )

    return result


def suggest_fixes(metadata: VideoMetadata, spec: VideoSpec) -> dict:
    """
    Suggest fixes for validation issues.

    Args:
        metadata: Video metadata
        spec: Target video specification

    Returns:
        Dictionary of suggested fixes
    """
    fixes = {}

    # Duration fix
    if metadata.duration > spec.max_duration:
        fixes['trim_duration'] = spec.max_duration
        fixes['trim_method'] = 'intelligent'  # Use AI to select best segments

    # Aspect ratio fix
    target_aspect = spec.get_aspect_ratio_float()
    if abs(metadata.aspect_ratio - target_aspect) > 0.01:
        fixes['crop_to_aspect'] = spec.aspect_ratio
        fixes['crop_method'] = 'smart'  # Use AI-guided cropping

    # Resolution fix
    if (metadata.width, metadata.height) != spec.resolution:
        fixes['resize_to'] = spec.resolution
        fixes['resize_method'] = 'lanczos'  # High-quality scaling

    # Frame rate fix
    if metadata.fps and abs(metadata.fps - spec.framerate) > 5:
        fixes['change_fps'] = spec.framerate
        fixes['fps_method'] = 'blend'  # Smooth frame blending

    # File size fix
    if metadata.file_size_mb > spec.max_file_size_mb:
        fixes['reduce_bitrate'] = True
        target_bitrate = int(
            (spec.max_file_size_mb * 8 * 1024 * 1024) / metadata.duration
        )
        fixes['target_bitrate'] = f"{target_bitrate}k"

    return fixes
