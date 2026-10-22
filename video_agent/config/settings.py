"""
Global Configuration Settings
"""
import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Settings:
    """Global application settings."""

    # API Configuration
    ANTHROPIC_API_KEY: str = os.getenv('ANTHROPIC_API_KEY', '')

    # Model Configuration
    CLAUDE_MODEL: str = os.getenv('CLAUDE_MODEL', 'claude-sonnet-4-5-20250929')
    CLAUDE_MAX_TOKENS: int = int(os.getenv('CLAUDE_MAX_TOKENS', '4096'))
    CLAUDE_TEMPERATURE: float = float(os.getenv('CLAUDE_TEMPERATURE', '0.7'))

    # Frame Extraction Settings
    FRAME_SAMPLE_RATE: int = int(os.getenv('FRAME_SAMPLE_RATE', '1'))  # frames per second
    MAX_FRAME_DIMENSION: int = int(os.getenv('MAX_FRAME_DIMENSION', '1024'))  # pixels
    FRAME_QUALITY: int = int(os.getenv('FRAME_QUALITY', '85'))  # JPEG quality 1-100

    # Scene Detection Settings
    SCENE_THRESHOLD: float = float(os.getenv('SCENE_THRESHOLD', '27.0'))
    MIN_SCENE_LENGTH: float = float(os.getenv('MIN_SCENE_LENGTH', '0.5'))  # seconds

    # Audio Settings
    WHISPER_MODEL: str = os.getenv('WHISPER_MODEL', 'base')  # tiny, base, small, medium, large
    SILENCE_THRESHOLD_DB: int = int(os.getenv('SILENCE_THRESHOLD_DB', '-40'))
    MIN_SILENCE_DURATION: int = int(os.getenv('MIN_SILENCE_DURATION', '500'))  # milliseconds

    # Processing Settings
    TEMP_DIR: Path = Path(os.getenv('TEMP_DIR', './temp'))
    OUTPUT_DIR: Path = Path(os.getenv('OUTPUT_DIR', './output'))
    CACHE_DIR: Path = Path(os.getenv('CACHE_DIR', './cache'))

    # Performance Settings
    MAX_VIDEO_MEMORY_MB: int = int(os.getenv('MAX_VIDEO_MEMORY_MB', '2048'))
    ENABLE_CACHING: bool = os.getenv('ENABLE_CACHING', 'true').lower() == 'true'
    PARALLEL_PROCESSING: bool = os.getenv('PARALLEL_PROCESSING', 'true').lower() == 'true'

    # Logging
    LOG_LEVEL: str = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE: Optional[str] = os.getenv('LOG_FILE', None)

    # Caption Settings
    CAPTION_MAX_WORDS: int = int(os.getenv('CAPTION_MAX_WORDS', '7'))
    CAPTION_FONT_SIZE: int = int(os.getenv('CAPTION_FONT_SIZE', '60'))
    CAPTION_FONT_COLOR: str = os.getenv('CAPTION_FONT_COLOR', 'white')
    CAPTION_OUTLINE_COLOR: str = os.getenv('CAPTION_OUTLINE_COLOR', 'black')
    CAPTION_OUTLINE_WIDTH: int = int(os.getenv('CAPTION_OUTLINE_WIDTH', '2'))

    # Cost Optimization
    MAX_FRAMES_PER_VIDEO: int = int(os.getenv('MAX_FRAMES_PER_VIDEO', '60'))
    ENABLE_FRAME_DEDUPLICATION: bool = os.getenv('ENABLE_FRAME_DEDUPLICATION', 'true').lower() == 'true'

    @classmethod
    def ensure_directories(cls):
        """Create necessary directories if they don't exist."""
        cls.TEMP_DIR.mkdir(parents=True, exist_ok=True)
        cls.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        cls.CACHE_DIR.mkdir(parents=True, exist_ok=True)

    @classmethod
    def validate(cls) -> bool:
        """Validate critical settings."""
        if not cls.ANTHROPIC_API_KEY:
            raise ValueError(
                "ANTHROPIC_API_KEY not found. Please set it in your .env file or environment."
            )
        return True


# Create settings instance
settings = Settings()
