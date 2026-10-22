"""
Editing Style Models
Allows learning and applying editing styles from reference videos.
"""
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from pathlib import Path
import json
from loguru import logger


@dataclass
class EditingStyle:
    """
    Represents an editing style learned from a reference video.
    Can be applied to new videos to replicate the editing approach.
    """
    name: str
    description: Optional[str] = None

    # Pacing & Rhythm
    average_shot_duration: float = 3.0
    min_shot_duration: float = 1.0
    max_shot_duration: float = 5.0
    pace: str = 'medium'  # slow, medium, fast, dynamic

    # Transitions
    primary_transition: str = 'cut'
    transition_frequency: float = 1.0  # transitions per minute

    # Cropping & Framing
    crop_style: str = 'centered'  # centered, dynamic, rule_of_thirds
    subject_focus: str = 'face'  # face, full_body, object, scene
    headroom_percentage: float = 0.15
    motion_tracking: bool = True

    # Captions
    has_captions: bool = True
    caption_position: str = 'center'  # top, center, bottom
    caption_style: str = 'modern'  # minimal, modern, bold, elegant
    caption_frequency: str = 'always'  # always, keywords_only, occasional, never
    words_per_caption: int = 5

    # Visual Effects
    color_grade: str = 'natural'
    saturation_level: float = 1.0  # 0.0-2.0
    contrast_level: float = 1.0
    brightness_level: float = 1.0
    uses_filters: bool = False
    filter_intensity: float = 0.5

    # Audio
    music_presence: str = 'none'  # none, background, prominent
    music_mood: Optional[str] = None
    sound_effects: bool = False
    audio_ducking: bool = True  # Lower music during speech

    # Specific Patterns
    patterns: Dict[str, Any] = field(default_factory=dict)

    # Metadata
    source_video: Optional[Path] = None
    created_from: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'name': self.name,
            'description': self.description,
            'pacing': {
                'average_shot_duration': self.average_shot_duration,
                'min_shot_duration': self.min_shot_duration,
                'max_shot_duration': self.max_shot_duration,
                'pace': self.pace,
            },
            'transitions': {
                'primary_transition': self.primary_transition,
                'transition_frequency': self.transition_frequency,
            },
            'cropping': {
                'crop_style': self.crop_style,
                'subject_focus': self.subject_focus,
                'headroom_percentage': self.headroom_percentage,
                'motion_tracking': self.motion_tracking,
            },
            'captions': {
                'has_captions': self.has_captions,
                'caption_position': self.caption_position,
                'caption_style': self.caption_style,
                'caption_frequency': self.caption_frequency,
                'words_per_caption': self.words_per_caption,
            },
            'visual_effects': {
                'color_grade': self.color_grade,
                'saturation_level': self.saturation_level,
                'contrast_level': self.contrast_level,
                'brightness_level': self.brightness_level,
                'uses_filters': self.uses_filters,
                'filter_intensity': self.filter_intensity,
            },
            'audio': {
                'music_presence': self.music_presence,
                'music_mood': self.music_mood,
                'sound_effects': self.sound_effects,
                'audio_ducking': self.audio_ducking,
            },
            'patterns': self.patterns,
            'metadata': {
                'source_video': str(self.source_video) if self.source_video else None,
                'created_from': self.created_from,
            }
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'EditingStyle':
        """Create from dictionary."""
        return cls(
            name=data['name'],
            description=data.get('description'),
            average_shot_duration=data['pacing']['average_shot_duration'],
            min_shot_duration=data['pacing']['min_shot_duration'],
            max_shot_duration=data['pacing']['max_shot_duration'],
            pace=data['pacing']['pace'],
            primary_transition=data['transitions']['primary_transition'],
            transition_frequency=data['transitions']['transition_frequency'],
            crop_style=data['cropping']['crop_style'],
            subject_focus=data['cropping']['subject_focus'],
            headroom_percentage=data['cropping']['headroom_percentage'],
            motion_tracking=data['cropping']['motion_tracking'],
            has_captions=data['captions']['has_captions'],
            caption_position=data['captions']['caption_position'],
            caption_style=data['captions']['caption_style'],
            caption_frequency=data['captions']['caption_frequency'],
            words_per_caption=data['captions']['words_per_caption'],
            color_grade=data['visual_effects']['color_grade'],
            saturation_level=data['visual_effects']['saturation_level'],
            contrast_level=data['visual_effects']['contrast_level'],
            brightness_level=data['visual_effects']['brightness_level'],
            uses_filters=data['visual_effects']['uses_filters'],
            filter_intensity=data['visual_effects']['filter_intensity'],
            music_presence=data['audio']['music_presence'],
            music_mood=data['audio'].get('music_mood'),
            sound_effects=data['audio']['sound_effects'],
            audio_ducking=data['audio']['audio_ducking'],
            patterns=data.get('patterns', {}),
            source_video=Path(data['metadata']['source_video']) if data['metadata'].get('source_video') else None,
            created_from=data['metadata'].get('created_from'),
        )

    def save(self, filepath: Path):
        """Save style to JSON file."""
        with open(filepath, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)
        logger.info(f"Editing style saved to {filepath}")

    @classmethod
    def load(cls, filepath: Path) -> 'EditingStyle':
        """Load style from JSON file."""
        with open(filepath, 'r') as f:
            data = json.load(f)
        logger.info(f"Editing style loaded from {filepath}")
        return cls.from_dict(data)


