"""
Video Utility Functions
"""
import hashlib
from pathlib import Path
from typing import Tuple, Optional
from loguru import logger

# Optional imports for advanced features
try:
    import cv2
    import numpy as np
    CV2_AVAILABLE = True
except ImportError:
    CV2_AVAILABLE = False
    cv2 = None
    np = None


def calculate_video_hash(video_path: Path) -> str:
    """
    Calculate SHA256 hash of video file for caching.

    Args:
        video_path: Path to video file

    Returns:
        Hex string of hash
    """
    sha256_hash = hashlib.sha256()
    with open(video_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


def resize_frame(
    frame,
    max_dimension: int = 1024,
):
    """
    Resize frame to fit within max_dimension while preserving aspect ratio.

    Args:
        frame: Input frame as numpy array
        max_dimension: Maximum width or height

    Returns:
        Resized frame
    """
    if not CV2_AVAILABLE:
        logger.warning("OpenCV not available, returning original frame")
        return frame

    height, width = frame.shape[:2]

    if width <= max_dimension and height <= max_dimension:
        return frame

    scale = max_dimension / max(width, height)
    new_width = int(width * scale)
    new_height = int(height * scale)

    return cv2.resize(frame, (new_width, new_height), interpolation=cv2.INTER_AREA)


def calculate_crop_box(
    source_width: int,
    source_height: int,
    target_aspect: float,
    center_x: Optional[int] = None,
    center_y: Optional[int] = None,
) -> Tuple[int, int, int, int]:
    """
    Calculate crop box to achieve target aspect ratio.

    Args:
        source_width: Source video width
        source_height: Source video height
        target_aspect: Target aspect ratio (width/height)
        center_x: Optional center x coordinate for crop
        center_y: Optional center y coordinate for crop

    Returns:
        Tuple of (x, y, width, height)
    """
    source_aspect = source_width / source_height

    if abs(source_aspect - target_aspect) < 0.01:
        # Already correct aspect ratio
        return (0, 0, source_width, source_height)

    if source_aspect > target_aspect:
        # Source is wider, crop horizontally
        crop_width = int(source_height * target_aspect)
        crop_height = source_height
        crop_x = center_x - crop_width // 2 if center_x else (source_width - crop_width) // 2
        crop_y = 0
    else:
        # Source is taller, crop vertically
        crop_width = source_width
        crop_height = int(source_width / target_aspect)
        crop_x = 0
        crop_y = center_y - crop_height // 2 if center_y else (source_height - crop_height) // 2

    # Ensure crop box is within bounds
    crop_x = max(0, min(crop_x, source_width - crop_width))
    crop_y = max(0, min(crop_y, source_height - crop_height))

    return (crop_x, crop_y, crop_width, crop_height)


def detect_faces(frame) -> list:
    """
    Detect faces in a frame using OpenCV.

    Args:
        frame: Input frame as numpy array

    Returns:
        List of face bounding boxes [(x, y, w, h), ...]
    """
    if not CV2_AVAILABLE:
        logger.warning("OpenCV not available, face detection disabled")
        return []

    try:
        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Load face cascade
        face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )

        # Detect faces
        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )

        return faces.tolist() if len(faces) > 0 else []

    except Exception as e:
        logger.error(f"Face detection failed: {e}")
        return []


def calculate_frame_difference(frame1, frame2) -> float:
    """
    Calculate visual difference between two frames.

    Args:
        frame1: First frame
        frame2: Second frame

    Returns:
        Difference score (0-1, higher means more different)
    """
    if not CV2_AVAILABLE:
        return 0.0

    try:
        # Resize to same size if needed
        if frame1.shape != frame2.shape:
            frame2 = cv2.resize(frame2, (frame1.shape[1], frame1.shape[0]))

        # Convert to grayscale
        gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

        # Calculate absolute difference
        diff = cv2.absdiff(gray1, gray2)

        # Calculate mean difference
        mean_diff = np.mean(diff) / 255.0

        return mean_diff

    except Exception as e:
        logger.error(f"Frame difference calculation failed: {e}")
        return 0.0


def is_blurry(frame, threshold: float = 100.0) -> bool:
    """
    Check if a frame is blurry using Laplacian variance.

    Args:
        frame: Input frame
        threshold: Blur threshold (lower = more blurry)

    Returns:
        True if frame is blurry
    """
    if not CV2_AVAILABLE:
        return False

    try:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        laplacian = cv2.Laplacian(gray, cv2.CV_64F)
        variance = laplacian.var()
        return variance < threshold
    except Exception as e:
        logger.error(f"Blur detection failed: {e}")
        return False


def calculate_motion_score(frame1, frame2) -> float:
    """
    Calculate motion score between two frames using optical flow.

    Args:
        frame1: First frame
        frame2: Second frame

    Returns:
        Motion score (0-1, higher means more motion)
    """
    if not CV2_AVAILABLE:
        return 0.0

    try:
        # Convert to grayscale
        gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

        # Calculate optical flow
        flow = cv2.calcOpticalFlowFarneback(
            gray1, gray2, None,
            pyr_scale=0.5, levels=3, winsize=15,
            iterations=3, poly_n=5, poly_sigma=1.2, flags=0
        )

        # Calculate magnitude
        magnitude = np.sqrt(flow[..., 0]**2 + flow[..., 1]**2)
        mean_magnitude = np.mean(magnitude)

        # Normalize to 0-1 range (assuming max motion of 10 pixels)
        return min(mean_magnitude / 10.0, 1.0)

    except Exception as e:
        logger.error(f"Motion calculation failed: {e}")
        return 0.0


def get_safe_zones(width: int, height: int) -> dict:
    """
    Get safe zones for text placement based on video dimensions.

    Args:
        width: Video width
        height: Video height

    Returns:
        Dictionary with safe zone coordinates
    """
    margin_x = int(width * 0.05)
    margin_y = int(height * 0.05)

    return {
        'top': {
            'x': margin_x,
            'y': margin_y,
            'width': width - 2 * margin_x,
            'height': int(height * 0.2),
        },
        'center': {
            'x': margin_x,
            'y': int(height * 0.4),
            'width': width - 2 * margin_x,
            'height': int(height * 0.2),
        },
        'bottom': {
            'x': margin_x,
            'y': int(height * 0.75),
            'width': width - 2 * margin_x,
            'height': int(height * 0.2),
        },
    }


def format_timestamp(seconds: float) -> str:
    """
    Format seconds as HH:MM:SS.mmm.

    Args:
        seconds: Time in seconds

    Returns:
        Formatted timestamp string
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = seconds % 60
    return f"{hours:02d}:{minutes:02d}:{secs:06.3f}"