# Predefined editing styles
PRESET_STYLES = {
    'viral_tiktok': EditingStyle(
        name='Viral TikTok Style',
        description='Fast-paced with frequent cuts, bold captions, and energetic feel',
        average_shot_duration=1.5,
        min_shot_duration=0.5,
        max_shot_duration=3.0,
        pace='fast',
        primary_transition='cut',
        transition_frequency=40.0,
        crop_style='dynamic',
        subject_focus='face',
        motion_tracking=True,
        has_captions=True,
        caption_position='center',
        caption_style='bold',
        caption_frequency='always',
        words_per_caption=3,
        color_grade='vibrant',
        saturation_level=1.3,
        contrast_level=1.2,
        music_presence='prominent',
    ),
    'professional_linkedin': EditingStyle(
        name='Professional LinkedIn Style',
        description='Clean, professional with subtle transitions and clear messaging',
        average_shot_duration=4.0,
        min_shot_duration=2.0,
        max_shot_duration=8.0,
        pace='medium',
        primary_transition='dissolve',
        transition_frequency=10.0,
        crop_style='centered',
        subject_focus='face',
        motion_tracking=False,
        has_captions=True,
        caption_position='bottom',
        caption_style='minimal',
        caption_frequency='keywords_only',
        words_per_caption=7,
        color_grade='natural',
        saturation_level=0.95,
        contrast_level=1.0,
        music_presence='background',
        music_mood='corporate',
    ),
    'cinematic_youtube': EditingStyle(
        name='Cinematic YouTube Style',
        description='Cinematic look with smooth transitions and atmospheric grading',
        average_shot_duration=3.5,
        min_shot_duration=1.5,
        max_shot_duration=6.0,
        pace='medium',
        primary_transition='fade',
        transition_frequency=15.0,
        crop_style='rule_of_thirds',
        subject_focus='scene',
        motion_tracking=True,
        has_captions=True,
        caption_position='bottom',
        caption_style='elegant',
        caption_frequency='occasional',
        words_per_caption=6,
        color_grade='cinematic',
        saturation_level=0.9,
        contrast_level=1.3,
        brightness_level=0.95,
        uses_filters=True,
        filter_intensity=0.4,
        music_presence='background',
        music_mood='atmospheric',
    ),
    'vlog_casual': EditingStyle(
        name='Casual Vlog Style',
        description='Natural, conversational feel with minimal effects',
        average_shot_duration=5.0,
        min_shot_duration=2.0,
        max_shot_duration=10.0,
        pace='slow',
        primary_transition='cut',
        transition_frequency=8.0,
        crop_style='centered',
        subject_focus='full_body',
        motion_tracking=False,
        has_captions=False,
        color_grade='warm',
        saturation_level=1.1,
        brightness_level=1.05,
        music_presence='none',
    ),
}


def get_preset_style(style_name: str) -> EditingStyle:
    """
    Get a predefined editing style.

    Args:
        style_name: Name of preset style

    Returns:
        EditingStyle object

    Raises:
        ValueError: If style not found
    """
    if style_name not in PRESET_STYLES:
        available = ', '.join(PRESET_STYLES.keys())
        raise ValueError(f"Unknown style '{style_name}'. Available: {available}")

    return PRESET_STYLES[style_name]


def list_preset_styles() -> List[str]:
    """Get list of available preset styles."""
    return list(PRESET_STYLES.keys())
